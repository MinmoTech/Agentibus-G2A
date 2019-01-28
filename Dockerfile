FROM selenium/standalone-chrome-debug
COPY . GameDeals
RUN sudo apt-get update && \
    sudo apt-get install -y \
    python3-dev \
    python3-pip --fix-missing && \
    pip install GameDeals/ && \
    rm -rf GameDeals/ && \
    mkdir -p gamedeals/resources/
ENV AGENTIBUS_RESOURCES gamedeals/resources/
ENV PYTHONUNBUFFERED 0
CMD ["agentibus"]
