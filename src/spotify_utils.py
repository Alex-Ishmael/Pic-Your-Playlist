# image-color imports
import image_color_processing as icp
import webcolors as wc

# spotipy imports
import spotipy, requests, urllib3, time, math, sys, os
from spotipy.oauth2 import SpotifyOAuth


SPOTIPY_REDIRECT_URI=os.environ.get('SPOTIPY_REDIRECT_URI')
SPOTIPY_CLIENT_ID=os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET=os.environ.get('SPOTIPY_CLIENT_SECRET')
USERNAME = os.environ.get('SPOTIFY_USERNAME')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="playlist-modify-public,ugc-image-upload"))

def make_playlist_name(complex_colors) :
    # First we sort the array and create our data structures
    complex_colors_sorted = dict(reversed(sorted(complex_colors.items(), key=lambda x:x[1])))
    playlist_name = str()
    seen_standard_colors = set()

    # Base Case - if there is only one color, we simply return it
    if (len(complex_colors_sorted) == 1) : 
        return next(iter(complex_colors_sorted))    
    
    for complex_color, value in complex_colors_sorted.items() :
        # We simplify the complex colors using the find_approx_color with standard_only set to true and add them to a set
        # This is to ensure we don't output a playlist name wtih slight variations of the same color ex: "grav, lightgray, dimgray"
        standard_color = icp.find_approx_color(wc.name_to_rgb(complex_color), standard_only = True) 
        if (standard_color not in seen_standard_colors) : 
            playlist_name += complex_color + ", "
            seen_standard_colors.add(standard_color)
    print(playlist_name[:-2])
    return playlist_name[:-2] # Removes the last whitespace and comma



# Makes the playlist through the Spotify API using SpotiPy
def make_playlist(prominent_colors, complex_colors, image_path, popularity) :
    pyp_name = make_playlist_name(complex_colors)
    playlist = sp.user_playlist_create(user = USERNAME, name = pyp_name , public = True, collaborative = False, description = "Enjoy!")
    pyp_playlist = playlist["id"]
    sp.playlist_upload_cover_image(playlist_id = pyp_playlist, image_b64 =  icp.image_to_base64(image_path))  # Max image size is 256KB
   

    for key, value in prominent_colors.items() :
        recs = generate_recommendations(key, value, popularity)
        tracks_to_add = list()
        for i in range(value) :
            print(key, "->", recs["tracks"][i]["name"], "by", recs["tracks"][i]["album"]["artists"][0]["name"])
            tracks_to_add.append(recs["tracks"][i]["id"])
        sp.playlist_add_items(playlist_id=pyp_playlist, items=tracks_to_add)
        # print("track_ids",tracks_to_add)
        time.sleep(5)
  
# Function returns the API call we make to get recommendations using the SpotiPy wrapper
# Has defined attributes for each of the 12 standard colors based on rigorous testing 
def generate_recommendations(color, limit, popularity):
    min_energy = 0
    max_energy = 0
    min_valence = 0
    max_valence = 0
    min_tempo = 0
    max_tempo = 0
    min_loud = 0
    max_loud = 0
    genres = {}
    
    if color == "red" :
        min_energy = 0.9
        max_energy = 1
        min_valence = 0
        max_valence = 1
        min_tempo = 95
        max_tempo = 250
        min_loud = -7
        max_loud = 0
        genres = {"rock", "hardcore", "hard-rock", "alt-rock", "garage"}
    
    if color == "pink" :
        min_energy = 0.6
        max_energy = 1
        min_valence = 0.65
        max_valence = 1
        min_tempo = 50
        max_tempo = 250
        min_loud = -25
        max_loud = 0
        genres = {"pop", "romance", "dance", "power-pop"}
    
    if color == "blue" :
        min_energy = 0
        max_energy = 0.6
        min_valence = 0
        max_valence = 0.5
        min_tempo = 0
        max_tempo = 100
        min_loud = -25
        max_loud = 0
        genres = {"blues", "sad", "soul", "ambient", "rainy-day"}

    if color == "green" :
        min_energy = 0.3
        max_energy = 0.8
        min_valence = 0.5
        max_valence = 1
        min_tempo = 50
        max_tempo = 200
        min_loud = -25
        max_loud = 0
        genres = {"acoustic","folk", "chill", "ambient", "indie"}
    
    if color == "purple" :
        min_energy = 0.5
        max_energy = 1
        min_valence = 0.5
        max_valence = 1
        min_tempo = 70
        max_tempo = 200
        min_loud = -20
        max_loud = 0
        genres = {"funk", "disco", "groove", "trance", "electronic"}

    if color == "beige" :
        min_energy = 0
        max_energy = 0.5
        min_valence = 0
        max_valence = 0.7
        min_tempo = 0
        max_tempo = 100
        min_loud = -40
        max_loud = 0
        genres = {"sleep", "ambient", "study", "classical" }
    
    if color == "white" :
        min_energy = 0
        max_energy = 0.7
        min_valence = 0.5
        max_valence = 1
        min_tempo = 0
        max_tempo = 180
        min_loud = -40
        max_loud = 0
        genres = {"classical", "gospel", "opera", "piano", "jazz"}

    if color == "black" :
        min_energy = 0
        max_energy = 1
        min_valence = 0
        max_valence = 1
        min_tempo = 0
        max_tempo = 240
        min_loud = -40
        max_loud = 0
        genres = {"metalcore", "black-metal", "goth", "metal"}
    
    if color == "orange" :
        min_energy = 0.3
        max_energy = 1
        min_valence = 0
        max_valence = 0.7
        min_tempo = 0
        max_tempo = 170
        min_loud = -40
        max_loud = 0
        genres = {"indie", "hip-hop", "psych-rock", "r-n-b", "trip-hop"}

    if color == "gray" :
        min_energy = 0
        max_energy = 1
        min_valence = 0
        max_valence = 0.6
        min_tempo = 0
        max_tempo = 240
        min_loud = -40
        max_loud = 0
        genres = {"industrial", "opera", "piano", "ambient"}
    
    if color == "yellow" :
        min_energy = 0.5
        max_energy = 1
        min_valence = 0.4
        max_valence = 1
        min_tempo = 50
        max_tempo = 200
        min_loud = -40
        max_loud = 0
        genres = {"happy", "indie-pop", "summer", "synth-pop", "dance"}

    if color == "brown" :
        min_energy = 0
        max_energy = 0.7
        min_valence = 0
        max_valence = 0.5
        min_tempo = 0
        max_tempo = 150
        min_loud = -40
        max_loud = -10
        genres = {"folk", "singer-songwriter", "acoustic", "country"}

    return sp.recommendations(seed_genres=genres, limit = limit, min_popularity = popularity, min_energy = min_energy,
                        max_energy = max_energy, min_valence = min_valence, max_valence = max_valence,
                        min_tempo = min_tempo, max_tempo = max_tempo, min_loud = min_loud, max_loud = max_loud)
    
