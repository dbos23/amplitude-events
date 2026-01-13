import os
import gzip
import shutil
from datetime import datetime
from modules import make_logger, unzip, decompress_gzips

#make timestamp for use in log file name
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

#set up logging
logger = make_logger(timestamp=timestamp)

#check if extracted_data and json_data directories exist; if not, create them
gzip_files = 'gzip_files'
json_data = 'json_data'
os.makedirs(gzip_files, exist_ok=True)
os.makedirs(json_data, exist_ok=True)

#Extract zip files, creating gzip files. Remaining zip files are deleted
zip_directory = 'zip_files'
unzip(zip_dir=zip_directory, gzip_dir=gzip_files, logger=logger)

print('Zip file(s) extracted')
print('Starting on gzip files')

#Extract gzips, outputting json files. The remaining gzip files are deleted
decompress_gzips(gzip_dir=gzip_files, output_dir=json_data, logger=logger)