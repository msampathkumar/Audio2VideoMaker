"""
Configuration settings for the application.

This module defines constants and settings used throughout the application,
such as font details, image dimensions, colors, and video parameters.
"""

import os

colors = {
    # Standard Colors
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "gray": (128, 128, 128),
    "grey": (128, 128, 128),  # Alternate spelling
    "silver": (192, 192, 192),
    "maroon": (128, 0, 0),
    "olive": (128, 128, 0),
    "purple": (128, 0, 128),
    "teal": (0, 128, 128),
    "navy": (0, 0, 128),
    "orange": (255, 165, 0),
    "lime": (0, 255, 0),
    "aqua": (0, 255, 255),
    "fuchsia": (255, 0, 255),
    # Pastel Colors
    "pastel_pink": (255, 182, 193),  # Light Pink
    "pastel_blue": (173, 216, 230),  # Light Blue
    "pastel_green": (144, 238, 144),  # Light Green
    "pastel_yellow": (255, 255, 224),  # Light Yellow
    "pastel_purple": (221, 160, 221),  # Light Purple
    "pastel_orange": (255, 228, 196),  # Light Orange
    "pastel_peach": (255, 218, 185),
    "pastel_lavender": (230, 230, 250),
    "pastel_mint": (189, 252, 201),
    "pastel_coral": (240, 128, 128),
    "pastel_sky_blue": (135, 206, 250),
    "pastel_seafoam": (143, 188, 143),
    "pastel_beige": (245, 245, 220),
    "pastel_cream": (255, 253, 208),
    "pastel_apricot": (251, 206, 177),
    "pastel_periwinkle": (204, 204, 255),
    "pastel_rose": (255, 228, 225),
    "pastel_mauve": (224, 176, 255),
    "pastel_turquoise": (175, 238, 238),
}

# --- Font Settings ---
# Specify the path to the font file.
# If the font is not found at this path, a default font will be used.
# FONT_PATH = os.path.join("font", "Gupter", "Gupter-Regular.ttf")
FONT_PATH = os.path.join("font", "Tinos", "Tinos-Regular.ttf")
# FONT_SIZE = 62
FONT_SIZE = 42

# --- Image Settings ---
# Dimensions of the generated images (width, height).
# IMAGE_DIMENSION = (1920, 1350)
IMAGE_DIMENSION = (1024, 720)

# Padding around the text within the image.
IMAGE_PADDING_X = 10  # Left padding
IMAGE_PADDING_Y = 10  # Top padding
IMAGE_PADDING_ROW = int(FONT_SIZE * 1.04)  # Vertical spacing between text lines

# Colors for the text and background.
IMAGE_TEXT_COLOR = colors["white"]
IMAGE_BACKGROUND_COLOR = colors["navy"]  # "rgb(0, 0, 162)"  # Dark blue background

# Text
IMAGE_TEXT_MAX_LINE_CHAR_LIMIT = 45  # Maximum characters per line
IMAGE_TEXT_MAX_LINES_LIMIT = 16  # Maximum number of lines

# --- Video Settings ---
# Frames per second for the generated video.
VIDEO_FPS = 2
