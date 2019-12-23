import json
import boto3

from boto3.dynamodb.conditions import Key, Attr
import time


def db1_insert(email,list_name):

    email = email
    list_name = list_name



    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    passcodes = dynamodb.Table('project-user-list')
    current_count = get_timestamp()


    passcodes.put_item(Item={
        'email': email,
        'list_name': list_name,
        'list_id': current_count
        })

    return ("insert")

def lambda_handler(event, context):
    # TODO implement
    email = event['email']
    list_name = event['list_name']
    response = db1_insert(email, list_name)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": response,
            # "location": ip.text.replace("\n", "")
        }),
    }


def get_timestamp():
    now = int(round(time.time() * 1000))
    now02 = time.strftime('%Y-%m-%d', time.localtime(now / 1000))
    # print(now)
    return now

#
# event={"email" : "abc@qq.com", "list_name" : "my love 2"}
event = {"email":"abc@qq.com","list_name":"my love 1"}
print(lambda_handler(event,'1'))