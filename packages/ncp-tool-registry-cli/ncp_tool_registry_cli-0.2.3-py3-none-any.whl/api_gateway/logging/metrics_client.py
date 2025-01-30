import logging
import threading
import time
import uuid
from queue import Queue, Empty
from typing import Generic, TypeVar

import nflxenv
import requests
from pydantic import BaseModel
from spectator import GlobalRegistry

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)

BATCH_SIZE = 5


class MetricsClient(Generic[T]):
    def __init__(self, stream_name: str):
        self.endpoint = f"https://ksgateway-us-east-1.{nflxenv.nf_env('test')}.netflix.net/REST/v1/stream/{stream_name}"
        self.session = requests.Session()
        self.queue: Queue[T] = Queue()
        self._should_stop = False
        self._worker_thread = None
        self._start_background_worker()

    def _start_background_worker(self):
        def worker():
            while not self._should_stop:
                try:
                    metric = self.queue.get(timeout=1)
                    if metric is None:
                        break
                    metrics_batch = [metric]

                    while len(metrics_batch) < BATCH_SIZE:
                        try:
                            metric = self.queue.get_nowait()
                            if metric is None:
                                break
                            metrics_batch.append(metric)
                        except Empty:
                            break

                    self._log_to_datamesh(metrics_batch)
                except Empty:
                    continue
                except Exception as e:
                    logger.error("Error processing metrics: %s", e)

        self._worker_thread = threading.Thread(target=worker, daemon=True)
        logger.info("Starting metrics client background worker...")
        self._worker_thread.start()

    async def cleanup(self):
        if self._worker_thread and self._worker_thread.is_alive():
            logger.info("Stopping metrics client background worker...")
            self._should_stop = True
            self.queue.put(None)  # Will cause worker thread to stop

            remaining = []
            while True:
                try:
                    metric = self.queue.get_nowait()
                    if metric is not None:
                        remaining.append(metric)
                except Empty:
                    break

            if remaining:
                try:
                    logger.info(f"Flushing {len(remaining)} remaining metrics...")
                    self._log_to_datamesh(remaining)
                except Exception as e:
                    logger.error("Error flushing remaining metrics during shutdown: %s", e)

            self._worker_thread.join(timeout=5)
            if self._worker_thread.is_alive():
                logger.warning("Metrics client background worker didn't shut down cleanly")

    def _log_to_datamesh(self, metrics: list[T]):
        start_time = time.perf_counter()
        success, error = False, None

        try:
            logger.info("Sending %d metric object(s) to datamesh", len(metrics))
            request_body = {
                "appName": "api_gateway",
                "hostname": nflxenv.nf_instance_id(),
                "ack": nflxenv.is_local_dev(),
                "event": [{"uuid": str(uuid.uuid4()), "payload": metric.model_dump(exclude_none=True)} for metric in metrics],
            }

            response = self.session.post(
                self.endpoint,
                json=request_body,
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Connection": "close",
                },
                timeout=10,
            )

            if response.status_code == 207:
                logger.error("Partial success when sending metrics: %s", response.text)
            else:
                response.raise_for_status()

            success = True

        except Exception as e:
            error = str(e)
            logger.error("Failed to send metrics to datamesh: %s", error)
            raise

        finally:
            GlobalRegistry.pct_timer(
                "apigateway.logToDatamesh", tags={"success": str(success).lower(), "error": error if error else "none"}
            ).record(time.perf_counter() - start_time)

    def log_metric(self, metric: T):
        self.queue.put(metric)
