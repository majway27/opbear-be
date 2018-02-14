# Version 1.2

import decimal
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import os
import uuid


dynamodb = boto3.resource("dynamodb", region_name='us-west-2')
table = dynamodb.Table(os.getenv('TABLE_NAME'))

def response_builder(message, status_code):  
    return {
        'statusCode': str(status_code),
        'body': message,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
    }
    
def query_table(filter_key=None, filter_value=None):
    """
    Perform a query operation on the table. Can specify filter_key (col name) and its value to be filtered. Returns the response.
    """
    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.query(KeyConditionExpression=filtering_exp)
        return response
    else: print("oops") 
    #return response_builder("Bad Robot", 400)

def lambda_handler(event, context):
    userid = event['requestContext']['authorizer']['claims']['sub']
    #print(userid)
    
    if event['httpMethod'] == 'GET':
        response_list = []
        response_json = ""
        try:
            resp = query_table("uid",userid)
            
            for item in resp['Items']:
                data = {}
                data["uid"] = item["uid"]
                data['listid'] = str(item['listid'])
                data['name'] = item['name']
                data['longDescription'] = item['longDescription']
                data['status'] = item['status']
                response_list.append(data)
            json_data = json.dumps(response_list)
            return response_builder(json_data, 200)
        except Exception as e:
            print(e)
            return response_builder("Bad Robot", 400)
    
    elif event['httpMethod'] == 'POST':
        try:
            body = json.loads(event['body'])
        except:
            return {'statusCode': 400, 'body': 'malformed json input'}
        try:
            response = table.put_item(
                Item={
                    #'uid': 'bad0b9bb-6af8-4abc-b5ba-1a323733ee45',
                    'uid': userid,
                    'listid': str(uuid.uuid4()),
                    'name': body['name'],
                    'longDescription': body['longDescription'],
                    'status': "active"
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response_builder('[{"result":"success"}]', 200)
