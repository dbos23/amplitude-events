import boto3
from dotenv import load_dotenv
import os
import logging
from datetime import datetime

#make timestamp for use in log file name
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
log_filepath = f'logs/logs_{timestamp}.log'

#set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filepath
)

logger = logging.getLogger()

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

#loop through and upload all JSON files to s3, deleting the local files
for root, dirs, files in os.walk(json_data):
    files = [file for file in files if file[-5:] == '.json'] #filter list to only JSON files
    if len(files) > 0:
        for file in files:
            filepath = os.path.join(root, file)
            print(f'Uploading {filepath}')
            logger.info(f'Uploading {filepath}')
            try:
                s3_client.upload_file(filepath, bucket_name, file)
                print('Upload successful')
                logger.info('Upload successful')
                os.remove(filepath)
                print(f'Local copy of {file} deleted')
                logger.info(f'Local copy of {file} deleted')
            except Exception as e:
                print(f'Error: {e}')
                logger.error(f'Error: {e}')
    else:
        print('No JSON files to upload')
        logger.info('No JSON files to upload')