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
# GAS_FEED_KEY = os.environ['GAS_FEED_KEY']

FS_SEARCH_URL = 'https://api.foursquare.com/v2/venues/explore'
GMAPS_SEARCH_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
GAS_FEED_URL = 'http://devapi.mygasfeed.com/stations/radius'
DISTANCE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'
YELP_SEARCH_URL = 'https://api.yelp.com/v3/businesses/search'

gmaps_client = googlemaps.Client(key=GMAPS_KEY)

date = time.strftime("%Y%m%d")

def yelp_search(lat, lng):

	location = '%s,%s' % (str(lat), str(lng))

	headers = {
		'Authorization': 'bearer %s' % YELP_TOKEN
	}

	data = {
		'cll': location,
		'term' : 'food',
		'radius_filter': '8000',
		'limit': 10
	}

	response = requests.get(YELP_SEARCH_URL, params=data, headers=headers)


def fs_search(lat, lng):

	location = '%s,%s' % (str(lat), str(lng))

	fs_data = {
		'll': location,
		'section' : 'topPicks',
		'price' : '1,2,3',
		'limit': 10
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
		return venue, venue_lat, venue_lng
	except:
		pass


# def gmaps_search(lat, lng, keyword):

# 	location = '%s,%s' % (str(lat), str(lng))

# 	gmaps_payload = {
# 		'location': '40.801970000000004, -74.46182',
# 		'radius': '1000',
# 		'type': keyword,
# 		# 'keyword': 'bar',
# 		'key': GMAPS_KEY
# 	}

# 	api_response = requests.get(GMAPS_SEARCH_URL, params=gmaps_payload)
# 	json_response = api_response.json()
# 	if len(json_response['results']) == 0:
# 		pass
# 	else:
# 		venue = json_response['results'][0]['name']
# 		return venue

