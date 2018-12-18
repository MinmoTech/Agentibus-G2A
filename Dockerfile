FROM python:3.7-alpine
COPY . GameDeals
RUN wget -q "https://chromedriver.storage.googleapis.com/72.0.3626.7/chromedriver_linux64.zip" -O /tmp/chromedriver.zip \
    && unzip /tmp/chromedriver.zip -d /usr/bin/ \
    && rm /tmp/chromedriver.zip
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
CMD ["agentibus"]
