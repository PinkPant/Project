FROM ubuntu:latest
RUN apt-get update
RUN apt-get -y install \
        python-pip \
        python-setuptools \
        build-essential \
        nodejs \
        npm
COPY . /flask_app
WORKDIR /flask_app
RUN pip install -r requirements.txt
RUN npm install -g coffee-script
RUN npm install -g yo generator-hubot
RUN useradd -d /hubot -m -s /bin/bash -U hubot
USER hubot
WORKDIR /hubot
RUN yo hubot --name="group3bot" --defaults
CMD ["/bin/bash"]
