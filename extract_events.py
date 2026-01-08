import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
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

#create timestamps (used for file names and api call)
end_timestamp = datetime.now()
start_timestamp = end_timestamp - timedelta(days=7)

end_timestamp_str = end_timestamp.strftime('%Y-%m-%d_%H-%M-%S')
start_timestamp_str = start_timestamp.strftime('%Y-%m-%d_%H-%M-%S')

request_end = f'{end_timestamp_str.replace('-', '')[:8]}T23'
request_start = f'{start_timestamp_str.replace('-', '')[:8]}T00'

#set up logging
logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s',
    filename = f'{logs_dir}/logs_{end_timestamp_str}.py'
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
        print('download successful')
        logger.info('download successful')
        file_path = f'{data_dir}/amplitude_events_{end_timestamp_str}.zip'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        break

    #check for server error
    elif response.status_code < 200 or response.status_code >= 500:
        print(f'server error')
        logger.warning('server error')
        print(response.reason)
        logger.warning(response.reason)
        print('Retrying...')
        time.sleep(10)
        attempts_made += 1

    #check for non-server error
    else:
        print('non-server error')
        logger.error('non-server error')
        print(response.reason)
        logger.error(response.reason)
        break