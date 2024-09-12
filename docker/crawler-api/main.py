import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
import boto3

# Base Variables
API_BASE_URL = "https://us-central1-bix-tecnologia-prd.cloudfunctions.net/api_challenge_junior"
MAX_WORKERS = 3  # Number of workers
BUCKET_NAME = os.environ.get("RAW_BUCKET")

# S3 Client
s3 = boto3.client('s3')

def fetch_data_from_api(id):
    """Fetch data from API for a given ID."""
    url = f"{API_BASE_URL}?id={id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return id, response.content.decode()
    except requests.RequestException as e:
        print(f"Error fetching data for ID {id}: {str(e)}")
        return id, None

def save_to_s3(data):
    """Save data to S3 bucket."""

    if data is None:
        return

    today = date.today().isoformat()
    key = f"api/date={today}/users.json"

    file_name = "users.json"
    tmp_file_path = f"/tmp/{file_name}"
    with open(tmp_file_path, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False)
    try:
        s3.upload_file(tmp_file_path, BUCKET_NAME, key)
        print(f"Successfully saved data from {today} extraction.")
    except Exception as e:
        print(f"Error saving data: {str(e)}")
    return f"s3a://{BUCKET_NAME}/{key}"

def main():
    # Check if env variables are set up
    if not BUCKET_NAME:
        raise ValueError("BUCKET_NAME environment variable is not set")

    # Id list and empty data var
    ids = range(1, 10)
    all_data = []
    file_path = None

    # Using ThreadPoolExecutor to parallelize requests
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit task
        future_to_id = {executor.submit(fetch_data_from_api, id): id for id in ids}

        # Process concluded tasks
        for future in as_completed(future_to_id):
            id, data = future.result()
            if data:
                all_data.append({"id": id, "nome": data})
    if all_data:
        file_path = save_to_s3(all_data)
    else:
        print("No data was fetched from the API")

    return file_path

if __name__ == "__main__":
    main()
