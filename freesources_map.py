from flask import Flask, render_template
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)

# Initialize GoogleMaps extension with API key
GoogleMaps(app, key="AIzaSyBd0mJvs0Oue8YIRwLfF2LM4VGaPhc9fFg")

@app.route('/')
def map():
	mymap = Map(
		identifier="view-side",
		lat=37.4419,
		lng=-122.1419,
		markers=[(37.4419, -122.1419)]
	)
	sndmap = Map(
		identifier="sndmap",
		lat=37.4419,
		lng=-122.1419,
		markers=[
			{
				'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
				'lat': 37.4419,
				'lng': -122.1419,
				'infobox': "<b>Hello World</b>"
			},
			{
				'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
				'lat': 37.4300,
				'lng': -122.1400,
				'infobox': "<b>Hello World from other place</b>"
			}
		]
	)
	return render_template('freesources_map.html', mymap=mymap, sndmap=sndmap)

if __name__ == "__main__":
	app.run(host='172.31.58.208')
