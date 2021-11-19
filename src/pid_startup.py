import subprocess, sys
from logfunc import init_logging, loggingdatei
import logging, socket


LOGGER = init_logging()
LOGDAT = loggingdatei()
LOGGER.info("Programm gestartet")  
LOGGER.debug("Coputername: " + socket.gethostname()) 
subprocess.Popen([sys.executable, "/var/StatusClient/pid_heathchecks.py"])
subprocess.Popen([sys.executable, "/var/StatusClient/pid_checkFeuerSoftCehicle.py"])