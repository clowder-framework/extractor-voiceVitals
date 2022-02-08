# Base image is an Ubuntu based
FROM python:3

# Creating workdir
WORKDIR /home/clowder

RUN apt-get -qq -y update && apt-get install -qq -y libsndfile-dev sox

# RUN shell command

# Install pyClowder and any other python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Adding necessary code to container under workdir
COPY openSmileExtractor.py extractor_info.json /home/clowder/

# Command to be run when container is run
CMD python3 openSmileExtractor.py

ENV MAIN_SCRIPT="openSmileExtractor.py"

