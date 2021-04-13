import boto3
import os
import botocore
import datetime
import time
import re
import requests
from requests_aws4auth import AWS4Auth

## Global
host = os.environ["host"] # Endpoint to ElasticSearch Service
region = os.environ["region"] # Region for your ElasticSearch Service
bucket = os.environ["bucket"] # Name of the bucket where we save the snapshot
repository = os.environ["repository"] # Repository name
role = os.environ["role"] # ARN role that allow to do the snapshot
today = datetime.datetime.now() # The name of the snapshot, with format yyyy.mm.dd

# Auxiliar var
url = host + "_snapshot/" + repository

# Generate connection with services in AWS
service = "es" # Service ES
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Main
def main(event, context):
  try:
    # Register repository if not exists
    if not re.search(repository, requests.get(host + "_cat/repositories", auth=awsauth).text):

      print("Repository doesn't exists. Creating...")

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

      # Register snapshot if not exists. If exists, then show error a list it
      print("Repository exists. Verifying if the snapshot exists or not...")
    
      if requests.get(url + "/" + today.strftime("%Y.%m.%d"), auth=awsauth).status_code == 404:     
        print("Snapshot doesn't exists. Creating and registering...")
        requests.put(url + "/" + today.strftime("%Y.%m.%d"), auth=awsauth)

        # Waiting for SUCCESS state
        while requests.get(host + "_snapshot/" + repository + "/" + today.strftime("%Y.%m.%d"), auth=awsauth).json()["snapshots"][0]["state"] == "IN_PROGRESS":
          print("Waiting for backup...")
          time.sleep(30)

        if requests.get(host + "_snapshot/" + repository + "/" + today.strftime("%Y.%m.%d"), auth=awsauth).json()["snapshots"][0]["state"] == "SUCCESS":
          print("Backup finished successfully!!!")
          print(requests.get(host + "_snapshot/" + repository + "/" + today.strftime("%Y.%m.%d") + "?pretty", auth=awsauth).text)
          
        else:
          print("Something have happened with the backup. Please, review your logs.")
          print(requests.get(host + "_snapshot/" + repository + "/" + today.strftime("%Y.%m.%d") + "?pretty", auth=awsauth).text)
      
      else:
        print("Exists a backup for today " + today.strftime("%Y.%m.%d"))
        print(requests.get(host + "_snapshot/" + repository + "/" + today.strftime("%Y.%m.%d") + "?pretty", auth=awsauth).text)

  except botocore.exceptions.ClientError as Error:
    print(Error)