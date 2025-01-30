FROM dockerregistry.test.netflix.net:7002/baseos/jammy:release

COPY ./ /project-snapshot

RUN apt-get update && \
    apt-get install -y git htop nflx-python-{{.ToolVersions.python}} && \
    apt-get install -y nflx-ezconfig nflx-shrimpi proxyd gandalf-agent && \
    /apps/python{{.ToolVersions.python}}/bin/python -mvenv /apps/api-gateway && \
    /apps/api-gateway/bin/pip install -U pip -r /project-snapshot/requirements.txt /project-snapshot && \
    chown -R $NETFLIX_APPUSER /apps/api-gateway && \
    if [[ -d /project-snapshot/root ]]; then rsync -arHK /project-snapshot/root/ /; fi && \
    rm -rf /var/lib/apt/lists/* /project-snapshot

EXPOSE 7001
EXPOSE 7004
EXPOSE 443

CMD ["/nflx/bin/init"]
