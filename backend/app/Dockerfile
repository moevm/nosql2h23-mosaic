FROM python:latest
ADD backend.py /server/
ADD requirements.txt /server/
WORKDIR /server/
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt