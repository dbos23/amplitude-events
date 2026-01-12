import os
from zipfile import ZipFile
import gzip
from functions import mkdir_if_not_exists
import shutil

#check if extracted_data and json_data directories exist; if not, create them
extracted_data = 'extracted_data'
json_data = 'json_data'
mkdir_if_not_exists(extracted_data)
mkdir_if_not_exists(json_data)

# Identify directory containing zip files
zip_directory = 'data'

#Iterate through zip files, extracting one by one
for name in os.listdir(zip_directory):
    file_path = os.path.join(zip_directory, name)
    if file_path[-4:] == '.zip':
        print(f'Unzipping {name}:')
        with ZipFile(file_path) as zObject:
            zObject.extractall(path=extracted_data)
        print(f'{name} successfully extracted')

print('Zip file(s) extracted')
print('Starting on gzip files')

#Identify directory containing gzip files
gzip_directory = 'extracted_data'

#Iterate through the created directories, extracting contained gzip files one by one
for name in os.listdir(gzip_directory):
    dir_path = os.path.join(gzip_directory, name)

    #If it's a directory, loop through it
    if os.path.isdir(dir_path):
        for root, _, files in os.walk(dir_path):
            
            #Check if each file is a gzip; if yes, extract it
            for file in files:
                if file.endswith('.gz'):
                    gz_path = os.path.join(root, file)
                    json_filename = file[:-3]  # Remove .gz extension
                    output_path = os.path.join(json_data, json_filename)

                    with gzip.open(gz_path, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                        shutil.copyfileobj(gz_file, out_file)