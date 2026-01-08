import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import logging

#function to check if a directory exists; if not, make it
def mkdir_if_not_exists(path):
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)

#create directories for data and logs
data_dir = 'data'
logs_dir = 'logs'
mkdir_if_not_exists(data_dir)
mkdir_if_not_exists(logs_dir)

#load secrets
load_dotenv()
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')

#api information
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': '20260101T00',
    'end': '20260107T23'
}

#define retry logic and timestamp (used for output file names)
max_attempts = 3
attempts_made = 0
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

while attempts_made < 3:
    response = requests.get(url, params=params, auth=(AMP_API_KEY, AMP_SECRET_KEY))

    #check for successful download
    if response.status_code == 200:
        print('Download successful')
        file_path = f'{data_dir}/amplitude_events_{timestamp}.zip'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        break

    #check for server error
    elif response.status_code < 200 or response.status_code >= 500:
        print('Server error')
        print(response.reason)
        print('Retrying...')
        time.sleep(10)
        attempts_made += 1

    #check for non-server error
    else:
        print('Non-server error')
        print(response.reason)
        break