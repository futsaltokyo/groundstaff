FROM python:3.6-alpine

# Source for chrome driver installation
# https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79

# TODO: Caching chromedriver installation
RUN apk add wget xvfb unzip

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apk update
RUN apk add google-chrome-stable

# Set up Chromedriver Environment variables
ENV CHROME_DRIVER_VER 2.9
ENV CHROME_DRIVER_DIR /usr/bin/google-chrome-driver
RUN mkdir $CHROME_DRIVER_DIR

# Download and install Chromedriver
RUN wget -q --continue -P $CHROME_DRIVER_DIR "http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VER/chromedriver_linux64.zip"
RUN unzip $CHROME_DRIVER_DIR/chromedriver* -d $CHROME_DRIVER_DIR

# Put Chromedriver into the PATH
ENV PATH $CHROME_DRIVER_DIR:$PATH

# install requirements
# Layer caching
COPY requirements.txt /
RUN pip install -r requirements.txt

ENV groundstaff groundstaff.py
ENV config config.py

ADD $groundstaff $config /

# TODO: Modify the input option 
CMD [ "python", "./groundstaff.py" ]