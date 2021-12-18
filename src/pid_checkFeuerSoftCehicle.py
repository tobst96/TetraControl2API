
from error import erroradd
import subprocess, sys
from safe import tosafe
import requests
from notifymydevice import NotifyMyDevice
from createconfig import createConfigFile
from logfunc import init_logging, loggingdatei
from tetracontrolstatus import TetraControlStatus
import logging, socket
from FeuerSoftVehicle import FeuerSoftVehicle
import schedule, time, configparser, ctypes
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
LOGGER.addHandler(GelfUdpHandler(host='https://seq.tobiobst.de', port=12201))

fhd = logging.FileHandler("/var/StatusClient/StatusAPI/logging.log", encoding = "UTF-8")
fhd.setLevel(logging.DEBUG)
LOGDAT = logging.getLogger('>>>logdata<<<')
LOGDAT.addHandler(fhd)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
fhd.setFormatter(formatter)  
LOGDAT.addHandler(fhd)  


config = configparser.ConfigParser(interpolation=None)
file = f"/var/StatusClient/config/config.ini"
config.read(file, encoding='utf-8')


start = time.time()
path_items = config.items("Feuersoftware")
computername = socket.gethostname()
for key, token in path_items:
    if token != "Kann belibig erweitert werden. Token Nummer nur erhöhen":
        #LOGGER.debug("Token Feuersoftware abfragen der Fahrzeuge: " + str(token[0:10]))
        progFeuerSoftVehicle = FeuerSoftVehicle(token, key)
        FeuerSoftVehicle.start(progFeuerSoftVehicle)



ende = time.time()
timede = ('{:5.3f}'.format(ende-start))
LOGGER.info("Whitelist Feuersoftware Fahrzeuge geschrieben in " + str(timede) + "sek")