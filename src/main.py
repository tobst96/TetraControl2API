from error import erroradd
import subprocess, sys
from safe import tosafe
import requests
from createconfig import createConfigFile
from notifymydevice import NotifyMyDevice
from logfunc import init_logging, loggingdatei
from tetracontrolstatus import TetraControlStatus
import logging, socket, os
from FeuerSoftVehicle import FeuerSoftVehicle
import schedule, time, configparser, ctypes

LOGGER = init_logging()
LOGDAT = loggingdatei()
LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')


def pid_status():
    p = subprocess.Popen([sys.executable, "/var/StatusClient/pid_status.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = p.communicate()
    #LOGGER.debug('SUBPROCESS ERROR: ' + str(err))
    #LOGGER.debug('SUBPROCESS stdout: ' + str(out.decode()))

def pid_statuslong():
    if checkRAM() < 65:
        p = subprocess.Popen([sys.executable, "/var/StatusClient/pid_statuslong.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = p.communicate()
    else:
        LOGGER.warning("Status 6h Rückwirkend abfragen gestoppt, RAM ist zu voll!")

def pid_heathchecks():
    subprocess.Popen([sys.executable, "/var/StatusClient/pid_heathchecks.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

def pid_checkFeuerSoftCehicle():
    if checkRAM() < 50:
        LOGGER.debug("pid_checkFeuerSoftCehicle start")
        subprocess.Popen([sys.executable, "/var/StatusClient/pid_checkFeuerSoftCehicle.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        LOGGER.warning("Feuersoftware Fahrzeuge werden nicht geholt, RAM ist zu voll!")
def checkRAM():
    total_memory, used_memory, free_memory = map(
        int, os.popen('free -t -m').readlines()[-1].split()[1:])
    ramusefloat = round((used_memory/total_memory) * 100, 2)
    ramusestr = str(ramusefloat)

    if ramusefloat > 70:
        LOGGER.critical("RAM ist zu voll! Über 70%")
        LOGGER.critical("Software wird beendet! Danach neu gestartet!")
        subprocess.Popen([sys.executable, "/var/StatusClient/main.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        sys.exit(0)

    return ramusefloat

def startclient():
    
    config = configparser.ConfigParser(interpolation=None)
    file = f"/var/StatusClient/config/config.ini"
    config.read(file, encoding='utf-8')

    prog = TetraControlStatus(user=config.get("TetraControl","user"), password=config.get("TetraControl","password"),url=config.get("TetraControl","url"),notifymydevice="6UOCIS9FRQNDX634NUO9YM731")


    TetraControlStatus.checkTC(prog)
    
    schedule.every(1).seconds.do(pid_status)
    schedule.every(5).seconds.do(checkRAM)
    schedule.every(6).hours.do(pid_statuslong)
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
    subprocess.Popen([sys.executable, "/var/StatusClient/pid_startup.py"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    startclient()
    