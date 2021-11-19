import logging, os, configparser, time
LOGGER = logging.getLogger('>>>main<<<')
LOGDAT = logging.getLogger('>>>logdata<<<')

def createConfigFile(configfile_name=f"/var/StatusClient/config/config.ini"):
    if not os.path.isfile(configfile_name):
        LOGGER.info("Erstelle Config Datei, diese muss noch Konfiguiert werden")
        cfgfile = open(configfile_name, "w", encoding='utf-8')
        Config = configparser.ConfigParser()

        Config.add_section("TetraControl")
        Config.set("TetraControl", "User","Hier den Benutzer eintragen!")
        Config.set("TetraControl", "Password", "Passwort")
        Config.set("TetraControl", "URL", "192.168.2.100.xxx:8080 oder https://status.internet.de")

        Config.add_section("Monitoring")
        Config.set("Monitoring", "healthchecks", "")

        Config.add_section("Feuersoftware")

        Config.add_section("Divera")

        Config.add_section("Fireboard")

        Config.write(cfgfile)
        cfgfile.close()


