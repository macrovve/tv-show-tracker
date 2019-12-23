# project-update-history
import json

# import requests
import boto3
import time
import datetime
import trakt
import trakt.tv
def connect_trakt():

    trakt.core.OAUTH_TOKEN = "2d54930af74ab77d3152e214777501c4d75128194de3da07847df376c15f0b52"
    trakt.core.CLIENT_ID = "6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32"
    trakt.core.CLIENT_SECRET = "fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b"

def get_movie_id(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['trakt']
        # response = trakt.movies.Movie(name)
    except(trakt.errors.NotFoundException):
        response = 0
    return response

def get_movie_id_tmdb(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['tmdb']
        # response = trakt.movies.Movie(name)
    except(trakt.errors.NotFoundException):
        response = 0
    return response

# email,  season, eposides
def db1_insert(email, movie_name, season, eposides,movie_id):
    email = email
    ttl = get_timestamp()
    s_e = str(movie_id)+"_"+season+"_"+eposides

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    passcodes = dynamodb.Table('project-history')
    # print(passcodes.creation_date_time)

    passcodes.put_item(Item={
        'email': email,
        's_e': (s_e),
        'movie_name':movie_name,
        "ttl": ttl
    })

    return ("insert")

def get_timestamp():
    now = int(round(time.time() * 1000))
    now02 = time.strftime('%Y-%m-%d', time.localtime(now / 1000))
    # print(now)
    return now02

# def add_watchlist(name):
#     try:
#         trakt.tv.TVShow(name).add_to_watchlist()
#     except(trakt.errors.NotFoundException):
#         print("trakt.errors.NotFoundException")

def lambda_handler(event, context):
    connect_trakt()
    event = event
    email = event['email']
    movie_name = event['movie_name']
    movie_id = get_movie_id_tmdb(movie_name)
    season = str(event['season'])
    eposides = str(event['eposides'])
    print(movie_id)
    if(movie_id == 0):
        response = "no movie id records"
    else:

        response = db1_insert(email, movie_name, season, eposides, movie_id)

    print(response)
    # add_watchlist(movie_name)
    return json.dumps({
        "statusCode": 200,
        "body": {
            "message": response,
            # "location": ip.text.replace("\n", "")
        },
    })
#
event={"email":"abc@qq.com", "movie_name":"Game of Thrones","season":2,"eposides":1}
print(lambda_handler(event, "1"))

