"""
Image generation module for creating text-based images.

This module provides functions to generate images with text,
handle font loading, and manage text layout within image boundaries.
"""

import logging
import os
import time

from PIL import Image, ImageDraw, ImageFont

import config
import text_manager
from utils import Status

logger = logging.getLogger(__name__)


def get_font() -> ImageFont.FreeTypeFont:
    """
    Loads the specified font or falls back to a default font.

    Returns:
        An ImageFont object.
    """
    if os.path.isfile(config.FONT_PATH):
        logger.debug(f"{Status.OK} Loading font from: {config.FONT_PATH}")
        font = ImageFont.truetype(config.FONT_PATH, size=config.FONT_SIZE)
    else:
        logger.warning(
            f"{Status.WARNING} Font not found at {config.FONT_PATH}. Using default font."
        )
        font = ImageFont.load_default()
    return font


def get_text_box_dimensions(font: ImageFont.FreeTypeFont, text: str) -> tuple[int, int]:
    """
    Calculates the dimensions (width, height) of a text box.

    Args:
        font: The font used for rendering the text.
        text: The text to measure.

    Returns:
        A tuple containing the width and height of the text box.
    """
    left, top, right, bottom = font.getbbox(text)
    width = int(right - left)
    height = int(bottom - top)
    logger.debug(
        f"Text box dimensions for '{text[:20]}...': Width={width}, Height={height}"
    )
    return width, height


def is_text_within_image_bounds(font: ImageFont.FreeTypeFont, text: str) -> bool:
    """
    Checks if the text fits within the image boundaries.

    Args:
        font: The font used for rendering the text.
        text: The text to check.

    Returns:
        True if the text fits within the image, False otherwise.
    """
    x_padding = config.IMAGE_PADDING_X
    y_padding = config.IMAGE_PADDING_Y

    width, height = get_text_box_dimensions(font, text)
    if width + x_padding * 2 > config.IMAGE_DIMENSION[0]:
        logger.warning(
            f"{Status.WARNING} Text '{text[:20]}...' exceeds image width limit."
        )
        return False
    if height + y_padding * 2 > config.IMAGE_DIMENSION[1]:
        logger.warning(
            f"{Status.WARNING} Text '{text[:20]}...' exceeds image height limit."
        )
        return False
    return True


def generate_text_image(text_input: str, output_path: str) -> str:
    """
    Generates an image with the given text.

    Args:
        text_input: The text to render on the image.
        output_path: The path to save the generated image.

    Returns:
        The path to the generated image.
    """
    text_input = text_input.rstrip()  # Remove trailing spaces/line breaks
    txt_mgr = text_manager.TextManager()
    txt_mgr.set_text(text_input)  # Validate text using TextManager
    time.sleep(0.1)  # Small delay to allow for text validation

    font = get_font()
    img = Image.new(
        mode="RGB", size=config.IMAGE_DIMENSION, color=config.IMAGE_BACKGROUND_COLOR
    )
    draw = ImageDraw.Draw(img)

    y_pos = config.IMAGE_PADDING_Y
    for line in text_input.splitlines():
        # Remove only trailing spaces/line breaks
        line = line.rstrip()
        # Check if the line fits within the image
        if not is_text_within_image_bounds(font, line):
            logger.warning(
                f"{Status.WARNING} Line '{line[:20]}...' may not fit perfectly in the image."
            )
        draw.text(
            xy=(config.IMAGE_PADDING_X, y_pos),
            text=line,
            font=font,
            fill=config.IMAGE_TEXT_COLOR,
        )
        y_pos += config.IMAGE_PADDING_ROW

    img.save(output_path)
    logger.debug(f"{Status.OK} Image generated at: {output_path}")
    logger.debug(f" - Image text: {text_input[:50]}...")
    return output_path


def generate_multiple_text_images(
    text_inputs: list[str], output_paths: list[str]
) -> None:
    """
    Generates multiple text images.

    Args:
        text_inputs: A list of text strings.
        output_paths: A list of output paths for the images.
    """
    for text, out_path in zip(text_inputs, output_paths):
        image_path = generate_text_image(text, out_path)
        print(f"{Status.OK} Generated Image: {image_path}")


def create_test_image() -> None:
    """
    Creates a test image with sample text to demonstrate functionality.
    """
    font = get_font()
    sample_text = "Hello World"
    width, height = get_text_box_dimensions(font, sample_text)
    logger.debug(
        f"Sample text '{sample_text}' dimensions: Width={width}, Height={height}"
    )

    estimated_text_length = 42
    estimated_text_height = 12
    logger.debug(f"Estimated max text length: {estimated_text_length}")
    logger.debug(f"Estimated max text height: {estimated_text_height}")

    # Create an example image
    text_line = "".join([str(x) for x in range(10)]) + ";"
    text_line = text_line * 10
    text = "\n".join(
        [str(x + 1) + "-" + text_line for x in range(estimated_text_height)]
    )
    image_path = generate_text_image(text, "test_image.png")
    print(f"{Status.OK} Generated test image: {image_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    create_test_image()
