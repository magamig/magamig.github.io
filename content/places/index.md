---
title: "Places"
---

I've lived in <span id="PRT" class="interactive">Portugal</span>, <span id="HUN" class="interactive">Hungary</span>, <span id="FIN" class="interactive">Finland</span>, and I'm currently based in <span id="FRA" class="interactive">France</span>. Below is the map with the countries I've visited.

<i><span id="selectedLabel">&nbsp;</span></i>
<div id="map"></div>

<script src="https://d3js.org/d3.v6.min.js"></script>
<script src="https://d3js.org/d3-geo-projection.v2.min.js"></script>
<script>
    const visited = ["PRT","ESP","LUX","ITA","HUN","MKD","KOS","SVK","POL","BIH",
        "HRV","SVN","SRB","FRA","DEU","AUT","CZE","UKR","MDA","ROU","BGR","ALB",
        "MNE","CHL","GBR","VAT","DNK","SWE","CHE","IND","LKA","FIN","EST"];
    const selectedLabel = document.getElementById("selectedLabel");
    let w = 1000,
        h = 620,
        projection = d3.geoMercator().translate([w/2, h/2]).scale(150).center([0,45]);
        path = d3.geoPath().projection(projection),
        svg = d3.select("#map")
            .append("svg")
            .attr("preserveAspectRatio", "xMinYMin meet")
            .attr("viewBox", "0 0 " + w + " " + h)
            .classed("svg-content", true);
    let mouseOver = function(d) {
        console.log(d)
        d3.selectAll("path")
            .transition()
            .duration(200)
            .style("opacity", .5)
            .style("stroke", "transparent");
        d3.select(d.target)
            .transition()
            .duration(200)
            .style("opacity", 1)
            .style("stroke", "black");
        selectedLabel.innerHTML = ("> " + d.target.__data__.properties.name) ?? "";
    };
    let mouseLeave = function() {
        d3.selectAll("path")
            .transition()
            .duration(200)
            .style("opacity", 1)
            .style("stroke", "transparent");
        selectedLabel.innerHTML = "&nbsp;";
    };
    [...document.getElementsByClassName('interactive')].forEach((e) => {
        e.onmouseover = () => mouseOver({target: "path#" + e.id});
        e.onmouseleave = () => mouseLeave()
    });
    d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")
        .then((values) => {
            svg.selectAll("path")
                .data(values.features)
                .enter()
                .append("path")
                .style("stroke", "transparent")
                .on("mouseover", mouseOver )
                .on("mouseleave", mouseLeave )
                .attr("d", path)
                .attr("id", d => d.id)
                .attr("fill", (d) => 
                    visited.includes(d.id) 
                    ? '#03c8ff' 
                    : '#999999'
                );
        });
</script>
