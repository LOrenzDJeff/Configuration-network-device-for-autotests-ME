FROM debian:stretch-slim
RUN apt-get update \
    && apt-get install -y iperf \
    && apt-get install -y iputils-ping\
    && apt-get install -y net-tools\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["iperf"]
CMD ["-c"]


