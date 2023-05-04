# Summary:
This project uses CV in order to process a board of SET cards to find all
possible SETs present.

# How to use
- Clone this repository to your computer
- Install dependencies by running `pip install -r requirements.txt` and `sudo apt-get install python3-pil.imagetk`
- Run [file name] to start
- Point your camera at the set game
- Click to take a picture

# Tips for Usage:
- High-contrast background (preferably black)
- No overlapping cards
- Cards at least a pinky width apart
- Take photo from as close as possible, leaving at least 1/4 of a card of margin
around the edges
- White, constant lighting (minimize shadows)
- As little clutter/background noise as possible

# Dependencies:
Check requirements.txt for all dependencies, also listed below:
- [OpenCV](https://opencv.org/) for image recognition
- [Matplotlib](https://matplotlib.org/) for display
- [NumPy](https://numpy.org/) for internal data management
- [pytest](https://docs.pytest.org/en/7.3.x/contents.html) for unit testing. 
- [Pillow](https://pypi.org/project/Pillow/) for image display.
- Make sure to install the ImageTk module of Pillow (`sudo apt-get install python3-pil.imagetk`)