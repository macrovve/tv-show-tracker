import json


# import requests
import trakt
import trakt.tv

# from trakt.tv import popular_shows


def connect_trakt():

    trakt.core.OAUTH_TOKEN = "2d54930af74ab77d3152e214777501c4d75128194de3da07847df376c15f0b52"
    trakt.core.CLIENT_ID = "6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32"
    trakt.core.CLIENT_SECRET = "fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b"

# # trakt.init('yuejoy', client_id="6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32", client_secret="fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b")
# all_movies = get_recommended_movies()
# print(all_movies)
def get_recommend_tv():
    all_shows = trakt.tv.get_recommended_shows()
    return (all_shows)
def get_rate(name):
    return round(trakt.tv.TVShow(name).rating,1)

def lambda_handler(event, context):
    name=event['name']


    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    connect_trakt()
    try:
        response=get_rate(name)
    except(trakt.errors.NotFoundException):
        response="trakt.errors.NotFoundException : cannot get information of this movie/show"


    # print(response)
    # all_movies = get_recommend_tv()
    # print(all_movies)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": str(response),
            # "location": ip.text.replace("\n", "")
        }),
    }

# event={"name":"Ad Astra"}
# event={"name":"Saturday Night Live"}
#
# print(lambda_handler(event, '1'))
# zip -g function.zip app_rate.py
# aws lambda update-function-code --function-name project-rate --zip-file fileb://function.zip
# connect_trakt()
# print(get_recommend_tv())
# print(get_rate("Saturday Night Live"))

# [<TVShow> Saturday Night Live, <TVShow> Sesame Street, <TVShow> The Office, <TVShow> The Simpsons, <TVShow> Doctor Who, <TVShow> South Park, <TVShow> The Walking Dead, <TVShow> The Big Bang Theory, <TVShow> Family Guy, <TVShow> Game of Thrones]