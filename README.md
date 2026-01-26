# nfc Web Linker

This repo holds the raw python code that can be used to link an USB NFC Reader that is based on PC/SC protocol (e.g. this one here https://www.trust.com/de/product/24736-ceto-contactless-smartcard-reader) with a specific web url. If you use this code and place a nfc tag on the reader the url specified will be openend in you default browser.

### Dependencies
This project build on top of pyscard – find it here https://github.com/LudovicRousseau/pyscard

For Windows Users: You need to install Visual Studio Build Tools in order to be able to compile pyscard. Find the build tools here https://visualstudio.microsoft.com/visual-cpp-build-tools/


### Add nfc uids
Is you know your uid open uids.json and add an entry
''''"5A4400FF014189":"https://www.url.com"''''

where the first string is the uid of the nfc and the second string is the url to call

### Installation
Install Python 3.14 from here https://www.python.org/downloads/

Clone this Repo
''''git clone https://github.com/kempermo/nfcWebLinker.git''''

cd into the repo
''''cd path/to/repo''''

activate virtual environment
''''source venv/bin/activate''''

start Python Script
''''python pythonGHI.py''''

### Building App
Use this command to build a standalone app
''''pyinstaller --onefile --add-data "assets:uids.json;." pythonGHI.py''''
