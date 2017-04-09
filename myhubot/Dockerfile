FROM ubuntu:16.04

### Utils ###
RUN apt-get update
RUN apt-get install -y redis-server
RUN apt-get install -y nodejs
RUN apt-get install -y npm

### Setup Server ###
RUN ln -s /usr/bin/nodejs /usr/bin/node
RUN npm install -g npm@latest
RUN npm install -g yo
RUN npm install -g generator-hubot

### Hubot ###
RUN     useradd -d /hubot -m -s /bin/bash -U hubot
COPY    /hubot-myadapter /hubot/hubot-myadapter
RUN ls -al /hubot
RUN     chown hubot:hubot /hubot/hubot-myadapter
USER	hubot
WORKDIR /hubot
RUN     mkdir dist
WORKDIR /hubot/dist
RUN     yo hubot --owner hubot --name myhubot --adapter "shell" --description "Chat Hubot"
USER    root
RUN     npm link /hubot/hubot-myadapter

CMD ["/bin/bash"]

