"""
Main application entry point for the AudioVideoMaker.

This module orchestrates the image and video generation processes
based on a provided configuration file.
"""

import logging
import sys

import validation
import image
import video

# --- Configuration ---
DEBUG_FLAG = False  # Set to True for detailed debug logs

# --- Logging Setup ---
logging.basicConfig(
    level=logging.DEBUG if DEBUG_FLAG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("AudioVideoMaker")


def main(
    config: validation.GetConfig,
    generate_image: bool = True,
    generate_video: bool = False,
) -> None:
    """
    Main function to generate images and/or video based on the configuration.

    Args:
        config: The configuration object containing settings and data.
        generate_image: Whether to generate images.
        generate_video: Whether to generate a video.
    """
    logger.debug("Starting AudioVideoMaker process...")
    config_data = config

    # Generate images
    if generate_image:
        logger.debug("Generating images...")
        image.generate_multiple_text_images(
            text_inputs=config_data.txt_image_text,
            output_paths=config_data.txt_image_names,
        )
        logger.debug("Image generation completed.")

    # Generate video
    if generate_video:
        logger.debug("Generating video...")
        video.generate_video_with_audio(
            images=config_data.txt_image_names,
            durations=config_data.txt_image_durations,
            output_path=config_data.video_file_path,
            audio_path=config_data.audio_file_path,
        )
        logger.debug("Video generation completed.")

    logger.debug("AudioVideoMaker process finished.")


def parse_command_line_arguments() -> tuple[str | None, bool, bool]:
    """
    Parses command-line arguments to determine the configuration file and actions.

    Returns:
        A tuple containing:
        - The configuration file path (or None if not found).
        - Whether to generate images.
        - Whether to generate a video.
    """
    config_path = None
    generate_image = False
    generate_video = False

    for arg in sys.argv:
        if arg.endswith(".yaml"):
            config_path = arg
        elif arg == "image":
            generate_image = True
        elif arg == "video":
            generate_video = True
        elif arg == "test":
            image.create_test_image()
            sys.exit()

    return config_path, generate_image, generate_video


if __name__ == "__main__":
    logger.debug("-" * 50)
    config_path, generate_image, generate_video = parse_command_line_arguments()

    if not config_path:
        logger.error("Missing config .yaml input file!")
        sys.exit(1)

    logger.debug(f"Found provided input config file: {config_path}")

    try:
        config_info = validation.GetConfig(config_path)
        # config_info.show_config() # Uncomment to show the config info
        main(
            config=config_info,
            generate_image=generate_image,
            generate_video=generate_video,
        )
    except validation.ConfigValidationError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

    logger.debug("-" * 50)
