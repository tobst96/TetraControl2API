from pygelf import GelfUdpHandler
import logging, time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(GelfUdpHandler(host='192.168.2.19', port=12201, debug=True))

while True:
    logger.info("INFO test")
    logger.error("ERROR test")
    time.sleep(1)