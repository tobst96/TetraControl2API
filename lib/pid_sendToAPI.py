import datetime
import logging, chromalog, sys, subprocess, os, configparser, re

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

fhd = logging.FileHandler("/var/StatusClient/StatusAPI/logging.log", encoding = "UTF-8")
fhd.setLevel(logging.DEBUG)
LOGDAT = logging.getLogger('>>>logdata<<<')
LOGDAT.addHandler(fhd)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
fhd.setFormatter(formatter)  
LOGDAT.addHandler(fhd)  


class sendtoapi():
    def __init__(self, status, issi, name):
        self.status = status
        self.issi = issi
        self.name = name
        self.readConfig()
        self.loadAPI()

    def readConfig(self):
        try:
            self.config = configparser.ConfigParser(interpolation=None)
            file = f"/var/StatusClient/config/config.ini"
            self.config.read(file, encoding='utf-8')
        except Exception as ex:
            LOGGER.error("SendToAPI" +str(ex))
            LOGDAT.error(str(ex))

    def loadAPI(self):
        try:
            self.path_items = self.config.items("SendToAPI")
            for key, url in self.path_items: 
                if url != "Kann belibig erweitert werden. Token Nummer nur erhöhen":
                    self.url = url
                    try:
                        self.url = self.url.replace("%ISSI%", self.issi)
                    except:
                        pass
                    try:
                        self.url = self.url.replace("%STATUS%", self.status)
                    except:
                        pass
                    try:
                        self.url = self.url.replace("%NAME%", self.name)
                    except:
                        pass

                    

        except Exception as ex:
            LOGGER.error("startDivera" +str(ex))
            LOGDAT.error(str(ex))


sendtoapi(status = sys.argv[1], issi= sys.argv[2], name = sys.argv[3])