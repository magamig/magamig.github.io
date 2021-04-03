---
title: "Places"
---

I've lived in Portugal, Hungary, Finland, and I'm currently based in France. The map with the countries I've visited is below.

<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
<div id="map"></div>
<script>
    var visited = ["PRT","ESP","LUX","ITA","HUN","MKD","KOS","SVK","POL","BIH",
    "HRV","SVN","SRB","FRA","DEU","AUT","CZE","UKR","MDA","ROU","BGR","ALB","MNE",
    "CHL","GBR","VAT","DNK","SWE","CHE","IND","LKA","FIN","EST"];
    var map = L.map('map', { 
        attributionControl: false,
        dragging: !L.Browser.mobile
    });
    map.fitBounds([[-30, -70], [60, 100]]);
    map.scrollWheelZoom.disable();
    function style(feature) {
        return {
            fillColor: (visited.includes(feature.properties.adm0_a3) 
                ? '#03c8ff' 
                : '#606060'),
            weight: 1,
            opacity: 1,
            color: 'white',
            fillOpacity: 1
        };
    }        
    var myCustomStyle = {
        stroke: false,
        fill: true,
        fillColor: '#fff',
        fillOpacity: 1
    };
    fetch('https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_0_countries.geojson')
        .then(response => response.json())
        .then(data => L.geoJson(data, { style: style }).addTo(map));
</script>