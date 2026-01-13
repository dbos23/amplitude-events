import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from modules import extract_amplitude_data, make_logger

#create directories for data and logs if they don't already exist
data_dir = 'zip_files'
logs_dir = 'logs'
os.makedirs(data_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)

#create timestamps (used for file names and api call)
current_timestamp = datetime.now()
prior_day_timestamp = current_timestamp - timedelta(days=1)

current_timestamp_str = current_timestamp.strftime('%Y-%m-%d_%H-%M-%S')
prior_day_timestamp_str = prior_day_timestamp.strftime('%Y-%m-%d_%H-%M-%S')

request_start = f'{prior_day_timestamp_str.replace('-', '')[:8]}T00'
request_end = f'{prior_day_timestamp_str.replace('-', '')[:8]}T23'

#set up logging
logger = make_logger(timestamp=current_timestamp_str)

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

#extract data, implementing retry logic and logging the outcome
extract_amplitude_data(
    max_attempts=max_attempts,
    url=url,
    params=params,
    API_KEY=AMP_API_KEY,
    SECRET_KEY=AMP_SECRET_KEY,
    logger=logger,
    data_dir=data_dir,
    current_timestamp_str=current_timestamp_str
)