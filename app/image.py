from PIL import Image, ImageDraw, ImageFont

import os

import config


def get_font():
    if os.path.isfile(config.FONT_PATH):
        try:
            print(f"Loading found found at {config.FONT_PATH}.")
            font = ImageFont.truetype(config.FONT_PATH, config.FONT_SIZE)
        except IOError:
            print(f"Warning: Font not found at {config.FONT_PATH}. Using default font.")
            font = ImageFont.load_default()  # Fallback to default font
    else:
        font = ImageFont.load_default()
    return font


def get_text_box_dimensions(font, text_line):

    # About the Font
    text = "Hello World"
    left, top, right, bottom = font.getbbox(text)
    width = right - left
    height = bottom - top
    print(f'Font Width: {width}, Height: {height} for ("{text}")')
    return width, height


def generate_text_image(text_input: str, output_path: str = "output.png") -> str:

    font = get_font()

    img = Image.new(
        mode="RGB", size=config.IMAGE_DIMENSION, color=config.IMAGE_BACKGROUND_COLOR
    )
    draw = ImageDraw.Draw(img)

    x_pos = config.IMAGE_PADDING_TOP
    y_pos = config.IMAGE_PADDING_LEFT
    for line in text_input.splitlines():
        draw.text((x_pos, y_pos), line, font=font, fill=config.IMAGE_TEXT_COLOR)
        y_pos += config.IMAGE_PADDING_ROW

    img.save(output_path)
    # print(f'Generated Image"s text: {text_input}')
    return output_path


def generate_multiple_text_images(text_inputs: list, output_paths: list) -> None:
    for text, out_path in zip(text_inputs, output_paths):
        image_path = generate_text_image(text, out_path)
        print(f" - Generated Image: {image_path}")


def create_test_image():
    font = get_font()

    # About the Font
    text = "Hello World"
    width, height = get_text_box_dimensions(font, text_line=text)
    # print(f'Font Width: {width}, Height: {height} for ("{text}")')

    # Create an example image
    text = ("".join([str(x) for x in range(10)]) + ";") * 25
    text = "\n".join([str(x) + "-" + text for x in range(25)])
    image_path = generate_text_image(text, "my_image.png")
    print(f" - Generated Image: {image_path}")


if __name__ == "__main__":
    create_test_image()
