var apigClient = apigClientFactory.newClient({
    // apiKey: 'o8pWwS43OETeRWe1dYghaKmEgJ1AhTWgt5teJa90',
    accessKey: 'AKIAY4RLRMKBTTSTG2YB',
    secretKey: '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'
});

// 渲染简介和背景图片 Done
function renderBasicInfo(tvName) {
    // 获取这个剧的详细信息
    apigClient.infoGetFromApiPost({}, {"name": tvName}).then(function (result) {
        // raw = JSON.parse(result['data']);
        raw = JSON.parse(result['data']);
        raw = raw['body'];
        console.log(raw);
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
        document.getElementById("actors").innerHTML = `<span class="badge badge-primary text-truncate">Actors</span>${cast}`;
        document.getElementById("overview").innerHTML = `<span class="badge badge-primary text-truncate">Overview</span>${overview}`;
        document.getElementById("rate").innerHTML = `<span class="badge badge-primary">${rate}</span>`;

    }).catch(function (result) {
        console.log("Failed to infoGetFromApiPost");
        console.log(result);
    });

}

// 渲染页面下部每季的卡片
function renderSeasonCard(tvName) {

    apigClient.episodesGetSeasonPost({}, {"name": tvName}).then(function (result) {
        console.log("season", result);

        var raw = JSON.parse(result['data']);
        raw = raw['body'];
        console.log(raw);
        var seasons = raw['seasons_name'];
        var images = raw['images'];
        for (i = 0; i < seasons.length; i++) {
            addOneCardToSeasonList(tvName, seasons[i], images[i]);
        }

    }).catch(function (result) {
        console.log(result);
    });
}

function addOneCardToSeasonList(name, seasonName, image) {
    $('#season-list').append(
        `<div class="card col-md-2 m-2">
          <img class="card-img-top mt-3"
            src=${image}
            alt=""/>

          <div class="card-body">
            <h5 class="card-text text-center" style="color:black;">
                <a href="detail-episode.html?name=${name}&&season=${seasonName}">${seasonName}</a> 
            </h5>
            <p class="card-text text-center">
<!--              <small class="text-muted ">10 episodes</small>-->
            </p>
          </div>
        </div>`);
}

function renderRecommendation(name) {
    // console.log("recommendation");
    apigClient.recommendPredictPost({}, {"name":name}).then(function (result) {
        console.log("recommendation", result);
        var movies = JSON.parse(result['data']['body']);
        console.log("recommend movies", movies);
        for (i = 0; i < movies.length; i++) {
            var showName = movies[i]['movie_name'];
            var image = movies[i]['images'];
            var overview = movies[i]['overview'];
            addOneCardToRecommendation(showName, image, overview);
        }
    });
}

function addOneCardToRecommendation(name, image, overview) {
    console.log(name, image, overview);
    $('#recommendation-list').append(
        `<div class="card col-md-2 m-2">
            <img class="card-img-top img-fluid"
                 src=${image}
                 alt=""/>
            <div class="card-body">
                <h4 class="card-title"><a href="detail-overall.html?name=${name}">${name}</a> </h4>
                <p class="card-text text-truncate">
                    ${overview}
                </p>
            </div>
        </div>`
    );

}
var name = getParameterByName("name");
console.log(name);
renderBasicInfo(name);
renderSeasonCard(name);
renderRecommendation(name);