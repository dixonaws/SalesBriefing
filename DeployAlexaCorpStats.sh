#!/usr/bin/env bash

# create the Lambda deployment package -- just a zip file
zip AlexaCorpStats-deployment.zip AlexaCorpStats.py

# publish the code to Lambda (the function must already exist)
aws --profile dixonaws@amazon.com --region us-east-1 lambda update-function-code --function-name AlexaCorpStats --zip-file fileb://AlexaCorpStats-deployment.zip --publish
