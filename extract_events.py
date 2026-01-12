import requests
import os
from functions import mkdir_if_not_exists
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
import logging

#create directories for data and logs
data_dir = 'zip_files'
logs_dir = 'logs'
mkdir_if_not_exists(data_dir)
mkdir_if_not_exists(logs_dir)

#create timestamps (used for file names and api call)
current_timestamp = datetime.now()
prior_day_timestamp = current_timestamp - timedelta(days=1)

current_timestamp_str = current_timestamp.strftime('%Y-%m-%d_%H-%M-%S')
prior_day_timestamp_str = prior_day_timestamp.strftime('%Y-%m-%d_%H-%M-%S')

request_start = f'{prior_day_timestamp_str.replace('-', '')[:8]}T00'
request_end = f'{prior_day_timestamp_str.replace('-', '')[:8]}T23'

#set up logging
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    filename = f'{logs_dir}/logs_{current_timestamp_str}.log'
)

logger = logging.getLogger()

#load secrets
load_dotenv()
AMP_API_KEY = os.getenv('AMP_API_KEY')
AMP_SECRET_KEY = os.getenv('AMP_SECRET_KEY')

#api information
url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': request_start,
    'end': request_end
}

#define retry logic
max_attempts = 3
attempts_made = 0

while attempts_made < 3:
    response = requests.get(url, params=params, auth=(AMP_API_KEY, AMP_SECRET_KEY))
    request_number = attempts_made + 1

    #check for successful download
    if response.status_code == 200:
        print('Download successful')
        logger.info('Download successful')
        file_path = f'{data_dir}/amplitude_events_{current_timestamp_str}.zip'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f'File written successfully to {file_path}')
        break

    #check for server error
    elif response.status_code < 200 or response.status_code >= 500:
        print('Server error')
        logger.warning('Server error')
        print(response.reason)
        logger.warning(response.reason)
        print('Retrying...')
        time.sleep(10)
        attempts_made += 1

    #check for non-server error
    else:
        print('Non-server error. Terminating script')
        logger.error('Non-server error. Terminating script')
        print(response.reason)
        logger.error(response.reason)
        break