from smartcard.System import readers
from smartcard.CardRequest import CardRequest
from smartcard.Exceptions import NoCardException, CardRequestTimeoutException, CardConnectionException
import time
import json
import webbrowser

#Textfile einlesen
with open("uids.json") as f:
    urls = json.load(f)

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

        #print("UID:", ''.join(f'{x:02X}' for x in data))
        #print("Status:", sw1, sw2)

        # UID ausgeben
        uid = ''.join(f'{x:02X}' for x in data)

        # Nur neue Karten ausgeben
        if uid != previous_uid:
            print("Neue Karte erkannt! UID:", uid)
            webbrowser.open(urls.get(uid, "https://example.com"))
            previous_uid = uid

        connection.disconnect()

        time.sleep(1)

    except CardRequestTimeoutException:
        print("timeout")
        previous_uid = None
        pass
    except Exception as ex:
        import traceback
        traceback.print_exc()
        pass
