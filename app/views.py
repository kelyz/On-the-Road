from flask import request, render_template, jsonify
from app import app
from app import util
import requests
import random
import time
import json
import urllib.parse
import googlemaps
import os

GMAPS_KEY = os.environ['GMAPS_KEY']
GMAPS_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
gmaps_client = googlemaps.Client(key=GMAPS_KEY)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/search', methods=['GET','POST'])
def search():
	if request.method == 'POST':
		places = []
		gas_stations = []
		data = request.json
		step_unit = int(len(data) // 10)
		step_unit = step_unit if not step_unit % 2 else step_unit - 1
		data_dict = {data[i]: data[i+1] for i in range(0, len(data), step_unit)}
		
		for lat,lng in data_dict.items():
			places.append(util.fs_search(lat, lng))

		return jsonify(places)

	else:
		start = request.args.get('origin')
		origin = gmaps_client.geocode(start)
		origin_lat = origin[0]['geometry']['location']['lat']
		origin_lng = origin[0]['geometry']['location']['lng']

		end = request.args.get('destination')
		destination = gmaps_client.geocode(end)
		dest_lat = destination[0]['geometry']['location']['lat']
		dest_lng = destination[0]['geometry']['location']['lng']
		
		return render_template(
			'search.html', start=start, end=end, originlat=origin_lat, originlng=origin_lng, 
			endlat=dest_lat, endlng=dest_lng
		)

@app.errorhandler(404)
def page_not_found(e):
	return "Page not found"


