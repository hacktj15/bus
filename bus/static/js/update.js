$(function() {

    var timeout_interval = 10 * 1000;
    if(location.search.indexOf('timeout=') != -1) {
        timeout_interval = parseInt(location.search.split('timeout=')[1].split('&')[0]) * 1000
    }

    console.log("timeout interval=", timeout_interval)
    update_display = function() {
        $.get("", {}, function(d) {
            var txt = $(".container", $(d)).html();
            console.log(txt);
            $(".container").html(txt)
            console.log(new Date());
            drawCanvas();
        }, "text")
    }

    if(timeout_interval > 0) {
        setInterval(update_display, timeout_interval)
    }


});