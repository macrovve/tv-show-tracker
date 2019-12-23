# project-delete-from-list
import json
from boto3.dynamodb.conditions import Key
# import requests
import boto3
import time
import datetime
import trakt.tv

# project - update - list
def get_movie_id(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['trakt']
        # response = trakt.movies.Movie(name)
    except(trakt.errors.ForbiddenException):
        response = 0
    return response

def get_list_id(list_name, email):
    result = []
    list_name = list_name

    email = email

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    visitors = dynamodb.Table('project-user-list')

    response = visitors.query(
        KeyConditionExpression=Key('email').eq(email) )
    for i in response['Items']:
        if(i['list_name'] == list_name):
            result =int(i['list_id'])
    return result
def db1_delete(list_id,movie_id):
    list_id = list_id
    movie_id = movie_id

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('project-list-content')
    # print(passcodes.creation_date_time)

    table.delete_item(
        Key={
            'list_id': int(list_id),
            'movie_id': int(movie_id)
        }
    )

    return ("delete")



def lambda_handler(event, context):
    event = event
    list_id = event['list_id']

    movie_id = event['movie_id']

    response = db1_delete(list_id, movie_id)



    print(response)
    return json.dumps({
        "statusCode": 200,
        "body": {
            "message": response
        }
    })

event={"list_id":1576902047113,"movie_id":1399}
print(lambda_handler(event, "1"))

# print(get_list_id("my love", "abc@qq.com"))