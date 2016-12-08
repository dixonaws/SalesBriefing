#!/usr/bin/env bash

# create the Lambda deployment package -- just a zip file
zip SalesBriefing-deployment.zip SalesBriefing.py

# publish the code to Lambda (the function must already exist)
aws --profile dixonaws@amazon.com --region us-east-1 lambda update-function-code --function-name SalesBriefing --zip-file fileb://SalesBriefing-deployment.zip --publish

# publish the custom message and the walmart sales figures to my S3 bucket
aws --profile dixonaws@amazon.com s3 cp message.txt s3://salesbriefing-data/ --acl "public-read"
aws --profile dixonaws@amazon.com s3 cp walmart_salesFigures.txt s3://salesbriefing-data/ --acl "public-read"

