import datetime
import sys, requests
from pygelf import GelfUdpHandler
import logging, chromalog, subprocess
LOGGER = logging.getLogger('>>>main<<<')
chromalog.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
fh = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s - %(filename)s')
LOGGER.setLevel(logging.DEBUG)
file = ("/var/StatusClient/StatusAPI/logging.log")
fh = logging.FileHandler(file, encoding = "UTF-8")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(funcName)s')
fh.setFormatter(formatter)  
LOGGER.addHandler(fh)
LOGGER.addHandler(GelfUdpHandler(host='seq.tobiobst.de', port=12201, debug=True))

fhd = logging.FileHandler("/var/StatusClient/StatusAPI/logging.log", encoding = "UTF-8")
fhd.setLevel(logging.DEBUG)
LOGDAT = logging.getLogger('>>>logdata<<<')
LOGDAT.addHandler(fhd)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
fhd.setFormatter(formatter)  
LOGDAT.addHandler(fhd)  

def _FeuerSoftHeader(token):
    try:
        headers = {
            'authorization': f'bearer {token}',
            'accept': 'application/json',
            'content-type': 'application/json',
            }
        return headers
    except Exception as ex:
        LOGGER.error(str(ex))
        LOGDAT.error(str(ex))
   

def _FeuerSoftStatusVode(r):
    try:
        if str(r.status_code) == "404":
            LOGGER.warning("Fahrzeug nicht angelegt!")
            LOGDAT.warning("Fahrzeug nicht angelegt!")  
        if str(r.status_code) == "401":
            LOGGER.error("Falscher Token!")
            LOGDAT.error("Falscher Token!")
    except Exception as ex:
        LOGGER.error(str(ex))
        LOGDAT.error(str(ex))

headers = _FeuerSoftHeader(sys.argv[3])
r = requests.post(str(sys.argv[1]), str(sys.argv[2]), headers, timeout = 60)
_FeuerSoftStatusVode(r)

jsondata = {
    "url" : (str(sys.argv[1])),
    "data" : (str(sys.argv[2])),
    "token" : (str(sys.argv[3])[0:10])
}

file = open("/var/StatusClient/StatusAPI/Feuersoftware.json", "a")
file.write("\n" + str(jsondata))
file.close()
            
