import os
import time
import requests, json, logging

LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')

class FeuerSoftVehicle():
    def __init__(self, token, key):       
        self.token = token
        self.key = key
        self.issilist = []
        self.firstrun = True
        self.url = ("https://connectapi.feuersoftware.com/interfaces/public/vehicle")
        self.checkPath()

    def checkPath(self):
        if not os.path.isdir("StatusAPI"):
            os.system("mkdir StatusAPI")
        if not os.path.isdir("/var/StatusClient/StatusAPI/fahrzeugliste"):
            os.system("mkdir /var/StatusClient/StatusAPI/fahrzeugliste")

    def start(self):
        try:
            self.feuersoftwareHeader()
            self.r = requests.get(self.url, headers=self.header, timeout = 5)    
            self.statusCodeFeuersoftware()
            self.issiListGen()
            self.writeIssiList()
            LOGGER.debug("ISSI Liste für " + self.key + " geschrieben")
            LOGDAT.debug("ISSI Liste für " + self.key + " geschrieben")
        except:
            LOGGER.error("Konnte Fahrzeugliste nicht von Feuersoftware holen.")
            LOGGER.warning("Starte neuen Versuch in 5 Sekunden..")
            LOGDAT.error("Konnte Fahrzeugliste nicht von Feuersoftware holen.")

    def writeIssiList(self):
        try:
            with open(f"/var/StatusClient/StatusAPI/fahrzeugliste/Vehicle_{self.key}.json", "w") as outfile:
                outfile.write(str(self.issilist))
        except Exception as ex:
            LOGGER.error(str(ex))
            LOGDAT.error(str(ex))

    def issiListGen(self):
        try:
            jsontext = json.loads(self.r.text)
            for dsatz in jsontext:
                if dsatz["RadioId"] is not None:
                    self.issilist.append(dsatz["RadioId"])
        except Exception as ex:
            LOGGER.error(str(ex))
            LOGDAT.error(str(ex))

    def statusCodeFeuersoftware(self):
        try:
            if str(self.r.status_code) != "200":
                LOGGER.error("Feuersoftware Fahrzeugdaten holen, respone: " + str(self.r.status_code) + ", token: " + str(self.token[0:10]))
            if str(self.r.status_code) == "401":
                LOGGER.critical("Unauthorized Feuersoftware" + ", token: " + str(self.token[0:10]))
            if str(self.r.status_code) == "429":
                LOGGER.critical("Zu vile Anfragen an Feuersoftware" + ", token: " + str(self.token[0:10]))
                LOGDAT.critical("Zu vile Anfragen an Feuersoftware" + ", token: " + str(self.token[0:10]))
        except Exception as ex:
            LOGGER.error(str(ex))
            LOGDAT.error(str(ex))
            
    def feuersoftwareHeader(self):
        self.header = {
                    'authorization': f'bearer {self.token}',
                    'accept': 'application/json',
                    'content-type': 'application/json',
        }  
        return self.header      

    def _scode(self):
        self.scode = self.r.status_code
        return self.scode

    def _text(self):
        self.tetra = (f"{self.r.text}")
        self.tetra = json.loads(self.r.text)
        self.vehicleList = self.tetra
        return self.vehicleList