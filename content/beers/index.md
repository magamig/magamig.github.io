---
title: "Beers"
---

As a beer enthusiast, I've collected a list of all the different beers I've had within an app called [Untappd](https://untappd.com/user/magamig/beers). If you think this list is incomplete, you can help by suggesting other brews! 

My latest beers were the following (up-to-date in real time):

<div id="beers-list">

![](/image/beer.gif)

</div>

**[Click here to check out the rest of the list!](https://untappd.com/user/magamig/beers)**

<script>
fetch('https://wrapapi.com/use/magamig/untappd/distinct-list/1.0.1?wrapAPIKey=k00sa6Ado2F792ICOvLywRTOubqS8T7r')
    .then(response => response.json())
    .then(raw => {
        data = raw["data"]["collection"]
        console.log(data)
        var div = document.getElementById("beers-list");
        div.innerHTML = "";
        for(i=0;i<10; i++) {
            div.innerHTML += "<div style=\"min-height: 120px;\">"
                + "<img src=\"" + data[i]["image"] + "\" width=\"100px\" style=\"float:left;\">"
                + "<div style='margin-left:120px;'>"
                + "<b>" + data[i]["name"] + "</b> "
                + "(" + data[i]["abv"] + ")<br/>"
                + data[i]["style"] + "<br/>"
                + data[i]["brewery"] + "<br/><br/>"
                + "</div></div>"
        }
    })
</script>