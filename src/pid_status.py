import logging
from tetracontrolstatus import TetraControlStatus
LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')
import configparser, sys
try:
    sys.setrecursionlimit(1024)
    config = configparser.ConfigParser(interpolation=None)
    file = f"/var/StatusClient/config/config.ini"
    config.read(file, encoding='utf-8')
    prog = TetraControlStatus(user=config.get("TetraControl","user"), password=config.get("TetraControl","password"),url=config.get("TetraControl","url"),notifymydevice="6UOCIS9FRQNDX634NUO9YM731")
    TetraControlStatus.start(prog)
except Exception as e:
    LOGGER.critical("pid_Status", str(e))