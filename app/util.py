from urllib.parse import quote
import googlemaps
import requests
import random
import time
import json
import urllib
import os

FS_CLIENT_ID = os.environ['FS_CLIENT_ID']
FS_CLIENT_SECRET = os.environ['FS_CLIENT_SECRET']
GMAPS_KEY = os.environ['GMAPS_KEY']
YELP_TOKEN = os.environ['YELP_TOKEN']

FS_SEARCH_URL = 'https://api.foursquare.com/v2/venues/explore'
GMAPS_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
DISTANCE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
YELP_SEARCH = '/v3/businesses/search'

gmaps_client = googlemaps.Client(key=GMAPS_KEY)

date = time.strftime("%Y%m%d")
limit = 5

def yelp_search(lat, lng, query='food'):

	url = '%s%s' % ('https://api.yelp.com', quote(YELP_SEARCH.encode('utf8')))

	headers = {
		'Authorization': 'Bearer %s' % YELP_TOKEN
	}

	data = {
		'latitude' : lat,
		'longitude' : lng,
		'term' : query,
		'radius_filter': '3000',
		'limit': limit
	}

	api_response = requests.get(url, params=data, headers=headers)
	json_response = api_response.json()

	try:
		venue_name = json_response['businesses'][0]['name']
		venue_lat = json_response['businesses'][0]['coordinates']['latitude']
		venue_lng = json_response['businesses'][0]['coordinates']['longitude']
		url = json_response['businesses'][0]['url']

		return venue_name, venue_lat, venue_lng, url

	except:
		pass

def fs_search(lat, lng, query='topPicks'):

	location = '%s,%s' % (str(lat), str(lng))

	fs_data = {
		'll': location,
		'section' : query,
		'price' : '1,2,3',
		'limit': limit
	}

	fs_payload = {
		'client_id': FS_CLIENT_ID, 
		'client_secret': FS_CLIENT_SECRET, 
		'v': date
	}

	query_string = urllib.parse.urlencode(fs_data)
	api_url = '%s?%s' % (FS_SEARCH_URL, query_string)
	api_response = requests.get(api_url, params=fs_payload)
	json_response = api_response.json()

	try:
		venue = json_response['response']['groups'][0]['items'][0]['venue']['name']
		venue_lat = json_response['response']['groups'][0]['items'][0]['venue']['location']['lat']
		venue_lng =  json_response['response']['groups'][0]['items'][0]['venue']['location']['lng']
		url = json_response['response']['groups'][0]['items'][0]['tips'][0]['canonicalUrl']

		return venue, venue_lat, venue_lng, url

	except:
		pass

