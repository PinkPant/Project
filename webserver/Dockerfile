FROM ubuntu:latest
RUN apt-get update
RUN apt-get -y install \
        python-pip \
        python-setuptools \
        build-essential
COPY . /flask_app
WORKDIR /flask_app
RUN pip install -r requirements.txt
CMD ["/bin/bash"]
