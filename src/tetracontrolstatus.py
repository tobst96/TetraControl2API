from error import erroradd
from datetime import datetime 
from safe import tosafe
from notifymydevice import NotifyMyDevice
import requests, configparser, time, re, json, ctypes, logging, os, ast, urllib3, socket, subprocess, sys
from datetime import datetime
from requests import put, get
from logfunc import init_logging, loggingdatei
LOGGER = init_logging()
LOGDAT = loggingdatei()
LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')

class TetraControlStatus():
    def __init__(self, user, password, url, notifymydevice) -> None:
        self.user = user
        self.password = password
        self.interval = "5"
        self.ralt = ""
        self.summe = 0
        self.urlhost = url
        self.start = time.time()
        self.url = f"http://{self.user}:{self.password }@{url}/API/statusgps.json?maxalterstatus="
        self.mydevice = NotifyMyDevice(notifymydevice)
        send = "Gestartet. Auf dem PC ", socket.gethostname()
        NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol", send)
        
        self.checkPath()

    def checkPath(self):
        if not os.path.isfile("/var/StatusClient/StatusAPI/history.json"):
            file = open("/var/StatusClient/StatusAPI/history.json", "w")
            file.close()
            
        if not os.path.isdir("/var/StatusClient/StatusAPI/fahrzeuge"):
            os.system("mkdir /var/StatusClient/StatusAPI/fahrzeuge")
            

    def checkTC(self):
        try:
            self.r = requests.get(self.url + "1")
            
            if self.r.status_code != 200:
                self.checkTcError(str(self.r.status_code))
                LOGDAT.info("TC StatusCode Check: " + str(self.r.status_code))
            #LOGDAT.debug("TetraControl Check, status: " + str())
        except Exception as ex:
            self.checkTcError(ex)
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - checkTC", str(ex))
            


    def checkTcError(self, ex):
        LOGGER.critical(str(ex))
        LOGDAT.error(str(ex))
        LOGGER.critical("Keine TetraControl Verbindung.")
        LOGGER.warning("Config nicht richtig eingestellt?")


    def start(self):
        try:            
            url = self.url + self.intervalRequest()
            self.requestTC(url)
            if self.ralt != self.r.text:
                self.ralt = self.r.text
                self.rstatus = json.loads(self.r.text)
                for dsatz in self.rstatus["issis"]:
                    self.readStatusJSON(dsatz)
                        
        except Exception as ex:
           LOGGER.critical(str(ex))
           self.checkTC()
           LOGDAT.error(str(ex))
           
           NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - start", str(ex))

    def readStatusJSON(self, dsatz):
        try:
            self.issi = str(dsatz["ISSI"])
            self.status = (dsatz["status"])
            self.name = (dsatz["name"])
            self.statusman()           
            self.start_time = datetime.now() 
            out = "Empfangen: " + str(self.issi) + " | " + str(self.status) + " | " + str(self.name)
            LOGDAT.info(out)
            try:
                self.loadWhitelist()

            except Exception as ex:
                LOGGER.error("tetracontrolstatus" +"API senden: " + str(ex))
                
                erroradd()
                self.loadWhitelist()
                
            
            
            self.jsonStatusList()
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - readStatusJSON", str(ex))

    def jsonStatusList(self):
        try:
            now = datetime.now()
            timestemp = now.strftime("%d/%m/%Y, %H:%M:%S")
            jsondata = {
                "issi" : self.issi,
                "name" : self.name,
                "status" : self.status,
                "ts" : timestemp
            }

            file = open("/var/StatusClient/StatusAPI/history.json", "a")
            file.write("\n" + str(jsondata))
            file.close()

            path = f"/var/StatusClient/StatusAPI/fahrzeuge/{self.issi} - {self.name}.json"
            file = open(path, "a")
            file.write("\n" + str(jsondata))
            file.close()
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - jsonStatusList", str(ex))

    def requestTC(self, url):
        try:
            self.r = requests.get(url)
            #LOGDAT.debug("TetraControl Request: " + str(self.r.text))
        except:
            self.r = None

    def intervalRequest(self):
        try:
            self.ende = time.time()
            self.interval = ('{:5.3f}'.format(self.ende-self.start))
            x = re.findall("([0-9]*).", self.interval)
            x = str(x[0])
            self.interval = int(x)
            
            self.start = time.time()
            self.interval = self.interval + 1
            if self.interval > 10 and self.interval < 20:
                LOGGER.warning("TetraControl Abfrage letzten " + str(self.interval) + "sek")
                LOGDAT.warning("TetraControl Abfrage letzten " + str(self.interval) + "sek")
            if self.interval >= 20 and self.interval < 60:
                LOGGER.error("tetracontrolstatus" +"TetraControl Abfrage letzten " + str(self.interval) + "sek")
                LOGDAT.warning("TetraControl Abfrage letzten " + str(self.interval) + "sek")
            if self.interval >= 60:
                LOGGER.critical("TetraControl Abfrage letzten " + str(self.interval) + "sek")
                LOGDAT.warning("TetraControl Abfrage letzten " + str(self.interval) + "sek")
            return str(self.interval)
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - intervalRequest", str(ex))

    def loadWhitelist(self):
        try:

            self.readConfig()  
            self.loadFireboard()
            self.loadDivera()    
            self.loadFeuerSoft()
            

        except Exception as ex:
            LOGGER.critical(str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - loadWhitelist", str(ex))

    def readConfig(self):
        try:
            self.config = configparser.ConfigParser(interpolation=None)
            file = f"/var/StatusClient/config/config.ini"
            self.config.read(file, encoding='utf-8')
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))

            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - readConfig", str(ex))

    def loadFireboard(self):
        try:
            LOGGER.debug("Send to Fireboard")
            LOGDAT.debug("Send to Fireboard")
            subprocess.Popen(["python3", "/var/StatusClient/lib/pid_startfireboard.py", self.status, self.issi, self.name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 

             
        except Exception as ex:
            LOGGER.error("tetracontrolstatus - fireboard: " +str(ex))

    def loadDivera(self):
        try:
            LOGGER.debug("Send to Divera")
            LOGDAT.debug("Send to Divera")
            subprocess.Popen(["python3", "/var/StatusClient/lib/pid_startDivera.py", self.status, self.issi, self.name], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)   
        except Exception as ex:
            LOGGER.error("tetracontrolstatus - fireboard: " +str(ex))

    def loadFeuerSoft(self):
        try:
            self.path_items = self.config.items("Feuersoftware")
            for key, token in self.path_items:           
                if os.path.isfile(f"/var/StatusClient/StatusAPI/fahrzeugliste/Vehicle_{key}.json"):
                    with open(f"/var/StatusClient/StatusAPI/fahrzeugliste/Vehicle_{key}.json","r") as file:
                        self.checkForSendFeuersoftware(token, file)


        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - loadFeuerSoft", str(ex))

    def checkForSendFeuersoftware(self, token, file):
        try:
            obj = []
            obj = file.read()
            res = obj.strip("").split(', ')
            res = ast.literal_eval(obj)
            for dsatz in res:
                if dsatz == self.issi:
                    self.token = token
                    self.StatusFeuerSoft()
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - checkForSendFeuersoftware", str(ex))
                            
    def StatusFeuerSoft(self): #return statuscode (Http-Fehler-Code)       
        try:
            url = (f"https://connectapi.feuersoftware.com/interfaces/public/vehicle/{self.issi}/status")
            #token = (f"ru_6hrzrN7l6foPIfncJ2IyLvUSowX5iYl1xM1X59NgnUrOKMNd1BtQeoWB33jM5Fsgc0y3SoDI1NYtZHDbFd6tHNaiaHtbQ53RlAehBL6ITnHTQM3tTR7OD2Sldohtdx9AdG5iOfJjLl09TUVMU0zSEzfkECiuNZXSmZhOJyZATSNsarj3D-NZ4NiWTtkMy6EUi8Qjd5m5jFVlIvnffV_yIuUnSlr7NA707L-EXpEJysP6ED4PxYPZayCr-MZAuVOaTy35zMvvDKsoW3bkO-ORppLmKGshiqEU20FCqa_ZbEoQV_Xh6hBI5bRyG6Q7WoOZeITMkogVAjqeOj6pZjK6BlqH_3DnaxSm-0MEb8Ng4AiTATXe4XxVwUbUlg8sYyOCyZyxF_TEYYYED3takC3di0iGIrJ_0qY9OERFqhEXc8qNVz4pe_TpDI-T6B1mOtCQj2gEKvzFQ20mTMuGei2RRV1N-bb3Cp4CzSDtuKmQ51FLIC6VZznn4K4fD4SWREL2zx5l1ysodRWLU3_HvD2Fr-aFXDWUFidI_9j-5rhD3tEUaXyFCGzVMkoHVI5TrPwkVCA")
            #self._FeuerSoftHeader()
            self._FeuerSoftBody()
    
            #self.r = requests.post(url, data=json.dumps(self.body), headers=self.headers)
            data = json.dumps(self.body)
            #headers = self.headers
            subprocess.Popen(["python3", "/var/StatusClient/lib/pid_statusFeuersoftware.py", url, data, self.token], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #self._FeuerSoftStatusVode()
            msg = (str(self.name) + " | Status: " + self.status)
            LOGGER.debug("[" + str(os.getpid()) + "] " + "[Feuersoftware] " + self.token[0:10] + " " + msg) 
        except Exception as ex:
            LOGGER.critical(str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - StatusFeuerSoft", str(ex))

    def _FeuerSoftStatusVode(self):
        try:
            if str(self.r.status_code) == "404":
                LOGGER.warning("Fahrzeug nicht angelegt!")
            if str(self.r.status_code) == "401":
                LOGGER.error("tetracontrolstatus" +"Falscher Token!")
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - _FeuerSoftStatusVode", str(ex))

    def _FeuerSoftBody(self):
        try:
            self.body = {
                            'status': self.status
                    }
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - _FeuerSoftBody", str(ex))

    def _FeuerSoftHeader(self):
        try:
            self.headers = {
                            'authorization': f'bearer {self.token}',
                            'accept': 'application/json',
                            'content-type': 'application/json',
                            }
        except Exception as ex:
            LOGGER.error("tetracontrolstatus" +str(ex))
            LOGDAT.error(str(ex))
            
            NotifyMyDevice.sendmessage(self.mydevice, "Tetracontrol - _FeuerSoftHeader", str(ex))

    def statusman(self): #Passt den Status auf etwas plausiblen an
        if self.status == "0000":
            self.status = ("10")
        if self.status == "8003":
            self.status = ("1")
        if self.status == "8004":
            self.status = ("2")
        if self.status == "8005":
            self.status = ("3")
        if self.status == "8006":
            self.status = ("4")
        if self.status == "8007":
            self.status = ("5")
        if self.status == "8008":
            self.status = ("6")
        if self.status == "8009":
            self.status = ("7")
        if self.status == "800A":
            self.status = ("8")
        if self.status == "800B":
            self.status = ("9")
        if self.status == "800C":
            self.status = ("0")
        if self.status == "8A5B":
            self.status = ("9")
        if self.status == "8A5B":
            self.status = ("EDV abfrage")
