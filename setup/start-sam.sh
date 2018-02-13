#!/bin/bash
# Set Envs
export TABLE_NAME="test.ob.lists"

source ~/environment/opbear-be/.env/bin/activate
sam local start-api
