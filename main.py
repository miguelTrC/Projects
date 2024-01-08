from dotenv import load_dotenv
import os 
import base64 #built in module in python
from requests import post, get #for sending POST
import json

# Loading the file .env from same directory
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

#will send a request body, in return we
#get a json object file with info

#define, function/method

#encoding and decoding is converting strings to bytes, 
#used to transfer info over a network,       'json stuff'
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    #sending a POST request
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64, 
        "Content-Type": "application/x-www-form-urlencoded"

    }
    data = {"grant_type":"client_credentials"}
    #body of request below
    result = post(url, headers=headers, data=data)

    #will recieve a Json data in a field of .content, which we will convert to string
    json_result = json.loads(result.content)
    token = json_result["access_token"]
        #access token valid for 1 hour (3600sec), after expire, request new one
    return token

#token needs to be used whenever need to send/request
#this will be our header
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}
                #format from 'Access token' documentation


#endpoint == url 
def search_for_artist(token, artist_name): 
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    #q is the value such as artist/album/track ect, if 
    #was looking for multiple values, can do =artist,track
    #f""  is a final string

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    #json_result is a string containing the artist info

    if len(json_result) == 0:
        print("No artist found with the name given.")
        return None 
    return json_result[0]



def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result
    

token = get_token()
result = search_for_artist(token, "The Weeknd")
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)
print(songs)


for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")