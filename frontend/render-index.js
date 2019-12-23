var apigClient = apigClientFactory.newClient({
    // apiKey: 'o8pWwS43OETeRWe1dYghaKmEgJ1AhTWgt5teJa90',
    accessKey: 'AKIAY4RLRMKBTTSTG2YB',
    secretKey: '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'
});


function render_calendar() {
    apigClient.calendarPost({}, {}).then(function (result) {
        var raw = JSON.parse(result['data']);
        raw = raw['body'];

        weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        for (i = 0; i < weekday.length; i++) {
            currentDay = weekday[i];
            todayShows = raw[currentDay];
            // console.log(`calendar-${currentDay.toLocaleLowerCase()}`);
            // console.log(todayShows);
            // var table = document.getElementById(`calendar-${currentDay.toLocaleLowerCase()}`);
            var table = `calendar-${currentDay.toLocaleLowerCase()}`;


            for (j = 0; j < todayShows.length; j++) {
                show = todayShows[j];
                showName = show[0];

                time = new Date(show[1]).toLocaleDateString("en-US", {hour: 'numeric', minute: 'numeric'});
                season = show[4];
                episode = show[5];

                add_one_line_to_calendar_table(table, showName, time, season, episode);
            }
        }
    })
}

function add_one_line_to_calendar_table(table, showName, time, season, episode) {
    // var table = 'calendar-monday';
    // $(`#${table}`).
    $(`#${table}`).children('tbody').append(
        `<tr>
            <td><a href="detail-overall.html?name=${showName}">${showName}</a></td>
            <td>${season} x ${episode} </td>
        </tr>`
    );
    // var tableBody = table.getElementsByTagName('tbody')[0];
    //
    // // 修改ui中的一行
    // newRow = tableBody.insertRow();
    // var nameCell = newRow.insertCell();
    //
    //
    // // var timeCell = newRow.insertCell();
    // // timeCell.appendChild(document.createTextNode(time));
    //
    // var seasonCell = newRow.insertCell();
    // seasonCell.appendChild(document.createTextNode(`${season} x ${episode}`));
}

function render_slider_and_popular() {
    apigClient.popularPost({}, {}).then(function (result) {
        var raw = JSON.parse(result['data']);
        raw = raw['body'];

        populars = raw['message'];
        for (i = 0; i < populars.length; i++) {
            apigClient.infoGetFromApiPost({}, {"name": populars[i]}).then(function (rawInfo) {
                // console.log(rawInfo);
                var rawInfo = JSON.parse(rawInfo['data']);
                var show = rawInfo['body'];
                showName = show['movie_name'][0];
                first_air_date = show['first_air_date'][0];
                picture = show['images'][0];
                overview = show['overview'][0];

                add_one_picture_to_slider(showName, picture, first_air_date);
                add_one_card_to_popular_section(showName, picture, overview, first_air_date);
            })
        }

    });
}

function add_one_card_to_popular_section(name, picture, overview, first_air_date) {
    $('#popular-card-columns').append(
        `<div class="card">
            <img class="card-img-top img-fluid"
                 src=${picture}
                 alt=""/>
            <div class="card-body">
                <h4 class="card-title"><a href="detail-overall.html?name=${name}">${name}</a> </h4>
                <p class="card-text">
                    ${overview}
                </p>
                <p class="card-text">
                    <small class="text-muted">${first_air_date}</small>
                </p>
            </div>
        </div>`
    );
}

function add_two_picture_to_slider(name1, picture1, first_air_date1, name2, picture2, first_air_date2) {
    $("#carousel-inner").append(
        `<div class="carousel-item active">
                        <div class="row d-flex m-auto">
                            <div class="col col-md-5 ">
                                <img class="d-block img-fluid"
                                     src=${picture1}
                                     alt="First Slide"/>
                            <div class="carousel-caption d-none d-md-block">
                <!--                <h3>${name1}</h3>-->
                                <p>${first_air_date1}</p>
                            </div>
                            </div>
                            <div class="col col-md-5">
<!--                                src="https://source.unsplash.com/wgq4eit198Q/700x400"-->
                                <img class="d-block img-fluid"
                                     ssrc=${picture2}
                                     alt="First Slide"/>
                                <div class="carousel-caption d-none d-md-block">
                    <!--                <h3>${name2}</h3>-->
                                    <p>${first_air_date2}</p>
                                </div>
                            </div>

                        </div>

                    </div>`
    )
}
function add_one_picture_to_slider(name, picture, first_air_date) {
    $('#carousel-inner').append(
        `<div class="carousel-item col-md-5">
            <img class="d-block img-fluid"
                 src=${picture}
                 alt="First Slide"/>
            <div class="carousel-caption d-none d-md-block">
<!--                <h3>${name}</h3>-->
                <p>${first_air_date}</p>
            </div>
        </div>`
    );
}



render_calendar();
render_slider_and_popular();

//
// var params = {
//     AccessToken: 'eyJraWQiOiI1XC9sVHV4VTRQTXAyWEVrVzNWeVA1Z1FrRFBjVGFRcjU1NFlGUlA5clUyST0iLCJhbGciOiJSUzI1NiJ9' /* required */
// };
//
//
// cognitoidentityserviceprovider.getUser(params, function (err, data) {
//     if (err) {
//         console.log(err, err.stack);
//     } else {
//         console.log(data);
//     }
// })
