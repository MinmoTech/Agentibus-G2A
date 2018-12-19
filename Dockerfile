FROM python:3.7-stretch
COPY . GameDeals
RUN sudo apt-get update && apt-get install unzip
RUN RUN wget https://dl.google.com/linux/direct/google-chrome-unstable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
    && wget https://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
RUN pip install GameDeals/ && \
    rm -rf GameDeals/ && \
    mkdir -p gamedeals/resources/
ENV AGENTIBUS_RESOURCES gamedeals/resources/
ENV PYTHONUNBUFFERED 0
CMD ["agentibus"]
