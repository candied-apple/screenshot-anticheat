import argparse
import mss
import time
import requests
import os
import socket
import tempfile
import wmi
import atexit
from termcolor import colored
from datetime import datetime

# Replace the webhook_url with your own URL
webhook_url = 'your_discord_webhook'

#Get todays date
now = datetime.now()

date_str = now.strftime("%Y-%m-%d")

# Get the name of the computer running the script
computer_name = socket.gethostname()

# Get the WMI object
wmi_obj = wmi.WMI()

# Get the processor's serial number
for proc in wmi_obj.Win32_Processor():
    hardware_id = proc.ProcessorID.strip()

# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--password', help='password for authentication')
args = parser.parse_args()

# Check if password was provided as a command line argument
if args.password != 'your_password':
    print('Incorrect password. Please try again.')
    exit()

print('Anticheat running. (Do not close this windows otherwise you will be accused of cheating.)')

def send_disconnection_message():
    # Send a disconnection message to Discord using webhook
    payload = {'content': f'**Computer name:** `{computer_name}`\n**Hardware ID CPU:** `{hardware_id}` has disconnected.'}
    requests.post(webhook_url, data=payload)

atexit.register(send_disconnection_message)

while True:

    with mss.mss() as sct:
        # Get the current monitor's information
        monitor = sct.monitors[1]
        # Capture the screen
        screenshot = sct.grab(monitor)
        # Save the screen to a file in the temp folder
        temp_folder = tempfile.gettempdir()
        filename = os.path.join(temp_folder, f'{computer_name}_{time.time()}.png')
        mss.tools.to_png(screenshot.rgb, screenshot.size, output=filename)

    # Send the screenshot and computer name to Discord using webhook
    with open(filename, 'rb') as f:
        payload = {'content': f'**Computer name:** `{computer_name}`\n**Hardware ID CPU:** `{hardware_id}` \n**Timestamp:** `{date_str}`'}
        r = requests.post(webhook_url, data=payload, files={'file': f})
        print('Sending Actions')

    # Remove the screenshot file
    os.remove(filename)

    # Wait for 30 seconds before taking another screenshot
    time.sleep(30)


