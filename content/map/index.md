---
title: "Map"
---

I've lived in <span id="PRT" class="interactive">Portugal</span>, <span id="HUN" class="interactive">Hungary</span>, <span id="FIN" class="interactive">Finland</span>, <span id="FRA" class="interactive">France</span>, <span id="BEL" class="interactive">Belgium</span>,and I'm currently based in <span id="IRL" class="interactive">Ireland</span>. Below is the map with the countries I've visited.

<i><span id="selectedLabel">&nbsp;</span></i>
<div id="map"></div>

<script src="https://d3js.org/d3.v6.min.js"></script>
<script src="https://d3js.org/d3-geo-projection.v2.min.js"></script>
<script>
    const visited = ["PRT","ESP","LUX","ITA","HUN", "MKD","KOS","SVK","POL","BIH",
        "HRV","SVN","SRB","FRA","DEU","AUT","CZE","UKR","MDA","ROU","BGR","ALB",
        "MNE","CHL","GBR","VAT","DNK","SWE","CHE","IND","LKA","FIN","EST","MCO",
        "TUN", "BEL", "GRC", "NLD", "IRL", "MAR", "USA"];
    const selectedLabel = document.getElementById("s~electedLabel");
    let w = 900,
        h = 480,
        projection = d3.geoLarrivee().translate([w/2.15, h/2.85]).scale(145).center([0,45]);
        path = d3.geoPath().projection(projection),
        svg = d3.select("#map")
            .append("svg")
            .attr("preserveAspectRatio", "xMinYMin meet")
            .attr("viewBox", "0 0 " + w + " " + h)
            .classed("svg-content", true);
    let mouseOver = function(d) {
        d3.selectAll("path")
            .style("opacity", 1)
            .style("stroke", "white");
        d3.select(d.target)
            .raise()
            .style("opacity", 0.3)
            .style("stroke", "black");
        selectedLabel.innerHTML = ("> " + (d.name ?? d.target.__data__.properties.name)) ?? "";
    };
    let mouseLeave = function() {
        d3.selectAll("path")
            .style("opacity", 1)
            .style("stroke", "white");
        selectedLabel.innerHTML = "&nbsp;";
    };
    [...document.getElementsByClassName('interactive')].forEach((e) => {
        e.onmouseover = () => mouseOver({target: "path#" + e.id, name: e.innerText});
        e.onmouseleave = () => mouseLeave()
    });
    d3.json("/other/world.geojson")
        .then((values) => {
            svg.selectAll("path")
                .data(values.features)
                .enter()
                .append("path")
                .style("stroke", "white")
                .style("opacity", 1)
                .on("mouseover", mouseOver )
                .on("mouseleave", mouseLeave )
                .attr("d", path)
                .attr("id", d => d.id)
                .attr("fill", (d) => 
                    visited.includes(d.id) 
                    ? '#a40000' 
                    : '#cccccc'
                );
        });
</script>
