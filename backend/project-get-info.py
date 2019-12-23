#project-get-info
import json
from decimal import Decimal
from boto3.dynamodb.conditions import Key
import boto3
# import requests
import trakt
import trakt.tv
import urllib.request
from urllib.error import HTTPError
# project-get-info
# from trakt.tv import popular_shows
def get_movie_id(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['trakt']
        # response = trakt.movies.Movie(name)
    except(trakt.errors.NotFoundException):
        response = 0
    return response

def get_people_name(people_name):
    # show_name = "Sesame Street"
    # episode_name = "<TVEpisode>: Sesame Street S50E11 The Great Fruit Strike"
    #    Sesame Street
    people_name=people_name
    after_sp = people_name.split('<Person>: ')
    episode_name=(after_sp[len(after_sp) - 1])
    return episode_name



def get_from_api(movie_name):
    tmdb_id = get_movie_id_tmdb(movie_name)
    first_air_date, languages, images = get_image_from_tmdb(tmdb_id)
    # images = trakt.tv.TVShow(movie_name).images_ext
    # seasons = trakt.tv.TVShow(movie_name).seasons
    cast = trakt.tv.TVShow(movie_name).cast
    # print(cast)
    cast_new =""
    # for each in cast:
    #     cast_new += (get_people_name(str(each)))
    for i in range(0, len(cast)):
        cast_new += (get_people_name(str(cast[i])))
        if(i != len(cast) - 1):
            cast_new += ", "


    # related = trakt.tv.TVShow(movie_name).related
    show=trakt.tv.TVShow(movie_name)
    genres = show.genres
    result_g = ""
    for j in range(0, len(genres)):
        result_g += str(genres[j])
        if (j != len(genres) - 1):
            result_g += ", "


    overview = show.overview
    rate=round(trakt.tv.TVShow(movie_name).rating,1)
    return cast_new,images,result_g,overview,rate, first_air_date, languages

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
        result +=  [i['movie_id']],[i['movie_name']],[i['cast']],[i['images']],[i['genres']],[i['overview']],[i['rate']],[i['first_air_date']],[i['languages']]

    return result
def get_recommend_tv():
    all_shows = trakt.tv.get_recommended_shows()
    return (all_shows)
def get_rate(name):
    return round(trakt.tv.TVShow(name).rating,1)
def db1_insert(movie_id,movie_name, cast,images,genres,overview,rate,first_air_date, languages):

    movie_id = movie_id
    movie_name=movie_name
    cast=cast
    images=images
    genres=genres
    overview=overview
    rate=str(rate)
    first_air_date= str(first_air_date)
    languages = str(languages)

    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    passcodes = dynamodb.Table('project-info')
    # print(passcodes.creation_date_time)

    passcodes.put_item(Item={
        'movie_id': movie_id,
        'movie_name': movie_name,
        "cast": cast,
        "images": images,
        "genres": genres,
        "overview": overview,
        "rate":rate,
        "first_air_date":first_air_date,
        "languages":languages
    })

    return ("insert")
def lambda_handler(event, context):
    connect_trakt()
    movie_name=event['name']
    movie_id = get_movie_id(movie_name)
    result = db2_search(movie_id)
    # print(result)
    if(result== []):

        connect_trakt()

        try:
            cast,images,genres,overview,rate, first_air_date, languages = get_from_api(movie_name)
            db1_insert(movie_id,movie_name,cast,images,genres,overview,rate, first_air_date, languages)

            # print(cast)
            response = "insert successful"
        except(trakt.errors.NotFoundException):
            response="trakt.errors.NotFoundException : cannot get information of this movie/show"

    else:
        response = "from db"
        movie_name=(result[1])
        cast=result[2]
        images=result[3]
        genres=result[4]
        overview=result[5]
        rate=(result[6])
        first_air_date = result[7]
        languages=result[8]

    return json.dumps({
        "statusCode": 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        "body": {
            "response":response,
            "movie_name": movie_name,
            "cast": cast,
            "images": images,
            "genres": genres,
            "overview": overview,
            "rate": rate,
            "first_air_date": first_air_date,
            "languages": languages
        }
    })
def get_movie_id_tmdb(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['tmdb']
        # response = trakt.movies.Movie(name)
    except(trakt.errors.NotFoundException):
        response = 0
    return response

def get_image_from_tmdb(tmdb_id):
    try:
        urlData = ('https://api.themoviedb.org/3/tv/%d?api_key=67dfb229c85e9adefabc60194681a2be&language=en-US'%(tmdb_id))
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        # print(data)
        encoding = webURL.info().get_content_charset('utf-8')
        json_data = json.loads(data.decode(encoding))
        print(json_data)

        first_air_date = json_data['first_air_date']
        languages = json_data['languages']
        new_lang=""
        for i in  range(0, len(languages)):
            new_lang += str(languages[i])
            if (i != len(languages)-1):
                new_lang += ", "


        image_url = json_data['poster_path']
        image_pre = "https://image.tmdb.org/t/p/w500"
        image_full = image_pre + image_url


    except HTTPError as e:
        content = e.read()
    return first_air_date, new_lang, image_full

    # https: // api.themoviedb.org / 3 / tv / 502?api_key = 67dfb229c85e9adefabc60194681a2be & language = en - US

# connect_trakt()
# print(get_from_api("Sesame Street"))
# event={"name":"Ad Astra"}
# event={"name":"Saturday Night Live"}
event={"name":"The Dead Files"}

s=(lambda_handler(event, '1'))
# s_json = json.loads(s)
print(s)
# zip -g function.zip app_rate.py
# aws lambda update-function-code --function-name project-rate --zip-file fileb://function.zip
# connect_trakt()
# print(get_recommend_tv())
# print(get_rate("Saturday Night Live"))

# print(get_image_from_tmdb(502))#
# print(get_image_from_tmdb(1399))
# s=get_image_from_tmdb(502)
# print(s)

# print(get_from_api("Sesame Street")
# )
# [<TVShow> Saturday Night Live, <TVShow> Sesame Street]
# , <TVShow> The Office, <TVShow> The Simpsons, <TVShow> Doctor Who, <TVShow> South Park, <TVShow> The Walking Dead, <TVShow> The Big Bang Theory, <TVShow> Family Guy, <TVShow> Game of Thrones]