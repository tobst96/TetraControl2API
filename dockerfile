FROM python:buster



COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

#RUN \
#    pip3 install requests\
#    pip3 install configparser==3.5.0b2\
#    pip3 install time\
#    pip3 install re\
#    pip3 install json\
#    pip3 install ctypes\
#    pip3 install logging\
#    pip3 install os\
#    pip3 install ast\
#    pip3 install urllib3\
#    pip3 install socket\
#    pip3 install base64\
#    pip3 install schedule


WORKDIR /var/StatusClient

COPY /src /var/StatusClient


RUN echo "Erstellt StatusClient"

CMD [ "python3", "main.py" ]
