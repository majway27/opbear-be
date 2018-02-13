# Version 1.2

import os
import json
import boto3
import decimal
from botocore.exceptions import ClientError
#lists_table = boto3.resource('dynamodb').Table(os.getenv('TABLE_NAME'))
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

def lambda_handler(event, context):
    #print(event)
    
    if event['httpMethod'] == 'GET':
        response_list = []
        response_json = ""
        try:
            resp = table.scan()
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
                    #'uid': '94776f82-5d24-4c24-b042-a1e1690d2290',
                    #'listid': 2,
                    #'name' : 'My List'
                    'uid': body['uid'],
                    'listid': int(body['listid']),
                    'name': body['name']
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            #print("PutItem Succeeded")
            return {'statusCode': 200, 'body': 'List Added'}
