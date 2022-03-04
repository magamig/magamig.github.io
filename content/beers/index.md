---
title: "Beers"
---

As a beer enthusiast, I've collected a list of all the different beers I've had within an app called [Untappd](https://untappd.com/user/magamig/beers). If you think this list is incomplete, you can help by suggesting other brews! 

My latest distinct beers were the following (up-to-date in real time):

<div id="beers-list">

![](/image/beer.gif)

</div>

**[Click here to check out the rest of the list!](https://untappd.com/user/magamig/beers)**

<script>
fetch('https://api.untappd.com/v4/user/beers/magamig?client_id=C1F3540111F2A6C0F2E1964C243FB66AB620FCBB&client_secret=0FCC3B5993CB80F43038D7BA914E1E3615600577&limit=10')
    .then(response => response.json())
    .then(raw => {
        data = raw["response"]["beers"]["items"]
        var div = document.getElementById("beers-list");
        div.innerHTML = "";
        for(i=0;i<10; i++) {
            div.innerHTML += "<div style=\"min-height: 120px;\">"
                + "<img src=\"" + data[i]["beer"]["beer_label"] + "\" width=\"100px\" style=\"float:left;\">"
                + "<div style='margin-left:120px;'>"
                + "<b>" + data[i]["beer"]["beer_name"] + "</b> "
                + "(" + data[i]["beer"]["beer_abv"] + "% ABV)<br/>"
                + data[i]["beer"]["beer_style"] + "<br/>"
                + data[i]["brewery"]["brewery_name"] + "<br/><br/>"
                + "</div></div>"
        }
    })
</script>