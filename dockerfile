FROM python:buster

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

WORKDIR /var/StatusClient
COPY /src /var/StatusClient

RUN echo "Erstellt StatusClient"

CMD [ "python3", "main-tetracontrol.py" ]
