from error import erroradd
import subprocess, sys
from safe import tosafe
import requests
from createconfig import createConfigFile
from notifymydevice import NotifyMyDevice
from logfunc import init_logging, loggingdatei
from tetracontrolstatus import TetraControlStatus
import logging, socket
from FeuerSoftVehicle import FeuerSoftVehicle
import schedule, time, configparser, ctypes

LOGGER = init_logging()
LOGDAT = loggingdatei()
LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')


def pid_status():
    subprocess.Popen([sys.executable, "/var/StatusClient/pid_status.py"])

def pid_heathchecks():
    subprocess.Popen([sys.executable, "/var/StatusClient/pid_heathchecks.py"])

def pid_checkFeuerSoftCehicle():
    subprocess.Popen([sys.executable, "/var/StatusClient/pid_checkFeuerSoftCehicle.py"])

def startclient():
    config = configparser.ConfigParser(interpolation=None)
    file = f"/var/StatusClient/config/config.ini"
    config.read(file, encoding='utf-8')

    prog = TetraControlStatus(user=config.get("TetraControl","user"), password=config.get("TetraControl","password"),url=config.get("TetraControl","url"),notifymydevice="6UOCIS9FRQNDX634NUO9YM731")


    TetraControlStatus.checkTC(prog)
    
    schedule.every(1).seconds.do(pid_status)
    schedule.every(5).minutes.do(TetraControlStatus.checkTC, prog)
    schedule.every(1).minutes.do(pid_heathchecks)
    schedule.every(1).hours.do(pid_checkFeuerSoftCehicle)

    try:
        pid_heathchecks()
        LOGGER.debug("Starte Aufgabenplan.")
        while True:
            #try:
                schedule.run_pending()
                time.sleep(1)
            #except:
            #    LOGGER.error("Software fehler!!")
    except:
        pass

if __name__ == "__main__":
    createConfigFile()
    subprocess.Popen([sys.executable, "/var/StatusClient/pid_startup.py"])
    startclient()
    