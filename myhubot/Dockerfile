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
USER	hubot
RUN     mkdir /hubot/dist
WORKDIR /hubot/dist
RUN     yo hubot --owner myhubot --name myhubot --adapter "shell" --description "Group 03 Hubot"

USER    root
COPY    /hubot-myadapter /hubot/hubot-myadapter
COPY    /myhubot.coffee /hubot/dist/scripts
RUN     chown hubot:hubot -R /hubot
RUN     rm hubot-scripts.json
RUN     npm link /hubot/hubot-myadapter
CMD ["/bin/bash"]

