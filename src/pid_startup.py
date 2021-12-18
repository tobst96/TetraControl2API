import subprocess, sys, os, socket, time
from pygelf import GelfUdpHandler
import logging, chromalog, subprocess

from main import pid_statuslong
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
if not os.path.isfile("/var/StatusClient/StatusAPI/StatusToAPI.json"):
    file = open("/var/StatusClient/StatusAPI/StatusToAPI.json", "w")
    file.close()

subprocess.Popen([sys.executable, "/var/StatusClient/pid_heathchecks.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
subprocess.Popen([sys.executable, "/var/StatusClient/pid_checkFeuerSoftCehicle.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
time.sleep(15)
subprocess.Popen([sys.executable, "/var/StatusClient/pid_statuslong.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)