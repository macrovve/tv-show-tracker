// var url = www.google.com/?value=123
// var data = getParameterByName("value")
// data => 123
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function getDayOfWeek(date) {
    var dayOfWeek = new Date(date).getDay();
    return isNaN(dayOfWeek) ? null : ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][dayOfWeek];
}

// Game of Thrones S2E1 The North Remembers => 2, 1
function getSeasonAndEpisode(str) {
    match = str.match("S[1-9]+E[1-9]+");
    match = match[0];
    console.log("match", match);
    return {
        "season": match.charAt(1),
        "episode":match.charAt(3)
    }
}