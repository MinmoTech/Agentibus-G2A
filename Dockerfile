FROM selenium/standalone-chrome-debug
COPY . GameDeals
RUN sudo apt-get update && \
    sudo apt-get install -y build-essential && \
    sudo apt-get install -y checkinstall && \
    sudo apt-get install -y libreadline-gplv2-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    zlib1g-dev \
    openssl \
    libffi-dev \
    python3-dev \
    python3-setuptools \
    wget && \
    mkdir /tmp/Python37 && \
    cd /tmp/Python37 && \
    wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz && \
    tar xvf Python-3.7.0.tar.xz && \
    cd /tmp/Python37/Python-3.7.0 && \
    ./configure && \
    sudo make altinstall && \
    cd ../../.. && \
    sudo pip3.7 install GameDeals/ && \
    sudo rm -rf GameDeals/ && \
    sudo mkdir -p gamedeals/resources/
ENV AGENTIBUS_RESOURCES gamedeals/resources/
ENV PYTHONUNBUFFERED 0
RUN python3.7 --version
CMD ["python3.7 agentibus"]
