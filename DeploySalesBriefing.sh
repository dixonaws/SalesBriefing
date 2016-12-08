#!/usr/bin/env bash

# create the Lambda deployment package -- just a zip file
zip SalesBriefing-deployment.zip SalesBriefing.py

# publish the code to Lambda (the function must already exist)
aws --profile dixonaws@amazon.com --region us-east-1 lambda update-function-code --function-name SalesBriefing --zip-file fileb://SalesBriefing-deployment.zip --publish
