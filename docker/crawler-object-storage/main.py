import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
import boto3
from botocore.exceptions import ClientError

# Base Variables
FILE_URL = "https://storage.googleapis.com/challenge_junior/categoria.parquet"
BUCKET_NAME = os.environ.get("RAW_BUCKET")

# S3 Client
s3 = boto3.client('s3')

def download_file(url):
    """
    Fetch file from specified URL
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error: {e}")
        return None

def upload_to_s3(file_content, bucket, key):
    """
    Upload file content to S3.
    """
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=file_content)
        print(f"File upload with success {bucket}/{key}")
    except ClientError as e:
        print(f"Error: {e}")

def main():
    if not BUCKET_NAME:
        raise ValueError("RAW_BUCKET environment variable is not set")

    print(f"Downloading file {FILE_URL}")
    file_content = download_file(FILE_URL)
    key = None
    if file_content:
        print("File dowloaded with success. Sending to S3...")
        key = f"files/gcs/date={date.today()}/categoria.parquet"
        upload_to_s3(file_content, BUCKET_NAME, key)
    else:
        print("Error while fetching file.")

    return f"s3a://{BUCKET_NAME}/{key}"

if __name__ == "__main__":
    main()
