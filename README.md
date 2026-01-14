# Amplitude API Export

This is a project that downloads web traffic data from [Amplitude’s Export API](https://amplitude.com/docs/apis/analytics/export) and writes it to a zip file. It then extracts that file and the contained gzip files and outputs the resulting JSON files to Amazon S3. The project is built in Python and uses a local virtual environment.
​g

## Project layout

`main.py` - Exports the data from the API and writes it to a zip file. Then it unzips that file and the contained gzip files. Finally, it loads the resulting JSON files to a bucket in Amazon S3

`modules.py` - Contains functions referenced in the other Python scripts

`zip_files/` – The folder where the downloaded zip files are output

`gzip_files/` - The folder where the gzip files are written after extracting the zip files

`json_data/` - The folder where the final JSON files are written after all the extraction

`logs/` – Folder where timestamped log files are written

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a .env file in the project root:

   ```text
   AMP_API_KEY = '{{ your_amplitude_api_key }}'
   AMP_SECRET_KEY = '{{ your_amplitude_secret_key }}'
   AWS_ACCESS_KEY = '{{ your_aws_access_key }}'
   AWS_SECRET_KEY = '{{ your_aws_secret_key }}'
   bucket_name = '{{ your_aws_bucket_name }}'
   ```

4. Run the Python script to download, unzip, and load the data

   ```bash
   python main.py
   ```

## What it does:

- Ensures zip_files, gzip_files, json_data, and logs directories exist

- Downloads web traffic data from the day before the extract script is run

- Calls the Amplitude Export API with your keys

- Saves a zip file of data and logs status

- Extracts the zip file and its nested gzip files to JSON files stored in json_data

- Loads the JSON files to S3

- Deletes local copies of files once they've successfully been unzipped/uploaded

- Retries the download up to 3 times in the event of an error with the Amplitude API's server
