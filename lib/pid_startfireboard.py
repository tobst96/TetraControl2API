import subprocess, sys, logging, chromalog

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

class sendStatusToFireboard:
    def __init__(self, issi, status, name):
        self.issi = issi
        self.status = status
        self.name = name
        self.searchToken()

    def searchToken(self):
            try:
                self.path_items = self.config.items("Fireboard")
                for key, token in self.path_items: 
                    if token != "Kann belibig erweitert werden. Token Nummer nur erhöhen":
                        self.token = token
                        self.loadFireboard()
            except Exception as ex:
                self.LOGGER.error(str(ex))
                self.LOGDAT.error(str(ex))

    def loadFireboard(self):
        subprocess.Popen(["python3", "/var/StatusClient/lib/pid_statusfireboard.py", self.status, self.issi, self.name, self.token])

sendStatusToFireboard(sys.argv[1], sys.argv[2], sys.argv[3])