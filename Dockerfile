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
VOLUME /home/src/gamedeals/resources
WORKDIR /home/src/gamedeals/
CMD ["python", "-u", "Main.py"]
