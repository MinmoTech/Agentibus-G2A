FROM python:3.7-alpine
COPY gamedeals gamedeals
COPY LICENSE.txt __init__.py README.adoc requirements.txt gamedeals/
RUN apk add gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev && \
    pip install -r gamedeals/requirements.txt && \
    apk del openssl-dev \
        musl-dev \
        libffi-dev
VOLUME gamedeals/resources
WORKDIR gamedeals/
CMD ["python", "-u", "Main.py"]
