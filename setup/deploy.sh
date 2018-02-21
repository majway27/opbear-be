#!/bin/bash
# Set Envs
export TEST_SETUP_TABLE_NAME="test.2.ob.lists"
export PROD_SETUP_TABLE_NAME="prod.2.ob.lists"
export DEPLOY_BUCKET="opbearbe-deploy"
export PROD_LAMBDA_VERSION="95"  # String Type

# Note
# Environment Variable Management for Lambda
## Deployed versions are immutable, including Envvars
## $Latest/current version can have envars changed via cli update-function-configuration
## Current approach is to deploy with prod values.  Then override/set $LATEST at end of deploy script.
## This solves for being able to point the PROD alias at any past version and not have to worry about overriding an immutable envvar.
## 

source ~/environment/opbear-be/.env/bin/activate

#rm package.yaml
aws s3 cp swagger.json s3://opbearbe-deploy/

sam package --template-file template.yaml --s3-bucket opbearbe-deploy --output-template-file package.yaml

sam deploy --template-file package.yaml --stack-name OPBEAR --capabilities CAPABILITY_IAM --parameter-overrides LambdaFunctionProdVersionValue=$PROD_LAMBDA_VERSION

aws lambda update-function-configuration --function-name setuplambda --environment '{"Variables":{"TABLE_NAME":"'$TEST_SETUP_TABLE_NAME'", "DeployBucket":"'$DEPLOY_BUCKET'"}}'