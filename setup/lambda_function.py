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
    if filter_key and filter_value:
        filtering_exp = Key(filter_key).eq(filter_value)
        response = table.query(KeyConditionExpression=filtering_exp)
        return response
    else: 
        print("Error: Missing Query Values") 
        return response_builder("Bad Robot", 400)

def query_table_item(userid, listid):
    if userid and listid:
        print("Getting item: " + str(listid))
        response = table.get_item(
                    Key={
                        'uid': userid,
                        'listid': listid
                    },
        )
        return response
    else: 
        print("Error: Missing Query Values") 
        return response_builder("Error: Missing Query Values", 400)

def lambda_handler(event, context):
    userid = event['requestContext']['authorizer']['claims']['sub']
    #print(userid)
    
    if event['httpMethod'] == 'GET':
        if (event['pathParameters'] is not None):
            # Get single list
            data = {}
            try:
                resp = query_table_item(userid,event['pathParameters']['listid'])
                data['uid'] = resp['Item']['uid']
                data['listid'] = resp['Item']['listid']
                data['name'] = resp['Item']['name']
                data['longDescription'] = resp['Item']['longDescription']
                data['status'] = resp['Item']['status']
                data['listitems'] = resp['Item']['listitems']
                return response_builder(json.dumps(data), 200)
            except Exception as e:
                print(e)
                return response_builder("Bad Robot", 400)
        else:
            # Get all lists for user
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
                    'uid': userid,
                    'listid': body['listid'],
                    'name': body['name'],
                    'longDescription': body['longDescription'],
                    'status': "active",
                    'listitems': body['listitems']
                }
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response_builder('[{"result":"success"}]', 200)

    elif event['httpMethod'] == 'DELETE':
        print(event['pathParameters']['listid'])
        try:
            response = table.delete_item(
                Key={
                    'uid': userid,
                    'listid': event['pathParameters']['listid']
                },
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response_builder('[{"result":"success"}]', 200)
            
    elif event['httpMethod'] == 'PUT':
        print(event)
        try:
            body = json.loads(event['body'])
        except:
            return {'statusCode': 400, 'body': 'malformed json input'}        
        try:
            response = table.update_item(
                Key={
                    'uid': userid,
                    'listid': event['pathParameters']['listid']
                },
                UpdateExpression="set #listname = :n, longDescription =:l, #liststatus =:s, listitems =:i",
                ExpressionAttributeNames = {"#listname":"name", "#liststatus":"status"},
                ExpressionAttributeValues={
                    ':n': body[0]['name'],
                    ':l': body[0]['longDescription'],
                    ':s': body[0]['status'],
                    ':i': body[0]['listitems']
                },
                ReturnValues="UPDATED_NEW"
            )
        except ClientError as e:
            print(e.response['Error']['Message'])
        else:
            return response_builder('[{"result":"success"}]', 200)