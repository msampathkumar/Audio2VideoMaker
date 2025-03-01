"""
Configuration settings for the application.

This module defines constants and settings used throughout the application,
such as font details, image dimensions, colors, and video parameters.
"""

import os

# --- Font Settings ---
# Specify the path to the font file.
# If the font is not found at this path, a default font will be used.
FONT_PATH = os.path.join("font", "Gupter", "Gupter-Regular.ttf")
# FONT_PATH = os.path.join("font", "Roboto-Medium.ttf") # Example alternative font
FONT_SIZE = 55

# --- Image Settings ---
# Dimensions of the generated images (width, height).
IMAGE_DIMENSION = (1024, 720)

# Padding around the text within the image.
IMAGE_PADDING_X = 10  # Left padding
IMAGE_PADDING_Y = 10  # Top padding
IMAGE_PADDING_ROW = int(FONT_SIZE * 1.04)  # Vertical spacing between text lines

# Colors for the text and background.
IMAGE_TEXT_COLOR = "white"
IMAGE_BACKGROUND_COLOR = "rgb(0, 0, 162)"  # Dark blue background

# --- Video Settings ---
# Frames per second for the generated video.
VIDEO_FPS = 2
