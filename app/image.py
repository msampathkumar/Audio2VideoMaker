from PIL import Image, ImageDraw, ImageFont

import os

import config


def get_font():
    if os.path.isfile(config.FONT_PATH):
        print(f"Loading found found at {config.FONT_PATH}.")
        font = ImageFont.truetype(config.FONT_PATH, size=config.FONT_SIZE)
    else:
        print(f"Warning: Font not found at {config.FONT_PATH}. Using default font.")
        font = ImageFont.load_default(size=config.FONT_SIZE)  # Fallback to default font
    return font


def get_text_box_dimensions(font, text):
    """Provides the required images dimensions for a given text."""
    # About the Font
    # text = "Hello World"
    left, top, right, bottom = font.getbbox(text)
    width = right - left
    height = bottom - top
    print(f'Image"s Width: {width}, Height: {height} for ("{str(len(text)) + text}")')
    return width, height

def is_text_image_safety_limits(font, text):
    x = config.IMAGE_PADDING_X
    y = config.IMAGE_PADDING_Y

    width, height =  get_text_box_dimensions(font, text)
    if width + x > config.IMAGE_DIMENSION[0]:
        print(f"Warning: Text Image exceed limit for x dimension (text: {text})")
        return False
    if height + y > config.IMAGE_DIMENSION[1]:
        print(f"Warning: Text Image exceed limit for y dimension (text: {text})")
        return False
    return True


def generate_text_image(text_input: str, output_path: str = "output.png") -> str:

    font = get_font()

    img = Image.new(
        mode="RGB", size=config.IMAGE_DIMENSION, color=config.IMAGE_BACKGROUND_COLOR
    )
    draw = ImageDraw.Draw(img)

    y_pos = config.IMAGE_PADDING_Y
    for line in text_input.splitlines():
        if len(line.strip()) > 0:
            # check text image dimension limits
            is_text_image_safety_limits(font, line)
            # Draw the text
            draw.text(
                xy=(config.IMAGE_PADDING_X, y_pos),
                text=line,
                font=font,
                fill=config.IMAGE_TEXT_COLOR,
            )
        # increment the y position
        y_pos += config.IMAGE_PADDING_ROW

    # Save the image
    img.save(output_path)
    # print(f'Generated Image's text: {text_input}')
    return output_path


def generate_multiple_text_images(text_inputs: list, output_paths: list) -> None:
    for text, out_path in zip(text_inputs, output_paths):
        image_path = generate_text_image(text, out_path)
        print(f" - Generated Image: {image_path}")


def create_test_image():
    font = get_font()

    # About the Font
    text = "Hello World"
    width, height = get_text_box_dimensions(font, text)
    # print(f'Font Width: {width}, Height: {height} for ("{text}")')

    estimated_text_length = round(
        (config.IMAGE_DIMENSION[0] / (width / len(text))) * 0.9
    )
    estimated_text_height = round((config.IMAGE_DIMENSION[0] * 0.9) / height)
    print(f"Estimated Max Text length is {estimated_text_length}")
    print(f"Estimated Max Text height is {estimated_text_height}")

    # Create an example image
    text = "".join([str(x) for x in range(10)]) + ";"
    text = text * (1 + int(estimated_text_length / len(text)))
    text = "\n".join([str(x) + "-" + text for x in range(estimated_text_height)])
    image_path = generate_text_image(text, "my_image.png")
    print(f" - Generated Image: {image_path}")


if __name__ == "__main__":
    create_test_image()
