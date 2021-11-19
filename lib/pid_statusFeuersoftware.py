import sys, requests
import logging

import logging, chromalog, subprocess
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


def _FeuerSoftHeader(token):
    try:
        headers = {
            'authorization': f'bearer {token}',
            'accept': 'application/json',
            'content-type': 'application/json',
            }
        return headers
    except Exception as ex:
        LOGGER.error(str(ex))
   

def _FeuerSoftStatusVode(r):
    try:
        if str(r.status_code) == "404":
            LOGGER.warning("Fahrzeug nicht angelegt!")
        if str(r.status_code) == "401":
            LOGGER.error("Falscher Token!")
    except Exception as ex:
        LOGGER.error(str(ex))

headers = _FeuerSoftHeader(sys.argv[3])
r = requests.post(str(sys.argv[1]), str(sys.argv[2]), headers, timeout = 60)
_FeuerSoftStatusVode(r)


from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime 
 # You can generate a Token from the "Tokens Tab" in the UI
token = "jFG4vCStSySFlQA9hTrjDfdHZJAD93qn14iCGrd2g75jVDJYW5gMaTg7uhGtlie0Kril0Xuj3oU3g8ScEXdS-g=="
org = "Obst"
bucket = "Status"

client = InfluxDBClient(url="http://192.168.2.19:8086", token=token)



write_api = client.write_api(write_options=SYNCHRONOUS)


p = Point("Output:Divera").tag("token", str(sys.argv[3])).tag("url", str(sys.argv[1])).tag("data", str(sys.argv[2])).field("r_statuscode", int(r.status_code))
write_api.write(bucket=bucket, org=org, record=p)