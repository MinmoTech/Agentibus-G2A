FROM python:3.7-alpine
COPY . GameDeals
RUN apk add gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        openssl-dev && \
    pip install GameDeals/ && \
    apk del openssl-dev \
        musl-dev \
        libffi-dev && \
    rm -rf GameDeals/ && \
    mkdir -p gamedeals/resources/
VOLUME gamedeals/resources/
ENV AGENTIBUS_RESOURCES gamedeals/resources/
CMD ["python", "-u", "agentibus"]
