FROM selenium/standalone-chrome-debug
COPY . GameDeals
RUN sudo apt-get update && \
    sudo apt-get purge python2.7-minimal -y && \
    sudo apt-get install software-properties-common -y && \
    sudo add-apt-repository ppa:deadsnakes/ppa -y && \
    sudo apt-get update && \
    sudo apt-get install python3.7 -y && \
    sudo apt-get install python3-pip -y && \
    sudo pip3 install virtualenv && \
    sudo mkdir agentibus_venv && \
    sudo virtualenv -p /usr/bin/python3.7 agentibus_venv/agentibus && \
    cd agentibus_venv/agentibus/bin && \
    bash activate && \
    sudo pip3 install GameDeals/ && \
    sudo rm -rf GameDeals/ && \
    sudo mkdir -p gamedeals/resources/
ENV AGENTIBUS_RESOURCES gamedeals/resources/
ENV PYTHONUNBUFFERED 0
RUN python3 --version
CMD ["agentibus"]
