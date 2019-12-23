# project-get-history
import boto3
from boto3.dynamodb.conditions import Key
import urllib.request
from urllib.error import HTTPError
import json
import trakt
import trakt.users
#get history list
def lambda_handler(event, context):
    # TODO implement
    connect_trakt()
    email = event['email']
    result= db2_search(email)
    # from_api = (get_watchlist())
    return json.dumps({
        "statusCode": 200,
        "body": {
            "message": "success",
            "result":result
            # "from-api": str(from_api)
            # "location": ip.text.replace("\n", "")
        },
    })
def connect_trakt():

    trakt.core.OAUTH_TOKEN = "2d54930af74ab77d3152e214777501c4d75128194de3da07847df376c15f0b52"
    trakt.core.CLIENT_ID = "6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32"
    trakt.core.CLIENT_SECRET = "fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b"
# def get_watchlist():
#     return trakt.users.User("yuejoy").watchlist_shows


def db2_search(email):
    result=[]


    email=email


    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    visitors = dynamodb.Table('project-history')

    # print(visitors.creation_date_time)



    response = visitors.query(
    KeyConditionExpression=Key('email').eq(email))
    for i in response['Items']:
        s_e_json = ((i['s_e']))
        tmdb_id,se,ep = s_e_json.split('_')
        image = get_image_from_tmdb( int(tmdb_id), int(se), int(ep))
        # result.append([i['movie_name'],se,ep,i['ttl'],image])
        result.append([i['movie_name'],se,ep,i['ttl'],image, i['s_e']])


    return result
def get_image_from_tmdb(tmdb_id, sea_num, epi_num):
    try:
        urlData = ('https://api.themoviedb.org/3/tv/%d/season/%d/episode/%d/images?api_key=67dfb229c85e9adefabc60194681a2be'%(tmdb_id, sea_num, epi_num))
        webURL = urllib.request.urlopen(urlData)
        data = webURL.read()
        # print(data)
        encoding = webURL.info().get_content_charset('utf-8')
        json_data = json.loads(data.decode(encoding))
        image_url = (json_data['stills'])
        if(image_url ==[]): return ""
        image_url_1 = image_url[0]['file_path']


        image_pre = "https://image.tmdb.org/t/p/w500"
        image_full = image_pre + image_url_1

    except HTTPError as e:
        content = e.read()
    return image_full
event = {"email":"abc@qq.com"}
print(lambda_handler(event,'1'))