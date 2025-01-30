# import pytest
# from unittest.mock import Mock, patch
# from pydantic import BaseModel
# from queue import Empty
# import asyncio

# from src.api_gateway.logging.metrics_client import MetricsClient


# class TestMetric(BaseModel):
#     name: str
#     value: int


# @pytest.fixture
# def metrics_client():
#     client = MetricsClient[TestMetric]("test-stream")
#     yield client
#     # Ensure cleanup
#     if client._worker_thread and client._worker_thread.is_alive():
#         client._should_stop = True
#         client.queue.put(None)
#         client._worker_thread.join(timeout=1)


# def test_log_metric_adds_to_queue(metrics_client):
#     metric = TestMetric(name="test", value=42)
#     metrics_client.log_metric(metric)

#     # Verify metric was added to queue
#     queued_metric = metrics_client.queue.get_nowait()
#     assert queued_metric == metric


# @pytest.mark.asyncio
# async def test_cleanup_processes_remaining_metrics(metrics_client):
#     # Add some test metrics
#     metrics = [
#         TestMetric(name="test1", value=1),
#         TestMetric(name="test2", value=2)
#     ]
#     for metric in metrics:
#         metrics_client.log_metric(metric)

#     # Mock the _log_to_datamesh method
#     with patch.object(metrics_client, '_log_to_datamesh') as mock_log:
#         await metrics_client.cleanup()
#         # Verify remaining metrics were processed
#         mock_log.assert_called_once()
#         processed_metrics = mock_log.call_args[0][0]
#         assert len(processed_metrics) == 2
#         assert all(isinstance(m, TestMetric) for m in processed_metrics)


# @pytest.mark.asyncio
# async def test_cleanup_handles_empty_queue(metrics_client):
#     # Mock the _log_to_datamesh method
#     with patch.object(metrics_client, '_log_to_datamesh') as mock_log:
#         await metrics_client.cleanup()
#         # Verify no metrics were processed since queue was empty
#         mock_log.assert_not_called()


# def test_batch_processing(metrics_client):
#     # Mock the _log_to_datamesh method
#     with patch.object(metrics_client, '_log_to_datamesh') as mock_log:
#         # Add metrics up to batch size
#         for i in range(5):
#             metrics_client.log_metric(TestMetric(name=f"test{i}", value=i))

#         # Give the worker thread time to process
#         import time
#         time.sleep(0.1)

#         # Verify batch was processed
#         mock_log.assert_called_once()
#         processed_metrics = mock_log.call_args[0][0]
#         assert len(processed_metrics) == 5
#         assert all(isinstance(m, TestMetric) for m in processed_metrics)


# @patch('requests.Session')
# def test_log_to_datamesh_error_handling(mock_session, metrics_client):
#     mock_session.return_value.post.side_effect = Exception("Test error")

#     metric = TestMetric(name="test", value=42)

#     # Should raise exception but not crash
#     with pytest.raises(Exception):
#         metrics_client._log_to_datamesh([metric])
