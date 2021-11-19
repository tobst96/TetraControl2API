import json, os, logging, requests
LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')

def erroradd():

    errorsend = 1
    if not os.path.isdir("StatusAPI"):
        os.system("mkdir StatusAPI")
    if not os.path.isfile("/var/StatusClient/StatusAPI/error.json"):
        jsondata = {"error": 0}
        json.dump(jsondata,open('/var/StatusClient/StatusAPI/error.json','w'))
    with open('/var/StatusClient/StatusAPI/error.json','r') as file:
        error = json.loads(file.read())
    error["error"] = int(error["error"]) + 1
    json.dump(error,open('/var/StatusClient/StatusAPI/error.json','w'))
    if error["error"] >= errorsend:
        sendtoapi(str(error["error"]))

def sendtoapi(value):
    try:
        r = requests.get("http://192.168.2.35api/v1/statusserver/error/" + value, timeout=5)
        if r.status_code == 200:
            jsondata = {"error": 0}
            json.dump(jsondata,open('/var/StatusClient/StatusAPI/error.json','w'))
            LOGGER.debug("Error Report send")
        else:
            LOGGER.critical("Error Report can't send!")
    except:
        LOGGER.critical("Error Report can't send!")

