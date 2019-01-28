FROM python:3.7-stretch
COPY . GameDeals
RUN rm -rf /var/lib/apt/lists/* && \
    apt-get clean && \
    apt-get update && \
    apt-get install -y \
    gconf-service \
    chromium \
    chromedriver \
    lsb-release \
    xdg-utils \
    python3-dev --fix-missing && \
    pip install GameDeals/ && \
    rm -rf GameDeals/ && \
    mkdir -p gamedeals/resources/
ENV AGENTIBUS_RESOURCES gamedeals/resources/
ENV PYTHONUNBUFFERED 0
CMD ["agentibus"]
