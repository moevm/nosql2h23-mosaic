FROM ubuntu:22.04

RUN apt-get update
RUN apt upgrade -y
#RUN apt-get install -y build-essential 
RUN apt install -y npm
RUN apt install -y curl
RUN apt-get install -y nodejs

COPY hello_world/ front/

WORKDIR /front

RUN npm cache clean -f
RUN npm install -g n
RUN n stable

RUN npm install
RUN pwd
RUN ls
RUN node -v

EXPOSE 5173
WORKDIR /front
CMD ["npm", "run", "dev"]