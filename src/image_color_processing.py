# Color imports
import colorsys, math, os
import webcolors as wc
from webcolors import CSS3_HEX_TO_NAMES

# Pillow and Analysis 
import PIL, base64
from PIL import Image
from collections import Counter
import numpy as np

COMPLEX_COLOR_NAMES = list(CSS3_HEX_TO_NAMES.values()) # Create a list of CSS3 names for colors used to find approximate color matches
STANDARD_COLOR_NAMES = {'red', 'blue', 'green', 'purple', 'beige', 'white', 'black', 'orange', 'pink', 'gray', 'yellow', 'brown'} # 12 standard colors

# Most rgb values do not have a defined name, so we use this function to find the closest CSS3 color to our rgb value
# The standard_only denotes whether we are looking for a match to one of the 12 standard colors or the CS33 colors. 
def find_approx_color(look_up_rgb, standard_only) : 
    approx_color_name = None
    min_dist = float('inf')

    if standard_only == True :
        for name in STANDARD_COLOR_NAMES:
            named_color_rgb = wc.name_to_rgb(name)
            dist = np.linalg.norm(np.array(look_up_rgb) - np.array(named_color_rgb)) # Finds the Euclidean distance between points and updates if we find a closer point (smaller minimum distance)
            
            if dist < min_dist:
                min_dist = dist
                approx_color_name = name
    else :
        for name in COMPLEX_COLOR_NAMES:
            named_color_rgb = wc.name_to_rgb(name)
            dist = np.linalg.norm(np.array(look_up_rgb) - np.array(named_color_rgb)) 

            if dist < min_dist:
                min_dist = dist
                approx_color_name = name

    return approx_color_name


# get_prominent_colors from the image color processing class returns a pair 
# 1st item is a dictionary: the keys are the most prominent standard colors and the value is the number of tracks each color will receive
# 2nd item is a dictionary: the keys are the complex colors obtained and the value is the count of the times each color appears
def get_prominent_colors(image_path, num_considered_colors):

    complex_colors = dict() 
    standard_colors = dict()

    img = Image.open(image_path)    
    pixels = list(img.getdata())
    print("# of pixels", len(pixels))

    # Count occurrences of each pixel represented as an rgb value
    pixel_count = Counter(pixels)
    most_common_pixels = pixel_count.most_common(100000)

  
    # Use our prev defined function to find the top complex and simple colors and insert them into a dictionary,
    # with the color as the key and the value being the frequency of the color's appearance
    for pixel in most_common_pixels:
        if (len(complex_colors) < 20) :
            approx_complex = (find_approx_color(pixel[0], standard_only = False))
            complex_colors[approx_complex] = complex_colors.get(approx_complex, 0) + pixel[1]
        
        approx_simple = find_approx_color(pixel[0], standard_only = True) 
        standard_colors[approx_simple] = standard_colors.get(approx_simple, 0) + pixel[1] # Add's to the count of a color
        
    total_color_count = 0
    considered_colors_count = 0
    prominent_colors = dict()
    i = 0

    for color, color_count in standard_colors.items() :
        if (i < num_considered_colors) :
            considered_colors_count += color_count
        i += 1
        total_color_count += color_count # Should be commented out, just for reassurance purposes
    
    print("total simple color count:",total_color_count)
    print("considered color count:", considered_colors_count)

    i = 0

    # Getting percentages of our considered colors
    for color, color_count in standard_colors.items() :
        if (i >= num_considered_colors) :
            break
        if (color_count/considered_colors_count) * 100 < 1 :
            print(color, color_count/considered_colors_count)
            i += 1
            continue
        if (color_count/considered_colors_count) * 10 < 1 :
            prominent_colors[color] = 1
        else :
            prominent_colors[color] = math.floor((color_count/considered_colors_count) * 10)
        print(color, color_count/considered_colors_count)
        i += 1

    print("prominent colors:",prominent_colors)
    print("complex colors:", complex_colors)

    pair = (prominent_colors, complex_colors)
    
    return pair 

# Returns a base64 representation of the image for upload throught the Spotify API
def image_to_base64(image_path) :
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
        return encoded_image.decode('utf-8') 
    
# Compresses the image by reducing quality in increments of 5 and returns the new image to the output path
def compress_image(input_path, output_path):
    # Opening the image
    image = Image.open(input_path)

    quality = 90

    # 150 because base64 increases size 
    TARGET_KB = 180  
    while True:
        # Save the image with the current quality level
        image.save(output_path, quality=quality)
        file_size = os.path.getsize(output_path)

        # Break the loop if the target size is achieved or if the quality is 0
        if file_size <= TARGET_KB * 1024 or quality == 0:                             
            break
        quality -= 5

    print("file size in bytes: ", file_size, "file size in KB:", file_size/1024)
