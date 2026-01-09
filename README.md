# Amplitude API Export

This is a project that downloads web traffic data from [Amplitude’s Export API](https://amplitude.com/docs/apis/analytics/export) and writes it to a file. The project is built around a Python script and uses a local virtual environment.
​

## Project layout

`extract_events.py` – The main script in the project. It exports the data and writes it to a file

`unzip_files.py` - Unzips the file output by extract_events.py

`functions.py` - Contains functions referenced in the other Python scripts

`.venv/` – Local virtual environment with all installed Python packages

`data/` – Destination folder where Amplitude .zip exports are

`extracted_data/` - The folder where the gzip files are written

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
   ```

4. Run the Python script to download the data

   ```bash
   python extract_events.py
   ```

5. Run the Python script to extract the data

   ```bash
   python unzip_files.py
   ```

## What it does:

- Ensures data/ and logs/ directories exist

- Downloads web traffic data from a 7 day period of time up to and including the current date

- Calls the Amplitude Export API with your keys

- Saves a .zip file in data/ and logs status in logs/

- Extracts the zip files and its nested gzip files

- Retries the download up to 3 times in the event of an error with the Amplitude API's server
