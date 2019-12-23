# project-get-episodes
import trakt.tv
# <TVSeason>: Sesame Street Season 50

import urllib.request
from urllib.error import HTTPError
import json


# import requests
import trakt

import trakt.tv

def connect_trakt():

    trakt.core.OAUTH_TOKEN = "2d54930af74ab77d3152e214777501c4d75128194de3da07847df376c15f0b52"
    trakt.core.CLIENT_ID = "6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32"
    trakt.core.CLIENT_SECRET = "fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b"



def lambda_handler(event, context):
    movie_name = event['name']
    season_name = event['season_name']

    connect_trakt()
    show = trakt.tv.TVShow(movie_name)
    try:
        season_num = get_season_number(season_name)
        response=get_episodes(show,season_num)
        # print(response)
    except(trakt.errors.NotFoundException):
        response="trakt.errors.NotFoundException : cannot get information of this movie/show"

    return json.dumps({
        "statusCode": 200,
        "body": {
            "message": (response),
            # "location": ip.text.replace("\n", "")
        }
    })




def get_season_number(season_name):
    str = season_name
    after_sp = str.split(' ')
    # print(after_sp)
    season_num = int(after_sp[len(after_sp) - 1])
    # print(season_num)
    return season_num

def get_episodes(show, season_num):
    season = (show.seasons[season_num])
    episode = (season.episodes)
    episode_new = []
    for j in range(0, len(episode)):
        episode_new.append(get_ep_name(str(episode[j])))
    return episode_new

def get_ep_name(people_name):
    people_name=people_name
    after_sp = people_name.split('<TVEpisode>: ')
    episode_name=(after_sp[len(after_sp) - 1])
    return episode_name

event={"name":"Sesame Street", "season_name":"<TVSeason>: Sesame Street Season 50"}

print(lambda_handler(event, '1'))

# zip -g function.zip app_rate.py
# aws lambda update-function-code --function-name project-rate --zip-file fileb://function.zip

# https://api.themoviedb.org/3/tv/1399/season/2/images?api_key=67dfb229c85e9adefabc60194681a2be&language=en-US