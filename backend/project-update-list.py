# project-update-list
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
def db1_insert(list_id,movie_name, movie_id, season, eposides):
    list_id = list_id
    movie_id = movie_id

    movie_name = movie_name
    season = season
    eposides = eposides
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    passcodes = dynamodb.Table('project-list-content')
    # print(passcodes.creation_date_time)

    passcodes.put_item(Item={
        'list_id': list_id,
        'movie_id': int(movie_id),
        'movie_name':movie_name,
        'season':season,
        "eposides":eposides


    })

    return ("insert")


def get_timestamp():
    now = int(round(time.time() * 1000))
    now02 = time.strftime('%Y-%m-%d', time.localtime(now / 1000))
    # print(now)
    return now


def lambda_handler(event, context):
    connect_trakt()
    event = event
    list_name = event['list_name']
    email = event['email']
    movie_name = event['movie_name']
    season = event['season']
    eposides=event['eposides']
    movie_id = int(get_movie_id_tmdb(movie_name))
    print(movie_id)
    list_id=get_list_id(list_name, email)

    if(movie_id == 0):
        response = "no movie id records"
    if (list_id == []):
        response = "no movie id records"

    else:
        response = db1_insert(list_id, movie_name,movie_id , season, eposides)

    print(response)
    return json.dumps({
        "statusCode": 200,
        "body": {
            "message": response
        },
    })

def get_movie_id_tmdb(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['tmdb']
        # response = trakt.movies.Movie(name)
    except(trakt.errors.NotFoundException):
        response = 0
    return response


def connect_trakt():
    trakt.core.OAUTH_TOKEN = "2d54930af74ab77d3152e214777501c4d75128194de3da07847df376c15f0b52"
    trakt.core.CLIENT_ID = "6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32"
    trakt.core.CLIENT_SECRET = "fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b"
#
event={"email":"abc@qq.com","list_name":"my love 1", "movie_name":"Game of Thrones","season":1, "eposides":2}
print(lambda_handler(event, "1"))

# print(get_list_id("my love", "abc@qq.com"))
# print(get_movie_id_tmdb("Game of Thrones"))