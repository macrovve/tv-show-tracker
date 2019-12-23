# project-get-calendar
import urllib.request
from urllib.error import HTTPError
import json
import datetime
def next_week():
    current_time = datetime.datetime.now()
    d = datetime.date(current_time.year, current_time.month, current_time.day)
    next_week_day=[]
    for i in range(0,7):
        next_week_day = [str(next_weekday(d, i))]+next_week_day  # 0 = Monday, 1=Tuesday, 2=Wednesday...

    # print(next_week_day)
    return next_week_day

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)

def get_calender(date, days):
    date = str(date)
    days=int(days)
    headers = {
      'Content-Type': 'application/json',
      'trakt-api-version': '2',
      'trakt-api-key': '6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32'
    }
    exl="https://api.trakt.tv/calendars/all/shows/%s/%d"%(date,days)
    request = urllib.request.Request(exl, headers=headers)

    try:
        # handler = urllib.request.urlopen(request).read()
        webURL = urllib.request.urlopen(request)
        data = webURL.read()
        encoding = webURL.info().get_content_charset('utf-8')
        json_data = json.loads(data.decode(encoding))
        result=[]
        for x in json_data:
            first_aired = x['first_aired']
            episode = x['episode']
            season = episode['season']
            epi_number = episode['number']
            trakt_id = episode['ids']['trakt']
            tmdb_id = episode['ids']['tmdb']
            show = x['show']
            title = show['title']
            one_info = [title, first_aired, trakt_id, tmdb_id, season, epi_number]
            if(tmdb_id != None):
                result.append(one_info)

    # x = b'[{"first_aired":"2019-12-17T00:00:00.000Z","episode":{"season":2,"number":1,"title":"Episode 2019","ids":{"trakt":3824055,"tvdb":7463952,"imdb":null,"tmdb":null,"tvrage":null}},"show":{"title":"Romesh\'s Look Back to the Future","year":2018,"ids":{"trakt":141784,"slug":"romesh-s-look-back-to-the-future","tvdb":356915,"imdb":"tt9683610","tmdb":null,"tvrage":null}}},{"first_aired":"2019-12-17T00:00:00.000Z","episode":{"season":3,"number":17,"title":null,"ids":{"trakt":3840725,"tvdb":7475653,"imdb":null,"tmdb":null,"tvrage":null}},"show":{"title":"Det store eksperimentet","year":2016,"ids":{"trakt":113561,"slug":"det-store-eksperimentet","tvdb":320565,"imdb":null,"tmdb":68912,"tvrage":null}}}]'
    except HTTPError as e:
        re = e.read()

    return result

def byte_to_json(handler):
    my_bytes_value = handler

    # Decode UTF-8 bytes to Unicode, and convert single quotes
    # to double quotes to make it valid JSON
    my_json = my_bytes_value.decode('utf8').replace("'", '"')
    # print(my_json)
    # print('- ' * 20)

    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = json.loads(my_json)
    s = json.dumps(data, indent=4, sort_keys=True)
    # print(s)

def lambda_handler(event, context):
    # current_time = datetime.datetime.now()
    # d = datetime.date(current_time.year, current_time.month, current_time.day)
    # next_monday = next_weekday(d, 3)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
    # print(next_monday)
    # Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday \
    weekdays_dates = next_week()
    response=[]
    for weekday_date in weekdays_dates :
        get_calend = get_calender(weekday_date, 0)
        response = response + [get_calend]

    # print(byte_to_json(response))


    return json.dumps({
        "statusCode": 200,
        "body": {
            "Monday":(response[0]),
            "Tuesday":(response[1]),
            "Wednesday": (response[2]),
            "Thursday": (response[3]),
            "Friday": (response[4]),
            "Saturday": (response[5]),
            "Sunday": (response[6])

            # "location": ip.text.replace("\n", "")
        }
    })


#
# # using now() to get current time
# current_time = datetime.datetime.now()
#
# # Printing attributes of now().
# print("The attributes of now() are : ")
#
# print("Year : ", end="")
# print(current_time.year)
#
# print("Month : ", end="")
# print(current_time.month)
#
# print("Day : ", end="")
# print(current_time.day)
#
# print(get_calender("2019-12-19", 0))
#
event={}
print(lambda_handler(event, '1'))
# print(next_week())

