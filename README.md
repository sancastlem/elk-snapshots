# ELK Snapshots
Lambda function that do backup from your ELK indexes.

## Use

1. Zip the file generate_snapshot.py.

```bash

zip your_script_zip_name.zip generate_snapshot.py

```
2. Install the requirements to launch correctly the function. **Path is necessary**.

```bash

pip3 install -r requirements.txt -t python/lib/python3.8/site-packages/

```
3. Zip the folder with contains every libraries.

```bash

zip -r your_layer_zip_name.zip python

```

4. Create the layer, uploading the zip generated previously.

5. Create the lambda function, upload the zip generate previously.

You need to setup this options:

### Global Environments

- **host**: the url of your ElasticSearch Service, with this format: *https://your_es_url/*
- **region**: region where you've created your ElasticSearch Service. Need it to AWS credentials request.
- **bucket**: the name of the bucket where you've saved the snapshots.
- **repository**: the name of the repository where you've saved the snapshots. You can insert any name that you want, at less that you've created a repository before, then insert its name. If you've inserted another name, then this function will create a new repository.
- **role**: arn from role that have permission to put snapshot in your bucket S3.

### AWS Cloudwatch Event Bridge

For cron, you need to create a cron job, employing the service AWS Cloudwatch Event Bridge.

### Basic setup

- Change the name of the controller to **generate_snapshot.main**.
- Change timeout to 300 or upper, depends the size of your kibana indexes.

### Permissions and role

Make sure that your role have access to bucket S3, Cloudwatch for logging the launch and ES Service, and your lambda function has the permissions to launch the function.

### Runtime

Python 3.8.

6. Deploy, break and fun!

