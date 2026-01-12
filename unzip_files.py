import os
from zipfile import ZipFile
import gzip
from functions import mkdir_if_not_exists
import shutil
from datetime import datetime
import logging

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

#check if extracted_data and json_data directories exist; if not, create them
gzip_files = 'gzip_files'
json_data = 'json_data'
mkdir_if_not_exists(gzip_files)
mkdir_if_not_exists(json_data)

# Identify directory containing zip files
zip_directory = 'zip_files'

#Iterate through zip files, extracting one by one
for name in os.listdir(zip_directory):
    file_path = os.path.join(zip_directory, name)
    if file_path[-4:] == '.zip':
        print(f'Unzipping {name}:')
        try:
            with ZipFile(file_path) as zObject:
                zObject.extractall(path=gzip_files)
            print(f'{name} successfully extracted')
            logger.info(f'{name} successfully extracted')
            os.remove(file_path)
            print(f'{name} deleted')
            logger.info(f'{name} deleted')
        except Exception as e:
            print(f'Error: {e}')
            logger.error(f'Error: {e}')

print('Zip file(s) extracted')
print('Starting on gzip files')

#Iterate through the created directories, extracting contained gzip files one by one
for name in os.listdir(gzip_files):
    dir_path = os.path.join(gzip_files, name)

    #If it's a directory, loop through it
    if os.path.isdir(dir_path):
        for root, _, files in os.walk(dir_path):
            
            #Check if each file is a gzip; if yes, extract it
            for file in files:
                if file.endswith('.gz'):
                    gz_path = os.path.join(root, file)
                    json_filename = file[:-3]  # remove .gz extension
                    output_path = os.path.join(json_data, json_filename)
                    try:
                        with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                            shutil.copyfileobj(gz_file, out_file)
                        print(f'{file} successfully extracted')
                        logger.info(f'{file} successfully extracted')
                        os.remove(gz_path)
                        print(f'{file} deleted')
                        logger.info(f'{file} deleted')
                    except Exception as e:
                        print(f'Error: {e}')
                        logger.error(f'Error: {e}')