FROM python:3.7-alpine
COPY . GameDeals
RUN apk add gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev && \
    pip install GameDeals/ && \
    rm -rf GameDeals/ && \
    apk del openssl-dev \
        musl-dev \
        libffi-dev && \
    mkdir -p gamedeals/resources/
ENV AGENTIBUS_RESOURCES gamedeals/resources/
ENV PYTHONUNBUFFERED 0
CMD ["agentibus"]
