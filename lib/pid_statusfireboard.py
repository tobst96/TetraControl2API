from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.etree import ElementTree
from xml.dom import minidom
import urllib.request
import argparse
import time
import sys
import json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import re
from datetime import datetime 
import chromalog
import logging, os
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





def prettify(elem):
    rough_string = ElementTree.tostring(elem)
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="   ", encoding="UTF-8")


def main(status, issi, name, token):
    sys.argv = [sys.argv[0]]
    res = re.search(r'([A-Za-z]* [0-9]*-[0-9]*-[0-9]*)', name)
    parser = argparse.ArgumentParser(description='Fireboard Status erzeugen')
    parser.add_argument('--status', dest='status', default=status)
    parser.add_argument('--timestamp', dest='timestamp', default=str(int(time.time())))
    parser.add_argument('--issi', dest='issi', default=issi)
    try:
        parser.add_argument('--opta', dest='opta', default=res.group(0))
    except:
        pass
    parser.add_argument('--fmsid', dest='fmsid', default='')
    parser.add_argument('--device_id', dest='device_id', default=name)
    parser.add_argument('--apikey', dest='api_key', default=token)
    args = parser.parse_args()
    base_uri = 'https://login.fireboard.net/api?authkey=' + args.api_key +\
               '&call=status_data'

    root = Element('fireboardStatus')
    root.set('version', '1.0')

    status_data = SubElement(root, "statusData")
    SubElement(status_data, 'status').text = args.status
    SubElement(status_data, 'issi').text = args.issi
    SubElement(status_data, 'opta').text = args.opta
    SubElement(status_data, 'fms').text = args.fmsid
    SubElement(status_data, 'device_id').text = args.device_id
    timestamp = SubElement(status_data, 'timestamp')
    SubElement(timestamp, 'long').text = args.timestamp

    pret = prettify(root)
    with urllib.request.urlopen(base_uri, data=pret) as response:
        json_response = json.loads(response.read().decode("utf-8"))
        #LOGGER.debug("[" + str(os.getpid()) + "][Fireboard] " + str(json_response))
        if json_response['status'] == 'error':
            LOGGER.critical("[" + str(os.getpid()) + "][Fireboard]" + str(json_response['errors']))
            return 1
        LOGGER.info("[" + str(os.getpid()) + "]" + "[Fireboard] gesendet " + token[0:10])
        time_elapsed = datetime.now() - start_time 
        LOGGER.debug("[" + str(os.getpid()) + "]" + '[Dauer] Fireboard senden: {}'.format(time_elapsed))
        

        # You can generate a Token from the "Tokens Tab" in the UI
        token = "jFG4vCStSySFlQA9hTrjDfdHZJAD93qn14iCGrd2g75jVDJYW5gMaTg7uhGtlie0Kril0Xuj3oU3g8ScEXdS-g=="
        org = "Obst"
        bucket = "Status"

        client = InfluxDBClient(url="http://192.168.2.19:8086", token=token)



        write_api = client.write_api(write_options=SYNCHRONOUS)

        p = Point("Output:Fireboard").tag("issi", str(issi)).field("status", int(status)).tag("name", str(name).tag("token", str(args.api_key)))
        write_api.write(bucket=bucket, org=org, record=p)
        return 0

    

main(status=str(sys.argv[1]) ,issi = str(sys.argv[2]), name = str(sys.argv[3]), token = str(sys.argv[4]))
