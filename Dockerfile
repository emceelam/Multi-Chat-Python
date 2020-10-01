FROM alpine:latest

LABEL maintainer="Lambert Lum"
LABEL description="Multi-client Chat Server"

COPY server.py /root
WORKDIR /root
RUN apk add python3

ENTRYPOINT ["./server.py"]

EXPOSE 4020/tcp
