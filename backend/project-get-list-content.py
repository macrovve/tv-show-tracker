# project-get-list-content
import boto3
from boto3.dynamodb.conditions import Key

import json
import urllib.request
from urllib.error import HTTPError
def lambda_handler(event, context):
    # TODO implement
    list_name = event['list_name']
    email = event['email']
    list_id = get_list_id(list_name, email)
    response = db2_search(list_id)
    return json.dumps({
        "statusCode": 200,
        "body": {
            "message": response,
            # "location": ip.text.replace("\n", "")
        }
    })
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
def db2_search(list_id):
    result=[]

    list_id=list_id


    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    visitors = dynamodb.Table('project-list-content')

    response = visitors.query(
    KeyConditionExpression=Key('list_id').eq(list_id))
    for i in response['Items']:
        image = get_image_from_tmdb(int(int(i['movie_id'])), int(i['season']), int(i['eposides']))
        result +=  [int(i['movie_id']),i['movie_name'], str(i['season']),str(i['eposides']), image]

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

event={"list_name":"my love 1", "email":"abc@qq.com"}
print(lambda_handler(event,'1'))