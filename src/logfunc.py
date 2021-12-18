import logging, os
from pygelf import GelfUdpHandler

def init_loggingalt():    
    LOG_LEVEL = logging.DEBUG
    #LOGFORMAT = "%(log_color)s%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s"
    LOGFORMAT = "%(log_color)s%(asctime)s.%(msecs)03d - %(message)s"
    from colorlog import ColoredFormatter
    logging.root.setLevel(LOG_LEVEL)    
    formatter = ColoredFormatter(LOGFORMAT) 
    stream = logging.StreamHandler()  
    stream.setLevel(LOG_LEVEL)
    stream.setFormatter(formatter) 
    LOGGER = logging.getLogger('>>>main<<<')
    LOGGER.setLevel(LOG_LEVEL)
    LOGGER.addHandler(stream)
    return LOGGER  

def init_logging():
    import logging, chromalog
    LOGGER = logging.getLogger('>>>main<<<')
    chromalog.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    fh = logging.Formatter('%(asctime)s - %(message)s - %(filename)s')
    LOGGER.setLevel(logging.DEBUG)
    file = ("/var/StatusClient/StatusAPI/logging.log")
    fh = logging.FileHandler(file, encoding = "UTF-8")
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(funcName)s')
    fh.setFormatter(formatter)  
    LOGGER.addHandler(fh)
    LOGGER.addHandler(GelfUdpHandler(host='seq.tobiobst.de', port=12201, debug=True))
    return LOGGER

def loggingdatei():
    if not os.path.isdir("StatusAPI"):
        os.system("mkdir StatusAPI")
    fhd = logging.FileHandler("/var/StatusClient/StatusAPI/logging.log", encoding = "UTF-8")
    fhd.setLevel(logging.DEBUG)
    LOGDAT = logging.getLogger('>>>logdata<<<')
    LOGDAT.addHandler(fhd)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(funcName)s')
    fhd.setFormatter(formatter)  
    LOGDAT.addHandler(fhd)   
    return LOGDAT   