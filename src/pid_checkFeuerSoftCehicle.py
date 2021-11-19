
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
from logfunc import init_logging, loggingdatei
LOGGER = init_logging()
LOGDAT = loggingdatei()
LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')


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
LOGGER.info("Whitelist geschrieben in " + str(timede) + "sek")