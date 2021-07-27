---
title: "Crossing an Entire Country in a Straight Line"
date: 2021-07-24T21:00:00+01:00
location: "Monaco"
---
<!-- leaflet -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" integrity="sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A==" crossorigin=""/>
<script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js" integrity="sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA==" crossorigin=""></script>
<!-- leaflet-fullscreen -->
<script src='https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/Leaflet.fullscreen.min.js'></script>
<link href='https://api.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v1.0.1/leaflet.fullscreen.css' rel='stylesheet' />
<!-- leaflet-draw (dependency) -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.3.2/leaflet.draw.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.3.2/leaflet.draw.js"></script>
<!-- leaflet-measurecontrol -->
<link rel="stylesheet" href="https://makinacorpus.github.io/Leaflet.MeasureControl/leaflet.measurecontrol.css">
<script src="https://cdn.jsdelivr.net/npm/leaflet.measurecontrol@1.1.0/leaflet.measurecontrol.min.js"></script>

![](/image/monaco.jpg)

Recently, I've crossed an entire country in a straight line. "Why?", you might ask... why not? Inspired by [Tom Davies](https://www.atlasobscura.com/articles/geowizard-davies-straight-line-mission-across) (aka [GeoWizard](https://www.youtube.com/channel/UCW5OrUZ4SeUYkUg1XqcjFYA)), I decided to go on this harmless adventure & challenge across... Monaco! Not as exciting as Tom's missions across Norway or Wales, but good enough as a .

Before embarking on this trip, some planning had to be done. Since Monaco is a small country, we had to cross a small distance. Nevertheless, it's very mountainous and full of buildings everywhere, which makes the straigh line part of the challenge complex. The strategy used to approach this challenge was to go on Google Maps and drop two pins one for start and stop and moving them around until we converged to an adequate path. After having this pre-planned route it was time to draw the **actual line** (in green below) and then try to stick as closer as possible to it.

<div id="xsmap"></div>

Due to the difficulties presented by the terrain and the constructions, the plan was to make use of the "man-made facilities" to go accross the country - a combination of several of these, aligned in a straight line, was necessary to viabilize the selected route.

Since I arrived by train, that matched my start point for this challenge. The first step was to go up the escalators and go in direction of France, which meant starting to the parking lot - it is already within France and did not require me to leave and go around the train station. Then, you just go in the direction of the sea and take the elevator, in order not to ruin your precious straight line. Afterwards, you have some stairs. Later, a charming "slightly curved" walk around Chapelle Sainte-Dévote. Then, you cross the road in an illegal manner right near the crosswalk. And finally, there is an underpass that keeps you as close as possible to the line, without the need to do some *parkour*, which leads you to part of the F1 race track right near the marina - after all, it's Monaco!

This path is drawn in blue on the map above. You can use the ruler to make some measurements; I've used to measure my maximum distance from the line - which was 20 meters, a 🏆 **Platinum rank**.

<div class="info">

**Tom's Ranking**

| | | |
|-|-|-|
| 🏆  &emsp; | **Platinum** &emsp; | **< 25 meters**  |
| 🥇 | Gold     | < 50 meters  |
| 🥈 | Silver   | < 75 meters  |
| 🥉 | Bronze   | < 100 meters |

<br/>

</div>


<script type="module">
const map = L.map('xsmap').setView([51.505, -0.09], 13);
map.addControl(new L.Control.Fullscreen());
L.Control.measureControl().addTo(map);

const response = await fetch("/other/monaco.geojson");
const data = await response.json();
const geojson = L.geoJson(data, {
	style: feature => {
		return feature.style;
	}
});
geojson.addTo(map);
map.fitBounds(geojson.getBounds());

// L.tileLayer('https://tiles.stadiamaps.com/tiles/osm_bright/{z}/{x}/{y}{r}.png?api_key=c07befc9-a828-4993-9ede-3071b3008b8c'
// L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager_labels_under/{z}/{x}/{y}' + (L.Browser.retina ? '@2x.png' : '.png'), {
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 20,
	//attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors'
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

</script>
