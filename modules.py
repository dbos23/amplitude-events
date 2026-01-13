import requests
import time
import logging
from zipfile import ZipFile
import os
import gzip
import shutil



def make_logger(timestamp):
    '''
    Creates a logger, using a timestamp as a suffix to make the file name unique
    '''
    log_filepath = f'logs/logs_{timestamp}.log'

    #set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_filepath
    )
    return logging.getLogger()



def extract_amplitude_data(max_attempts, url, params, API_KEY, SECRET_KEY, logger, data_dir, current_timestamp_str):
    '''
    Extracts data from Amplitude, writing it to a zip file, handling errors, and logging the outcome
    '''
    attempts_made = 0
    while attempts_made < max_attempts:
        response = requests.get(url, params=params, auth=(API_KEY, SECRET_KEY))

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



def unzip(zip_dir, gzip_dir, logger):
    '''
    Extracts zip files from a given directory, outputting gzip files and then deleting the zip files
    '''
    #Iterate through zip files, extracting one by one
    for name in os.listdir(zip_dir):
        file_path = os.path.join(zip_dir, name)
        if file_path[-4:] == '.zip':
            print(f'Unzipping {name}:')
            try:
                with ZipFile(file_path) as zObject:
                    zObject.extractall(path=gzip_dir)
                print(f'{name} successfully extracted')
                logger.info(f'{name} successfully extracted')
                os.remove(file_path)
                print(f'{name} deleted')
                logger.info(f'{name} deleted')
            except Exception as e:
                print(f'Error: {e}')
                logger.error(f'Error: {e}')



def decompress_gzips(gzip_dir, output_dir, logger):
    '''
    Iterates through the created directories, extracting contained gzip files one by one. They're then deleted once they've been extracted
    '''
    for name in os.listdir(gzip_dir):
        dir_path = os.path.join(gzip_dir, name)

        #If it's a directory, loop through it
        if os.path.isdir(dir_path):
            for root, _, files in os.walk(dir_path):
                
                #Check if each file is a gzip; if yes, extract it
                for file in files:
                    if file.endswith('.gz'):
                        gz_path = os.path.join(root, file)
                        json_filename = file[:-3]  # remove .gz extension
                        output_path = os.path.join(output_dir, json_filename)
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




def load_to_s3(json_dir, s3_client, bucket_name, logger):
    '''
    Loops through and uploads all JSON files to s3, deleting the local files
    '''
    for root, dirs, files in os.walk(json_dir):
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