mapboxgl.accessToken =
	'pk.eyJ1IjoibWFsLXdvb2QiLCJhIjoiY2oyZ2t2em50MDAyMzJ3cnltMDFhb2NzdiJ9.X-D4Wvo5E5QxeP7K_I3O8w';
const map = new mapboxgl.Map({
	container: 'map',
	style: 'mapbox://styles/mapbox/dark-v10',
	center: [-0.28634550125236236, 38.03759971570147],
	zoom: 10 
});
map.on('load', () => {
	map.addSource('vessels', {
		'type': 'geojson',
					'data': data 
	});

	map.addLayer(
		{
			'id': 'vessels-heat',
			'type': 'heatmap',
			'source': 'vessels',
			'maxzoom': 15,
			'paint': {
				// increase weight as diameter breast height increases
				'heatmap-weight': {
					'property': 'Weight',
					'type': 'exponential',
					'stops': [
						[1, 0],
						[62, 1]
					]
				},
				// increase intensity as zoom level increases
				'heatmap-intensity': {
					'stops': [
						[11, 1],
						[15, 3]
					]
				},
				// use sequential color palette to use exponentially as the weight increases
				'heatmap-color': [
					'interpolate',
					['linear'],
					['heatmap-density'],
					0,
//                'rgba(236,222,239,0)',
					'rgba(255,255,255,0)',
					0.2,
					'rgb(93, 163, 253)',
					0.4,
					'rgb(5, 111, 252)',
					0.6,
					'rgb(1, 53, 121)',
					0.8,
					'rgb(28,144,153)'
				],
				// increase radius as zoom increases
				'heatmap-radius': {
					'stops': [
						[11, 15],
						[15, 20]
					]
				},
				// decrease opacity to transition into the circle layer
				'heatmap-opacity': {
					'default': 1,
					'stops': [
						[14, 1],
						[15, 0]
					]
				}
			}
		},
		'waterway-label'
	);

	map.addLayer(
		{
			'id': 'vessels-point',
			'type': 'circle',
			'source': 'vessels',
			'minzoom': 14,
			'paint': {
				// increase the radius of the circle as the zoom level and dbh value increases
				'circle-radius': {
					'property': 'Weight',
					'type': 'exponential',
					'stops': [
						[{ zoom: 15, value: 20 }, 5],
						[{ zoom: 15, value: 80 }, 10],
						[{ zoom: 22, value: 20 }, 20],
						[{ zoom: 22, value: 80 }, 50]
					]
				},
				'circle-color': {
					'property': 'Weight',
					'type': 'exponential',
					'stops': [
						[0, 'rgba(255,255,255,0)'],
						[10, 'rgb(93, 163, 253)'],
						[20, 'rgb(5, 111, 252)'],
						[30, 'rgb(2, 80, 182)'],
						[40, 'rgb(1, 53, 121)'],
						[50, 'rgb(28,144,153)'],
						[60, 'rgb(1,108,89)']
					]
				},
				'circle-stroke-color': 'white',
				'circle-stroke-width': 1,
				'circle-opacity': {
					'stops': [
						[14, 0],
						[15, 1]
					]
				}
			}
		},
		'waterway-label'
	);
});
