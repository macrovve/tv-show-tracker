var apigClient = apigClientFactory.newClient({
    // apiKey: 'o8pWwS43OETeRWe1dYghaKmEgJ1AhTWgt5teJa90',
    accessKey: 'AKIAY4RLRMKBTTSTG2YB',
    secretKey: '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'
});
// console.log('hello');
// var body = {
//     "name": "Sesame Street"
// };

// var data;
// apigClient.gernGetGernPost({}, body).then(function (result) {
//     console.log(result);
// });
// apigClient.infoGetFromApiPost()
//
// var data = apigClient.popularPost().then(function (result) {
//     console.log(result);
//     data=result;
// });

// 渲染简介和背景图片
function renderBasicInfo(tvName) {
    var movieName;
    var cast;
    var genres;
    var images;
    var overview;
    var rate;
    var first_air_date;
    var language;

    // 获取这个剧的详细信息
    apigClient.infoGetFromApiPost({}, {"name": tvName}).then(function (result) {
        // raw = JSON.parse(result['data']);
        raw = JSON.parse(result['data']);
        raw = raw['body'];
        movieName = raw['movie_name'][0];
        cast = raw['cast'][0];
        genres = raw['genres'][0];
        images = raw['images'][0];
        overview = raw['overview'][0];
        rate = raw['rate'][0];
        first_air_date = raw["first_air_date"][0];
        language = raw['languages'][0];
        var backgroundPicture = document.getElementById("background-picture");
        backgroundPicture.style = `background: url(${images}); background-repeat:no-repeat;background-size: cover;background-attachment: fixed;min-height: 700px;`

        document.getElementById("movie-name").innerHTML = movieName;
        document.getElementById("actors").innerHTML = `<span class="badge badge-primary">Actors</span>${cast}`;
        document.getElementById("overview").innerHTML = `<span class="badge badge-primary">Overview</span>${overview}`;
        document.getElementById("rate").innerHTML = `<span class="badge badge-primary">${rate}</span>`;

    }).catch(function (result) {
        console.log("Failed to infoGetFromApiPost");
        console.log(result);
    });
}

// 渲染页面下部每季的卡片
function renderEpisodes(tvName, season) {
    //{"name":"Game of Thrones", "season_name":"<TVSeason>: Game of Thrones Season 2"}
    apigClient.episodesGetEpisodesPost({}, {"name": tvName, "season_name": season}).then(function (result) {
        console.log(result);
        var raw = JSON.parse(result['data']);
        var episodes = raw['body']['message'];

        for (i = 0; i < episodes.length; i++) {
            var episodes_name = episodes[i];
            addOneCardToEpisodeList(tvName, episodes_name, i + 1);
        }
    });

}

function addOneCardToEpisodeList(show_name, episodes_name, order) {
    console.log("add one card to episode list");
    apigClient.episodesGetEpisodeInfoPost({}, {
        "name": show_name,
        "episode_name": episodes_name
    }).then(function (result) {
            console.log(result);
            var raw = JSON.parse(result['data']);
            var info = raw['body'];
            // console.log("episode info", info);
            var image = info['images_ext'];
            var overview = info['overview'];
            var rate = info['rate'];
            var first_aired_date = info['first_aired_date'];
            var watch_url = info['watch_exl'];
            $('#episodes-list').append(
                `<div class="card mt-3">
                <div class="card-horizontal order-${order}" style="display: flex; flex: 1 1 auto;">
                    <div class="img-square-wrapper">
                        <img src=${image}
                             alt=""
                             class="rounded float-left"/>
                    </div>
                    <div class="card-body">
                        <h4 class="card-title">${episodes_name}</h4>
                        <p class="card-text">
                            <span class="badge badge-primary">${rate}</span>
                            <small class="text-muted">${first_aired_date}</small>

                        </p>
                        <p class="card-text">
                            ${overview}
                        </p>
                        <button class="btn btn-primary" type="button" onclick="addToHistory('${show_name}','${episodes_name}')"><i class="fas fa-list"></i></button>
                        <button class="btn btn-primary" type="button"><i class="fas fa-check"></i></button>
                        <button id="play-button" class="btn btn-primary" type="button" onclick="redirect_url('${watch_url}')"><i class="fas fa-play"></i></button>
                        
                    </div>
                </div>
            </div>`
            )
        }
    );
}


var name = getParameterByName("name");
var season = getParameterByName("season");
// renderBasicInfo("Game of Thrones");
// renderEpisodes("Game of Thrones", "Game of Thrones Season 2");
renderBasicInfo(name);
renderEpisodes(name, season);
