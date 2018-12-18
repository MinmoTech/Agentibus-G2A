FROM python:3.7-alpine
COPY . GameDeals
RUN apk add gcc \
        musl-dev \
        python3-dev \
        libffi-dev \
        openssl-dev && \
    pip install Gamedeals/ && \
    apk del openssl-dev \
        musl-dev \
        libffi-dev && \
    rm -rf GameDeals/
VOLUME gamedeals/resources
ENV PYTHONPATH /home
WORKDIR gamedeals/
CMD ["python", "-u", "Main.py"]
