#project-get-seasons

import json
import urllib.request
from urllib.error import HTTPError

# import requests
import trakt

import trakt.tv
import urllib.request
from urllib.error import HTTPError
def connect_trakt():

    trakt.core.OAUTH_TOKEN = "2d54930af74ab77d3152e214777501c4d75128194de3da07847df376c15f0b52"
    trakt.core.CLIENT_ID = "6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32"
    trakt.core.CLIENT_SECRET = "fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b"


def get_all_seasons(show):

    seasons = (show.seasons[1:])
    seasons_new = []
    for j in range(0, len(seasons)):
        seasons_new.append(get_ep_name(str(seasons[j])))

    return (seasons_new), len(seasons)

def get_ep_name(people_name):
    # show_name = "Sesame Street"
    # episode_name = "<TVEpisode>: Sesame Street S50E11 The Great Fruit Strike"
    #    Sesame Street
    people_name=people_name
    after_sp = people_name.split('<TVSeason>: ')
    episode_name=(after_sp[len(after_sp) - 1])
    return episode_name


def lambda_handler(event, context):
    number_of_episodes = 0

    movie_name = event['name']

    connect_trakt()
    show = trakt.tv.TVShow(movie_name)
    try:
        seasons_name, seasons_number=get_all_seasons(show)
        tmdb_id = get_movie_id_tmdb(movie_name)


        images=[]
        # for i in range (1, 1+1):

        for i in range (1, seasons_number+1):
            x = get_image_from_tmdb(tmdb_id, i, 1)
            # print(x)
            images+=[x]
            number_of_episodes = get_ep_num_from_tmdb(tmdb_id, seasons_number)
            # print(number_of_episodes)
        # print(response)
    except(trakt.errors.NotFoundException):
        response="trakt.errors.NotFoundException : cannot get information of this movie/show"

    return json.dumps({
        "statusCode": 200,
        "body": {
            "seasons_name": (seasons_name),
            "number_of_episodes":number_of_episodes,
            "images":(images)
        }
    })
def get_movie_id_tmdb(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['tmdb']

        # response = trakt.movies.Movie(name)
    except(trakt.errors.NotFoundException):
        response = 0
    return response

def get_image_from_tmdb(tmdb_id, sea_num, epi_num):
    try:
        urlData = ('https://api.themoviedb.org/3/tv/%d/season/%d/episode/%d/images?api_key=67dfb229c85e9adefabc60194681a2be'%(tmdb_id, sea_num, epi_num))
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        # print(data)
        encoding = webURL.info().get_content_charset('utf-8')
        json_data = json.loads(data.decode(encoding))
        # print(json_data)

        image_url = (json_data['stills'])
        if(image_url ==[]): return ""
        image_url_1 = image_url[0]['file_path']


        image_pre = "https://image.tmdb.org/t/p/w500"
        image_full = image_pre + image_url_1
        return str(image_full)

    except HTTPError as e:
        content = e.read()



def get_ep_num_from_tmdb(tmdb_id, sea_num):
    try:
        urlData = ('https://api.themoviedb.org/3/tv/%d/season/%d?api_key=67dfb229c85e9adefabc60194681a2be&language=en-US'%(tmdb_id, sea_num))
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        # print(data)
        encoding = webURL.info().get_content_charset('utf-8')
        json_data = json.loads(data.decode(encoding))
        # print(json_data)
        number_of_episodes = json_data['episodes'].__len__()
        # number_of_seasons = json_data['number_of_seasons']

        # first_air_date = json_data['first_air_date']
        # languages = json_data['languages']
        # image_url = json_data['poster_path']
        # image_pre = "https://image.tmdb.org/t/p/w500"
        # image_full = image_pre + image_url


    except HTTPError as e:
        content = e.read()
    return number_of_episodes

event={"name":"Sesame Street"}
event={"name":"Destination Fear"}

# event = {"name":"The Dead Files"}
print(lambda_handler(event, '1'))
# zip -g function.zip app_rate.py
# aws lambda update-function-code --function-name project-rate --zip-file fileb://function.zip
# get_image_from_tmdb(1399)