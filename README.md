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

After installing the PIP, simply run the main.py file

## How it Works
