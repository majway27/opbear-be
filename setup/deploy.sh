#!/bin/bash
# Set Envs
export TABLE_NAME="test.ob.lists"

source ~/environment/opbear-be/.env/bin/activate

#rm package.yaml
aws s3 cp swagger.json s3://opbearbe-deploy/

sam package --template-file template.yaml --s3-bucket opbearbe-deploy --output-template-file package.yaml

sam deploy --template-file package.yaml --stack-name OPBEAR --capabilities CAPABILITY_IAM
