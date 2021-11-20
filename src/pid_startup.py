import subprocess, sys, os
from logfunc import init_logging, loggingdatei
import logging, socket


LOGGER = init_logging()
LOGDAT = loggingdatei()
LOGGER.info("Programm gestartet")  
LOGGER.debug("Coputername: " + socket.gethostname()) 

if not os.path.isfile("/var/StatusClient/StatusAPI/Divera.json"):
    file = open("/var/StatusClient/StatusAPI/Divera.json", "w")
    file.close()
if not os.path.isfile("/var/StatusClient/StatusAPI/Feuersoftware.json"):
    file = open("/var/StatusClient/StatusAPI/Feuersoftware.json", "w")
    file.close()
if not os.path.isfile("/var/StatusClient/StatusAPI/Fireboard.json"):
    file = open("/var/StatusClient/StatusAPI/Fireboard.json", "w")
    file.close()

subprocess.Popen([sys.executable, "/var/StatusClient/pid_heathchecks.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
subprocess.Popen([sys.executable, "/var/StatusClient/pid_checkFeuerSoftCehicle.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)