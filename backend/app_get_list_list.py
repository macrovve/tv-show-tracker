import boto3
from boto3.dynamodb.conditions import Key

import json

def lambda_handler(event, context):
    # TODO implement
    email = event['email']
    response = db2_search(email)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": response,
            # "location": ip.text.replace("\n", "")
        }),
    }

def db2_search(email):
    result=[]

    email=email


    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    visitors = dynamodb.Table('project-user-list')

    response = visitors.query(
    KeyConditionExpression=Key('email').eq(email))
    for i in response['Items']:
        result +=  [int(i['list_id']),i['list_name']]
    return result

event={"email":"abc@qq.com"}
print(lambda_handler(event,'1'))