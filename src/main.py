import image_color_processing as icp
import spotify_utils as su
import time, math, sys, os

PLAYLIST_COVER = ".PYP\img_to_upload.jpg"

# Print intro with a smooth text scrolling animation and get the path to the image
INTRO = "Hi, it's time to 'Pic' your Playlist! First write the path to your chosen image. \nNext write the number of colors you'd like to consider when curating your playlist.\nAfter that choose the range of popularity (0-100) for your tracks."

for char in INTRO :
    sys.stdout.write(char)
    sys.stdout.flush()
    time.sleep(0.060)
print("\n") 
time.sleep(0.100)
image_path = input("Path to image:")
level_of_pop = int(input("Popularity from 0-100:"))
num_considered_colors = int(input("Number of colors to consider:"))

# Gets the prominent colors to consturct the playlist and the complex colors to name it (see image_color_processing for more details about the funciton)
# We pass in how many colors we want to take into consideration in creating our playlist
color_data = icp.get_prominent_colors(image_path, num_considered_colors)
prominent_colors = color_data[0] 
complex_colors = color_data[1]

# Image must be compressed to fit the 256kb size limit imposed by the Spotify API
icp.compress_image(input_path = image_path, output_path = PLAYLIST_COVER)

# Then we use our spotify utility functions to make the playlist
su.make_playlist(prominent_colors = prominent_colors, complex_colors = complex_colors, image_path = PLAYLIST_COVER, popularity = level_of_pop)

