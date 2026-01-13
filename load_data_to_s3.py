import boto3
from dotenv import load_dotenv
import os
from datetime import datetime
from modules import make_logger, load_to_s3

#make timestamp for use in log file name
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

#set up logging
logger = make_logger(timestamp=timestamp)

#access environment variables for authentication with s3
load_dotenv()
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
bucket_name = os.getenv('bucket_name')

#connect to s3
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

#Identify directory with JSON files
json_data = 'json_data'

#loop through and upload all JSON files to s3, deleting the local copies
load_to_s3(json_dir=json_data, s3_client=s3_client, bucket_name=bucket_name, logger=logger)