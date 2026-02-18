import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import boto3
from modules import extract_amplitude_data, make_logger, unzip, decompress_gzips, load_to_s3

#create directories for data and logs if they don't already exist
logs_dir = 'logs'
zip_files = 'zip_files'
gzip_files = 'gzip_files'
json_data = 'json_data'

dirs = [logs_dir, zip_files, gzip_files, json_data]
for dir in dirs:
    os.makedirs(dir, exist_ok=True)

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
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
bucket_name = os.getenv('bucket_name')

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
    data_dir=zip_files,
    current_timestamp_str=current_timestamp_str
)

#Unzip zip files, outputting gzip files. Remaining zip files are deleted
unzip(
    zip_dir=zip_files,
    gzip_dir=gzip_files,
    logger=logger
)

print('Zip file(s) extracted')
print('Starting on gzip files')

#Unzip gzip files, outputting json files. Remaining gzip files are deleted
decompress_gzips(
    gzip_dir=gzip_files,
    output_dir=json_data,
    logger=logger
)

#connect to s3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

#loop through and upload all JSON files to s3, deleting the local copies
load_to_s3(
    json_dir=json_data,
    s3_client=s3_client,
    bucket_name=bucket_name,
    logger=logger
)