# Amplitude API Export

This is a project that downloads web traffic data from [Amplitude’s Export API](https://amplitude.com/docs/apis/analytics/export) and writes it to a zip file. It then extracts that file and the contained gzip files and outputs the resulting JSON files to Amazon S3. The project is built in Python and uses a local virtual environment.
​

## Project layout

`extract_events.py` – The main script in the project. It exports the data and writes it to a file

`unzip_files.py` - Unzips the file output by extract_events.py

`load_data_to_s3.py` - Loads the resulting JSON files output by unzip_files.py to Amazon S3

`functions.py` - Contains functions referenced in the other Python scripts

`.venv/` – Local virtual environment with all installed Python packages

`zip_files/` – The folder where the downloaded zip files are output

`gzip_files/` - The folder where the gzip files are written after extracting the zip files

`json_data/` - The folder where the final JSON files are written after all the extraction

`logs/` – Folder where timestamped log files are written

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file in the project root:

   ```text
   AMP_API_KEY = your_amplitude_api_key
   AMP_SECRET_KEY = your_amplitude_secret_key
   AWS_ACCESS_KEY = your_aws_access_key
   AWS_SECRET_KEY = your_aws_secret_key
   bucket_name = your_aws_bucket_name
   ```

4. Run the Python script to download the data

   ```bash
   python extract_events.py
   ```

5. Run the Python script to extract the data

   ```bash
   python unzip_files.py
   ```

6. Run the Python script to upload the data to S3

   ```bash
   python load_data_to_s3.py
   ```

## What it does:

- Ensures zip_files, gzip_files, json_data, and logs directories exist

- Downloads web traffic data from the day before the extract script is run

- Calls the Amplitude Export API with your keys

- Saves a zip file of data and logs status

- Extracts the zip file and its nested gzip files to JSON files stored in json_data

- Loads the JSON files to S3

- Deletes local copies of files once they've successfully been extracted/uploaded

- Retries the download up to 3 times in the event of an error with the Amplitude API's server
