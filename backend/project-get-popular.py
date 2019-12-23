import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import boto3
# import requests
import trakt
import trakt.tv

# from trakt.tv import popular_shows
def get_movie_id(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['trakt']
        # response = trakt.movies.Movie(name)
    except(trakt.errors.NotFoundException):
        response = 0
    return response


def get_show_name(people_name):
    # show_name = "Sesame Street"
    # episode_name = "<TVEpisode>: Sesame Street S50E11 The Great Fruit Strike"
    #    Sesame Street
    people_name=str(people_name)
    after_sp = people_name.split('<TVShow> ')
    episode_name=(after_sp[len(after_sp) - 1])
    return episode_name
def get_from_api():
    shows_name = trakt.tv.popular_shows()
    # print(shows_name)

    result=[]
    for show_name in shows_name:
        show_name_1 = get_show_name(show_name)
        result.append(show_name_1)
    return result

def connect_trakt():
    trakt.core.OAUTH_TOKEN = "2d54930af74ab77d3152e214777501c4d75128194de3da07847df376c15f0b52"
    trakt.core.CLIENT_ID = "6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32"
    trakt.core.CLIENT_SECRET = "fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b"
def db2_search(movie_id):
    result=[]

    movie_id=movie_id
    dynamodb = boto3.resource('dynamodb')

    visitors = dynamodb.Table('project-info')
    response = visitors.query(
    KeyConditionExpression=Key('movie_id').eq(movie_id))
    for i in response['Items']:
        result +=  [i['movie_id']],[i['movie_name']],[i['cast']],[i['images']],[i['genres']],[['overview']],[i['rate']]

    return result

def lambda_handler(event, context):
    connect_trakt()

    try:
        response = get_from_api()

    except(trakt.errors.NotFoundException):
        response="trakt.errors.NotFoundException : cannot get information of this movie/show"



    return json.dumps({
        "statusCode": 200,
        "body": {
            "message": (response),
            # "location": ip.text.replace("\n", "")
        }
    })
# connect_trakt()
# print(get_from_api("Sesame Street"))
# event={"name":"Ad Astra"}
event={}

print(lambda_handler(event, '1'))
# zip -g function.zip app_rate.py
# aws lambda update-function-code --function-name project-rate --zip-file fileb://function.zip
# connect_trakt()
# print(get_recommend_tv())
# print(get_rate("Saturday Night Live"))

# [<TVShow> Saturday Night Live, <TVShow> Sesame Street, <TVShow> The Office, <TVShow> The Simpsons, <TVShow> Doctor Who, <TVShow> South Park, <TVShow> The Walking Dead, <TVShow> The Big Bang Theory, <TVShow> Family Guy, <TVShow> Game of Thrones]