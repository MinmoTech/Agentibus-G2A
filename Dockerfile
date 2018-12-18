FROM python:3.7-alpine
COPY src/ GameDeals/src
COPY LICENSE.txt README.adoc requirements.txt GameDeals/
RUN apk add gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev && \
    pip install -r GameDeals/requirements.txt && \
    apk del openssl-dev \
        musl-dev \
        libffi-dev
VOLUME src/gamedeals/resources
WORKDIR GameDeals/src/gamedeals/
CMD ["python", "-u", "Main.py"]
