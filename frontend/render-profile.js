var apigClient = apigClientFactory.newClient({
    apiKey: 'o8pWwS43OETeRWe1dYghaKmEgJ1AhTWgt5teJa90',
    accessKey: 'AKIAY4RLRMKBTTSTG2YB',
    secretKey: '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'
});


// 渲染历史记录
function renderHistory(email) {
    apigClient.historyGetHistoryPost({}, {"email": "abc@qq.com"}).then(function (response) {
        var raw = JSON.parse(response['data']);
        var histories = raw['body'];
        var histories = raw['body']['result'];
        for (i = 0; i < histories.length; i++) {
            var history = histories[i];
            var name = history[0];
            var season = history[1];
            var episode = history[2];
            var time = history[3];
            var image = history[4];
            addOneHistoryToList(name, season, episode, time, image);
        }
    });
}

function addOneHistoryToList(name, season, episode, time, image) {
    $("#history-list").append(
        `<div class="card col-md-2 ml-2 p-0">
            <img class="card-img-top img-fluid m-2"
                 src=${image}
                 alt=""/>
            <div class="card-body">
                <h4 class="card-title">${name} S${season} E${episode}</h4>
                <p class="card-text">
                    <small class="text-muted">${time}</small>
                </p>
                 <button class="btn btn-primary" type="button" onclick="deleteHistory('${name}',${season},${episode})">
                 <i class="fas fa-trash-alt"></i></button>
            </div>
        </div>`
    );
}

function renderCollection(email) {
    apigClient.listsGetListGetListListPost({}, {'email': email}).then(function (response) {
        console.log(response);
        var raw = JSON.parse(response['data']['body']);
        var raw = raw['message'];
        console.log(raw);

        if (raw.length < 2) {
            return;
        } else {
            var listName = raw[1];
            var listName = "my love 1";
            apigClient.listsGetListGetListContentPost({}, {
                "email": email,
                "list_name": listName
            }).then(function (result) {
                var contentRaw = JSON.parse(result['data']);
                var content = contentRaw['body']['message'];
                // content  = [1399, "Game of Thrones", "1", "2", "https://image.tmdb.org/t/p/w500/icjOgl5F9DhysOEo6Six2Qfwcu2.jpg"]
                console.log(content);

            })
        }
    })
}


renderHistory("abc@qq.com");
renderCollection("abc@qq.com");
