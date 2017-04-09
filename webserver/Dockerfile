FROM ubuntu:16.04

### Utils ###
RUN apt-get update
RUN apt-get install -y python-setuptools build-essential python-pip

### Flask ###
COPY . /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/bin/bash"]
