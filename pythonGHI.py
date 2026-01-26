# ToDo: Read the information stored on the nfc
from smartcard.System import readers
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import NoCardException, CardRequestTimeoutException, CardConnectionException
import time
import json
import webbrowser
import sys
import os
from pathlib import Path

#def resource_path(relative):
#    if hasattr(sys, "_MEIPASS"):
#        return Path(sys._MEIPASS) / relative
#    return Path(__file__).parent / relative

#json_path = resource_path("assets/uids.json")

def resource_path(relative_path):
	if hasattr(sys, "_MEIPASS"):
		return os.path.join(sys._MEIPASS, relative_path)
	return os.path.join(os.path.abspath("."), relative_path)

with open(resource_path("uids.json"), "r", encoding="utf-8") as f:
	urls = json.load(f)

#Textfile einlesen
#with open(json_path) as f:
#    urls = json.load(f)

def on_close():
    print("Closing app")
    root.destroy()   # fully closes the app

# Reader-Liste anzeigen
reader = readers()
print("Gefundene Reader:", reader)

connection = reader[0].createConnection() # ersten Reader auswählen

previous_uid = None

while True:
    cardrequest = CardRequest(timeout=1)
    try:
        cardrequest.waitforcard()
        connection.connect()

        # APDU für UID (bei vielen NFC-Tags)
        get_uid = [0xFF, 0xCA, 0x00, 0x00, 0x00]
        data, sw1, sw2 = connection.transmit(get_uid)

        # UID ausgeben
        uid = ''.join(f'{x:02X}' for x in data)

        # Nur neue Karten ausgeben
        if uid != previous_uid:
            print("Neue Karte erkannt! UID:", uid)
            webbrowser.open(urls.get(uid, "https://brandportal.brita.net/product-design/style/category/overview"), new=0)
            previous_uid = uid

        connection.disconnect()

        time.sleep(1)

    except CardRequestTimeoutException:
        #print("timeout")
        previous_uid = None
        pass
    except Exception as ex:
        import traceback
        traceback.print_exc()
        pass
