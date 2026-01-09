import os
from zipfile import ZipFile
from functions import mkdir_if_not_exists

#check if extracted_data directory exists; if not, create it
mkdir_if_not_exists('extracted_data')

# Identify directory containing zip files
directory = 'data'

# Iterate over files in directory
for name in os.listdir(directory):
    file_path = os.path.join(directory, name)
    if os.path.isfile(file_path):
        print(f'Unzipping {name}:')
        with ZipFile(file_path) as zObject:
            zObject.extractall(path='extracted_data')
        print(f'{name} successfully extracted')