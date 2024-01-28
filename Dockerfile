FROM ubuntu:22.04

RUN apt-get update
RUN apt upgrade -y
#RUN apt-get install -y build-essential 
RUN apt install -y curl 
RUN apt install -y pip
RUN curl -fsSL https://deb.nodesource.com/setup_21.x | apt-get install -y nodejs
RUN apt install -y npm

COPY hello_world/ front/
COPY backend/app back/

WORKDIR /back

RUN pip install -r ./requirements.txt
#RUN nohup python3 ./backend.py

WORKDIR /front

RUN npm cache clean -f
RUN npm install -g n
RUN n stable


RUN npm install
RUN pwd
RUN ls
RUN node -v



EXPOSE 5173

CMD ["npm", "run", "dev"]