import datetime
import logging, chromalog, sys, subprocess, os, configparser

from pygelf import GelfUdpHandler

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

class StartDivera():
    def __init__(self, status, issi, name):
        self.status = status
        self.issi = issi
        self.name = name
        self.readConfig()
        self.loadDivera()

    def readConfig(self):
        try:
            self.config = configparser.ConfigParser(interpolation=None)
            file = f"/var/StatusClient/config/config.ini"
            self.config.read(file, encoding='utf-8')
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))


    def loadDivera(self):
        try:
            self.path_items = self.config.items("Divera")
            for key, token in self.path_items: 
                if token != "Kann belibig erweitert werden. Token Nummer nur erhöhen":
                    self.token = token
                    LOGGER.debug("Divera-Token: " + self.token)
                    self.StatusDivera()          
        except Exception as ex:
            LOGGER.error("startDivera" +str(ex))
            LOGDAT.error(str(ex))
           
    def StatusDivera(self):  #return statuscode (Http-Fehler-Code)
        try:
            url = (f"https://www.divera247.com/api/fms?status_id=" + self.status + "&vehicle_issi=" + (str(self.issi)) + '&accesskey=' + self.token)
            subprocess.Popen(["python3", "/var/StatusClient/lib/pid_statusDivera.py", self.status, url, self.name, self.token], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" + "[" + str(os.getpid()) + "] " + str(ex))
            
StartDivera(status = sys.argv[1], issi= sys.argv[2], name = sys.argv[3])