import sys, requests, os
import chromalog
import logging


from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime 
start_time = datetime.now() 

LOGGER = logging.getLogger('>>>main<<<')
chromalog.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')
fh = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s - %(filename)s')
LOGGER.setLevel(logging.DEBUG)
file = ("/var/api/logging.log")
fh = logging.FileHandler(file, encoding = "UTF-8")
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s - %(filename)s - %(funcName)s')
fh.setFormatter(formatter)  
LOGGER.addHandler(fh)




def DiveraStatusCode(r):
    try:
        if str(r.status_code) == "403":
            LOGGER.error("[" + str(os.getpid()) + "] " + "Falscher Token!")
    except Exception as ex:
        LOGGER.error(str(ex))

status = str(sys.argv[1])
url = str(sys.argv[2])
name = str(sys.argv[3])
token = str(sys.argv[4])
tokendb = token
try:

    try:
        r = requests.post(url, timeout = 60)
        DiveraStatusCode(r)
        time_elapsed = datetime.now() - start_time 
        LOGGER.debug("[" + str(os.getpid()) + "] " + '[Dauer] Verarbeitung Status: {}'.format(time_elapsed))
        msg = (str(name) + " | Info: " + str(r.status_code) + " | Status: " + status + ' | Dauer: {}'.format(time_elapsed))
        LOGGER.debug("[" + str(os.getpid()) + "] " + "[Divera] " + token[0:10] + " " + msg)  

        

        # You can generate a Token from the "Tokens Tab" in the UI
        token = "jFG4vCStSySFlQA9hTrjDfdHZJAD93qn14iCGrd2g75jVDJYW5gMaTg7uhGtlie0Kril0Xuj3oU3g8ScEXdS-g=="
        org = "Obst"
        bucket = "Status"

        client = InfluxDBClient(url="http://192.168.2.19:8086", token=token)



        write_api = client.write_api(write_options=SYNCHRONOUS)


        p = Point("Output:Divera").tag("token", str(tokendb)).tag("status", str(status)).tag("name", str(name)).field("r_statuscode", int(r.status_code))
        write_api.write(bucket=bucket, org=org, record=p)

    except Exception as ex:
        LOGGER.critical("[" + str(os.getpid()) + "] " + "send divera " + str(ex)) 
    
    

except Exception as ex:
    LOGGER.error("[" + str(os.getpid()) + "] " + str(ex))