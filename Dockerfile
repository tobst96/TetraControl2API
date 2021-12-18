#FROM python:buster
FROM ubuntu:latest

RUN apt-get update -y
#RUN apt-get upgrade -y
#RUN apt-get autoremove -y
RUN apt-get install sudo -y
RUN sudo apt-get install python3 -y
RUN sudo apt-get install python3-pip -y


COPY requirements.txt ./
RUN pip3 install -r requirements.txt
RUN pip install pygelf

WORKDIR /var/StatusClient
COPY /src /var/StatusClient
COPY /lib /var/StatusClient/lib

RUN mkdir /var/StatusClient/StatusAPI
RUN chmod 777 /var/StatusClient
RUN chmod 777 /var/StatusClient/lib
RUN chmod 777 /var/StatusClient/StatusAPI

CMD [ "python3", "main.py" ]
