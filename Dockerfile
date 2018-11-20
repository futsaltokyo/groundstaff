FROM python:3.6-alpine

# Source for chrome driver installation

# TODO: Caching chromedriver installation
# https://github.com/joyzoursky/docker-python-chromedriver/blob/master/py3/py3.6-alpine3.7-selenium/Dockerfile

# update apk repo
RUN echo "http://dl-4.alpinelinux.org/alpine/v3.7/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.7/community" >> /etc/apk/repositories

# install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

# install requirements
# Layer caching
COPY requirements.txt /
RUN pip install -r requirements.txt

ENV groundstaff groundstaff.py
ENV config config.py

ADD $groundstaff $config /

# TODO: Modify the input option 
CMD [ "python", "./groundstaff.py" ]