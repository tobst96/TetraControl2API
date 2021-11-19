import requests, json, logging
LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')


class NotifyMyDevice():
    def __init__(self, token) -> None:
        self.apitoken = token
        self.url = "https://www.notifymydevice.com/push"

    def sendmessage(self, title, message):
        try:
            data = {"ApiKey": self.apitoken, "PushTitle": title,"PushText": message} 
            headers = {'Content-Type': 'application/json'} 
            r = requests.post(self.url, data=json.dumps(data), headers=headers)
        except:
            pass

