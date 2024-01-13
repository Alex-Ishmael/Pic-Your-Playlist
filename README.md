# Pic-Your-Playlist
This semeseter I was listening to a lot of music on bus rides and walks between classes. I found myself listening to the same tracks and genres over and over. I wanted to discover music and while Spotify has great tools for recommending tracks based on your listening history or for a genre you had in mind, I wanted something totally fresh. So it sparked an idea for a way to listen to new music in a novel way. But reccomendations still have to come from somewhere and that led me to looking into synesthasia, "a perceptual phenomenon in which stimulation of one sensory or cognitive pathway leads to involuntary experiences in a second sensory or cognitive pathway. For instance, people with synesthesia may experience colors when listening to music, see shapes when smelling certain scents, or perceive tastes when looking at words" (Wikipedia). This then led me to explore color theory and how certain colors, hues, and brightnesses tend to correlate with certain gernes. 

This all culminated in the idea of a program where I could take a picture and the program could look at the color composition and curate a playlist for me directly in my spotify library. It also gave me a great excuse to delve into niche Python libraries and experiment with APIs and image processing. Check out the video below to see it in action!


## How to Run

This program uses OpenCV, Pillow, NumPY, WebColors, and SpotiPy which all need to be installed. I recommend setting up a virtual environment and use PIP installation.

You can create a virtual environment directory using this python command 

`py -m venv .<environment name>`

I used '.PYP' as my environment name as an acronym for Pick your Playlist, but you are free to choose your own name.

Then run this command to activate the enviroment (Windows)

`<venv>\Scripts\Activate.ps1` where venv is the name you choose for your virtual environment

For Mac or Linux visit: https://docs.python.org/3/library/venv.html

Once you have your virtual environment set up, you can install all the libraries we need with these PIP commands

`pip install spotipy --upgrade`
`pip install opencv-python numpy`
`pip install Pillow`
`pip install webcolors`

After installing the pips, you may need to generate a Spotify API token which can be done at https://developer.spotify.com/ 

Additionally, the program accesses Spotify Client ID's, Spotify Usernames and Spotify Client Secrets which should not be shared and are stored as environment variables on my system. THe program is set up to retrieve these variables, but for your own personal use you can either create your own environment variables or explicitly state them.


## How it Works

1) The program starts by asking the user for a path to their image, how many of the most prominent colors the program should consider, and their desired level of popularity in the tracks the playlist includes.
2) Next, the program begins to analyze the image using the `get_prominent_colors` function, which works by using Pillow to collect all the pixel data from the image and then uses a Py Counter to compute the most  
   common pixels in the image.
3) Loop through the dictionary of pixels and their counts and transform the rgb values of each pixel to a color using the `find_approx_color` function. This function then uses the Webcolor library to transform       rgb values to color names from the CSS3 library. The problem is that not every rgb value has a color so if an rgb value does not match the function throws an exception. The way I solved this was by creating a     try catch, that slowly increases red, green, or blue values until we get a match. To ensure that we are increasing the correct value and getting the closest match we use a NumPy linear algebra function that       finds and compares euclidean distances to esnure we get a close match. Additionally, `find_approx_color` takes a parameter called `standard_only`. In the current iteration of PYP we generate recommendations by    matching the color to one of 12 standard colors {red, blue, yellow, purple, orange, green, brown, black, white, gray, beige, pink} who's attributes have been defined from music color theory and rigorous 
   testing. When standard_only is selected, `find_approx_color` finds the closest match to one of those 12 standard colors instead. We make two calls to `find approx_color` one for the compelx_colors to use for      the playlist name and one for simple_colors to use for our playlist recommendations. We add each color to their respective dictionary with the key as the color and the value as the count. This results in two 
   dictionaries, complex_colors and prominent_colors (the most common standard colors).
5) After that, the program uses the user inputted number of colors to consider to loop through the standard colors dictionary and add the number of considered colors to a new dictionary with the value being the      number of songs the color will get in the playlist. This is calculated by looking at the percent each color makes up of the total considered pixels. For example if the user wants to consider 5 colors for the   
   playlist, the progrma iterates through the top 5 most prominent colors and obtains the total considered pixel count which is the sum of the 5 considered color pixel counts. Each color is then\\\\\\\\\\\\\\\\\\

