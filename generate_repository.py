import boto3
import os
import botocore
import datetime
import time
import re
import requests
from requests_aws4auth import AWS4Auth

## Global
host = "<https://endpoint-aws-es-service/>" # Endpoint to ElasticSearch Service
region = "<region>" # Region for your ElasticSearch Service
bucket = "<bucket_name>" # Name of the bucket where we save the snapshot
repository = "<bucket_repository>" # Repository name
role = "<role_arn>" # ARN role that allow to do the snapshot

# Auxiliar var
url = host + "_snapshot/" + repository

# Generate connection with services in AWS
service = "es" # Service ES
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Main
try:
  # Register repository if not exists
  if requests.get(url, auth=awsauth).status_code != 200:

    print("Repository doesn't exists. Creating...")

    while requests.get(url, auth=awsauth).status_code != 200:
      payload = {
        "type": "s3",
        "settings": {
          "bucket": bucket,
          "role_arn": role
        }
      }

      requests.put(url, auth=awsauth, json=payload, headers={"Content-Type": "application/json"})

    print("Repository created.")
  
  else:

    print("Repository exists.")

except botocore.exceptions.ClientError as Error:
  print(Error)