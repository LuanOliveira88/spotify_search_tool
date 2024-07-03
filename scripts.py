import base64
from os import getenv
from urllib.parse import urljoin

from dotenv import load_dotenv
from requests import get, post

load_dotenv()


def get_token():
	url = getenv('SPOTIFY_TOKEN_URL')
	client_id = getenv('CLIENT_ID')
	client_secret = getenv('CLIENT_SECRET')
	auth_string = client_id + ':' + client_secret
	auth_bytes = auth_string.encode('utf-8')
	auth_b64 = str(base64.b64encode(auth_bytes), 'utf-8')

	headers = {
		'Authorization': 'Basic ' + auth_b64,
		'Content-Type': 'application/x-www-form-urlencoded'
	}
	data = {
		'grant_type': 'client_credentials'
	}
	response = post(url=url, headers=headers, data=data)
	# if 'application/json' in response.headers:
	return response.json()['access_token']


def get_auth_header():
	token = get_token()
	headers = {
		'Authorization': f'Bearer {token}'
	}

	return headers


def search_for_artist(artist_name):
	endpoint = '/search'
	url = get_url(endpoint)
	headers = get_auth_header()
	query = f'?q={artist_name}&type=artist&limit=1'
	query_url = url + query
	response = get(url=query_url, headers=headers)
	result = response.json()
	return result['artists']


def get_artist_id(artist_name):
	return search_for_artist(artist_name)['items'][0]['id']


def get_artist_genres(artist_name):
	return search_for_artist(artist_name)['genres']


def get_search_url():
	return get_url(endpoint='/search')


def get_album_url(album_id):
	return get_url(f'/albums/{album_id}/tracks')


def get_tracks_from_album_id(album_id):
	url = get_album_url(album_id)
	headers = get_auth_header()
	response = get(url=url, headers=headers)
	if response.status_code == 200:
		result = response.json()
		tracks = result['items']
		for track in tracks:
			track_name = track['name']
			yield track_name
	else:
		print(f"Erro na requisição: {response.status_code}")
		print(response.json())


def scrape_artist_tracks(artist_name):
	_albums = get_artist_albums(artist_name)
	for album in _albums:
		album_name = album['name']
		album_id = album['id']
		for track_name in get_tracks_from_album_id(album_id):
			data = {
				'artist_name': artist_name,
				'album_name': album_name,
				'track_name': track_name
			}
			yield data


def get_artist_album(artist_name, album_name):
	url = get_search_url()
	headers = get_auth_header()
	params = {
		'q': f"album:{album_name} artist:{artist_name}",
		'type': "album",
		'limit': 1
	}

	response = get(url=url, headers=headers, params=params)
	if response.status_code == 200:
		results = response.json()
		albums = results['albums']['items']
		if albums:
			album = albums[0]
			album = albums[0]
			print(f"Nome do Álbum: {album['name']}")
			print(f"Artista: {album['artists'][0]['name']}")
			print(f"ID do Álbum: {album['id']}")
			print(f"Data de Lançamento: {album['release_date']}")
			print(f"Número de Faixas: {album['total_tracks']}")
			print(f"URL do Spotify: {album['external_urls']['spotify']}")
			print('Tracks List:')
			get_tracks_from_album_id(album['id'])
		else:
			print("Álbum não encontrado")
	else:
		print(f"Erro na requisição: {response.status_code}")
		print(response.json())


def save(content_text, filename='index.html'):
	with open('index.html', 'w') as file:
		file.write(content_text)
		print(f'A resposta dessa requisição é um html que foi salvo em {filename}')


def get_user_auth_code():
	auth_url = getenv('SPOTIFY_AUTH_URL')
	params = {
		'client_id': getenv('CLIENT_ID'),
		'response_type': 'code',
		'redirect_uri': getenv('REDIRECT_URI'),
		'scope': "user-library-read"
	}
	response = get(url=auth_url, params=params)
	if response.status_code == 200:
		if response.headers['content-type'] == 'text/html;charset=utf-8':
			save(content_text=response.text)

		else:
			print(response.headers['content-type'])
			return response.json()['code']
	else:
		print(f"Erro na requisição: {response.status_code}")
		print(response.json())
		return None


def get_url(endpoint):
	url = urljoin(getenv('SPOTIFY_API_URL'), f"v1/{endpoint}")
	return url


def get_auth_access_token():
	url = getenv('SPOTIFY_AUTH_URL')
	code = get_user_auth_code()
	if code:
		headers = get_auth_header()
		data = {
			'grant_type': 'authorization_code',
			'code': code,
			'redirect_uri': getenv("REDIRECT_URI")
		}
		response = post(url=url, headers=headers, data=data)


def get_artist_albums(artist_name):
	artist_id = get_artist_id(artist_name)
	url = get_url(f'/artists/{artist_id}/albums')

	response = get(url=url, headers=get_auth_header())
	if 'content-type' in response.headers:
		if 'json' in response.headers['content-type']:
			results = response.json()['items']
			_albums = [
				{
					'name': item['name'],
					'id': item['id']
				} for item in results
			]
			return _albums
