import json
import spotipy
import spotipy.util as util


# Client Settings
client_id = '8654953b081e4a93be3dc54a0bb94b76'
client_secret = 'ddf018ff1b3b4681878b036d6518ac29'
redirect_uri = 'http://google.com/'


# Username & Scope, and Prompt for user permission
username = 'ali.yo12324'
scope = 'user-library-read user-read-playback-state user-modify-playback-state'
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)


# Create Spotify Object
spotifyObject = spotipy.Spotify(auth=token)


# Get current user data
def current_user_data(spotifyObject):
	return spotifyObject.current_user()

# Get current user devices
def current_user_devices(spotifyObject):
	return spotifyObject._get('me/player/devices')

# Get currently played music data
def currently_played(spotifyObject):
	return spotifyObject._get('me/player/currently-playing')

# Get currently active device
def current_active_device(spotifyObject):
	for device in current_user_devices(spotifyObject)['devices']:
		if device['is_active'] == True:
			current_device = device
		return current_device


# Play music
def play(spotifyObject):
	spotifyObject._put('me/player/play')

# Play certain track
def play_track(spotifyObject, uri, device_id):
	data = {
		'uris': [uri],
		'device_ids': [device_id]
	}
	spotifyObject._put('me/player/play', payload=data)

# Pause music
def pause(spotifyObject):
	spotifyObject._put('me/player/pause')

# Transfer Playback
def transfer_playback(spotifyObject, device_id):
	data = {
		'device_ids': [device_id],
		'play': True
	}
	spotifyObject._put('me/player', payload=data)


# Search Song
def search_song(spotifyObject, query):
	
	current_market = current_user_data(spotifyObject)['country']
	current_device = current_active_device(spotifyObject)['id']

	searchResult = spotifyObject.search(query, type='track', limit=1, market=current_market)
	track_uri = searchResult['tracks']['items'][0]['uri']
	print("URI:", track_uri)
	play_track(spotifyObject, track_uri, current_device)


# Showing User Data
def show_user_data(user=current_user_data(spotifyObject)):
	print()
	print("Country:", user['country'])
	print("Display Name:", user['display_name'])
	print("External URL:", user['external_urls']['spotify'])
	print("User ID:", user['id'])
	print("Spotify URI:", user['uri'])


# Testing App
while True:
	print("Spotify Controller")
	print("1. Show User Data")
	print("2. Show Devices Available")
	print("3. Show Currently Played Music Data")
	print("4. Show Current Active Device")
	print("5. Play Music")
	print("6. Pause Music")
	print("7. Transfer Playback (give ID)")
	print("8. Search Songs")
	inp = input("Choose Option: ")
	
	if (inp == "1"):
		print(json.dumps(current_user_data(spotifyObject), sort_keys=True, indent=4))
		show_user_data()
	if (inp == "2"):
		print(json.dumps(current_user_devices(spotifyObject), sort_keys=True, indent=4))
	if inp == "3":
		print(json.dumps(currently_played(spotifyObject), sort_keys=True, indent=4))
	if inp == "4":
		print(json.dumps(current_active_device(spotifyObject), sort_keys=True, indent=4))
	if inp == "5":
		print(json.dumps(play(spotifyObject), sort_keys=True, indent=4))
	if inp == "6":
		print(json.dumps(pause(spotifyObject), sort_keys=True, indent=4))
	if inp == "7":
		device = input("Device ID: ")
		transfer_playback(spotifyObject, device)
	if inp == "8":
		query = input("Search: ")
		search_song(spotifyObject, query)

	print()
	print()