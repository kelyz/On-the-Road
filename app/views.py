from flask import session, request, render_template, jsonify
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
		#Receive all of the latitude and longitude pairs in between an origin and destination
		data = request.json
		#Divide the distance from origin to destination into 10 parts 
		#to spread out the different venues avaiable on the map
		#and store the latitude, longitude pairs in a dictionary
		step_unit = int(len(data) // 10)
		step_unit = step_unit if not step_unit % 2 else step_unit - 1
		data_dict = {data[i]: data[i+1] for i in range(0, len(data), step_unit)}

		#Create a query cookie
		query = session['query']

		#Use utility functions to find available venues at the latitude, longitude pairs
		fs_places = [util.fs_search(lat, lng) for lat,lng in data_dict.items() 
					if util.fs_search(lat, lng) != None]

		yelp_places = [util.yelp_search(lat, lng, query) for lat,lng in data_dict.items() 
					  if util.yelp_search(lat, lng, query) != None]

		#Remove duplicate venues
		places = list(set(fs_places + yelp_places))

		return jsonify(places)

	else:
		#Get origin from index page
		start = request.args.get('origin')
		origin = gmaps_client.geocode(start)
		origin_lat = origin[0]['geometry']['location']['lat']
		origin_lng = origin[0]['geometry']['location']['lng']

		#Get destination from index page
		end = request.args.get('destination')
		destination = gmaps_client.geocode(end)
		dest_lat = destination[0]['geometry']['location']['lat']
		dest_lng = destination[0]['geometry']['location']['lng']

		#Get query from index page if available
		query = request.args.get('query')
		session['query'] = query
		
		return render_template(
			'search.html', start=start, end=end, originlat=origin_lat, originlng=origin_lng, 
			endlat=dest_lat, endlng=dest_lng
		)

@app.errorhandler(404)
def page_not_found(e):
	return "Page not found"


