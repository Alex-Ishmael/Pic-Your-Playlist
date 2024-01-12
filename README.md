# Pic-Your-Playlist
A program that curates a playlist for a user using the Spotify API based on the color data of a user submitted photo obtained using Image Processing with OpenCV, Pillow libraries and data analysis using NumPY.

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
