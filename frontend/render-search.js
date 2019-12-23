var apigClient = apigClientFactory.newClient({
    apiKey: 'o8pWwS43OETeRWe1dYghaKmEgJ1AhTWgt5teJa90',
    accessKey: 'AKIAY4RLRMKBTTSTG2YB',
    secretKey: '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'
});

function renderSearchResult(query) {
    apigClient.searchGet({"q":query}).then(function (response) {
        console.log(response);
        var hits = response['data']['hits'];
        console.log(hits);
        var num = hits['found'];
        var data = hits['hit']; // num 长度到数组

        for (i = 0; i < num; i++) {
            var movie = data[i]['fields']['movie_name'];
            var picture = data[i]['fields']['images'];
            var overview = data[i]['fields']['overview'];
            addSearchResultToList(movie, picture, overview);
        }
    })
}

function addSearchResultToList(movie, picture, overview) {
    $('#search-result-list').append(
        `<div class="card col-md-3 h-100 mt-2">
            <img class="card-img-top img-fluid"
                 src=${picture}
                 alt=""/>
            <div class="card-body">
                <h4 class="card-title"><a href="detail-overall.html?name=${movie}"> ${movie}</a> </h4>
                <p class="card-text text-truncate">
                    ${overview}
                </p>
                <p class="card-text">
<!--                    <small class="text-muted">Last updated 3 mins ago</small>-->
                </p>
            </div>
        </div>`
    );
}


var q = getParameterByName("q",);
renderSearchResult(q);