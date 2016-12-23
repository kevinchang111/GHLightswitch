# GHLightswitch
<p>I wrote this program to allow my Google Home to control my TP-Link HS100 SmartPlug since TP-Link is not officially supported by Google Home yet. I simply leave the script running on my computer throughout the day so that I can turn on/off the smartplug (that my lights are plugged into) using Google Home.</p>

The process:<br/>
1. Use IFTTT to make Google Home (or Google Assistant in IFTTT) write to a Google Spreadsheet either "ON" or "OFF" whenever a certain command (e.g. "Turn on the lights") is called to Google Home. <br/>
2. lightswitch.py reads from the spreadsheet (I used https://github.com/burnash/gspread to read from Google Spreadsheets.) <br/>
3. lightswitch.py sends a signal to the lightswitch to turn ON or OFF respectively. <br/>

Files:<br/>
lightswitch.py: This is the main program that reads from the spreadsheet and sends the signal to the switch.<br/>
lightprofile.py: Fill in this file with the corresponding information. Follow the instructions in https://gspread.readthedocs.io/en/latest/oauth2.html to obtain the authentication file for your Google Spreadsheet.<br/>
