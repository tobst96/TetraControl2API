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


try:        
    config = configparser.ConfigParser(interpolation=None)
    file = f"/var/StatusClient/config/config.ini"
    config.read(file, encoding='utf-8')
    uuidhc = config.get("Monitoring","URL")
    if uuidhc == "" or uuidhc == None:
        LOGGER.debug("Kein Monitoring eingerichtet. https://healthchecks.io")
    else:
        LOGGER.debug("Monitoring ..")
        url = uuidhc
        response = requests.get(url)
        if response.status_code == 200:
            LOGGER.debug("Monitoring erfolgreich")
        else:
            LOGGER.debug("Monitoring fehlgeschlagen")


except requests.RequestException as e:
    # Log ping failure here...
    LOGGER.error("Ping failed: %s" % e)  

