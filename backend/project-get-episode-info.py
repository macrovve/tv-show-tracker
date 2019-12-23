#project-get-episode-info
import trakt.tv
import json
import urllib.request
from urllib.error import HTTPError
# <TVEpisode>: Sesame Street S50E11 The Great Fruit Strike

def get_movie_id(name):
    try:
        response = trakt.tv.TVShow(name).ids['ids']['trakt']
        # response = trakt.movies.Movie(name)
    except(trakt.errors.NotFoundException):
        response = 0
    return response

def get_ep_num(episode_name, show_name):
    # show_name = "Sesame Street"
    # episode_name = "<TVEpisode>: Sesame Street S50E11 The Great Fruit Strike"
    #    Sesame Street
    show_name=show_name
    after_sp = show_name.split('<TVShow>: ')
    show_name=(after_sp[len(after_sp) - 1])

    # Sesame Street S50E11 The Great Fruit Strike
    episode_name=episode_name
    after_sp = episode_name.split('<TVEpisode>: ')
    episode_name=(after_sp[len(after_sp) - 1])

    # S50E11
    episode_name_after_sp = episode_name.split(' ')
    show_name_after_sp = show_name.split(' ')
    # print(episode_name_after_sp)
    season_num = (episode_name_after_sp[len(show_name_after_sp)])

    # 5, 11
    # print(season_num)
    no_s = season_num.split('S')
    # print(no_s)
    season, episode = no_s[1].split('E')
    # print(int(season), int(episode))
    return show_name, int(season), int(episode)

def get_ep_overview_image(show_name, sea_num, ep_num):
    show = trakt.tv.TVShow(show_name)
    tmdb_id = get_movie_id_tmdb(show_name)
    season = (show.seasons[sea_num])
    episodes = (season.episodes)
    # print(episodes[ep_num-1])
    episode = episodes[ep_num-1]
    overview = episode.overview
    watch_exl = "https://trakt.tv/" + episode.ext_full
    images_ext = get_image_from_tmdb(tmdb_id, sea_num, ep_num)
    rate = round(episode.rating, 1)
    first_aired_date = episode.first_aired_date
    # print(overview)
    return overview,watch_exl,str(images_ext),rate,first_aired_date

def connect_trakt():

    trakt.core.OAUTH_TOKEN = "2d54930af74ab77d3152e214777501c4d75128194de3da07847df376c15f0b52"
    trakt.core.CLIENT_ID = "6dca1dcd2331fd4874c713d2c85c28f35a47f9f3286f2e69d9ba0c81a8773c32"
    trakt.core.CLIENT_SECRET = "fadadc5a8fc9b1861aedfc8407e08184dcc64c1109486ec3644602469a37a42b"

def lambda_handler(event, context):
    show_name = event['name']
    episode_name = event['episode_name']


    connect_trakt()
    try:
        show_name, season, episode = get_ep_num(episode_name, show_name)
        overview,watch_exl,images_ext,rate,first_aired_date=(get_ep_overview_image(show_name, season, episode))
        response="success achieved"
    except(trakt.errors.NotFoundException):
        response="trakt.errors.NotFoundException : cannot get information of this movie/show"
        overview= ""
        watch_exl= ""
        images_ext= ""
        rate= ""
        first_aired_date= ""


    return json.dumps({
        "statusCode": 200,
        "body": {
            "message": str(response),
            "overview":overview,
            "watch_exl":watch_exl,
            "images_ext":images_ext,
            "first_aired_date":str(first_aired_date),
            "rate":rate
            # "location": ip.text.replace("\n", "")
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
        image_url = (json_data['stills'][0]['file_path'])
        image_pre = "https://image.tmdb.org/t/p/w500"
        image_full = image_pre + image_url

    except HTTPError as e:
        content = e.read()
    return image_full

def transfer_space(xs):
    res=""
    for x in xs:
        if(x == '\\u'):
            x=' '
        res=res + (x)
    return res
# "<TVEpisode>: Game of Thrones S2E1 The North Remembers"

event={"name":"Game of Thrones", "episode_name":"Game of Thrones S2E1 The North Remembers"}

print(lambda_handler(event, '1'))
# connect_trakt()
# #
# season, episode=get_ep_num("<TVEpisode>: Game of Thrones S2E1 The North Remembers","Game of Thrones")
# overview,watch_exl,images_ext,rate,first_aired_date = (get_ep_overview(season, episode))
# print(overview,watch_exl,images_ext,rate,first_aired_date)


