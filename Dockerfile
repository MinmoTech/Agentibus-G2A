FROM python:3.7-alpine
ADD . .
RUN apk add gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev && \
    pip install -r requirements.txt && \
    apk del openssl-dev \
        musl-dev \
        libffi-dev
CMD ["python", "-u", "./src/gamedeals/Main.py"]