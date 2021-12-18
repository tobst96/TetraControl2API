import json
import random
import time

import requests

url = "http://FWWesterstede:Westerstede!@t93k9bi1v8bqausa.myfritz.net:8080"
print("Rufe Funkstatus der letzten 6 Stunden ab!")
r = requests.get(url + "/API/statusgps.json?maxalterstatus=21600")
print("Daten abgerufen!")
rstatus = json.loads(r.text)
#if rstatus != "{'issis': []}":
    #print("TetraControl Status: " + str(rstatus))
    
for dsatz in rstatus["issis"]:

        checktc = requests.get(url + "/API/issi.json?filter=" + str(dsatz["ISSI"]))
        tempstatus = json.loads(checktc.text)
        print("tempstatus: " + str(tempstatus["issis"][0]["status"]))
        print("dsatz: " + dsatz["status"])
        if str(tempstatus["issis"][0]["status"]) == dsatz["status"]:
            print("Status ist gleich, senden!")
            msgtext = "Rückwirkend"
            print("Sende: " + str(dsatz))
        else:
            print("Status ist ungleich, nicht senden! Hat sich in der letzten Zeit geändert! Letzter Status: " + str(tempstatus))
        time.sleep(random.randint(0, 5))
