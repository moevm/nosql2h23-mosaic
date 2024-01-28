FROM ubuntu:22.04
RUN apt-get -y update
RUN apt-get -y upgrade 
RUN apt-get install -y pip
RUN apt-get install -y python3 
COPY . /backend
WORKDIR /backend
RUN pip install -r requirements.txt
CMD python3 ./backend.py