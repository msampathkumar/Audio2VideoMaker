import os
import logging

from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips

import config
from utils import Status

logger = logging.getLogger(__name__)


def get_image_clip(image_path: str, duration: float) -> ImageClip:
    """
    Creates an ImageClip from an image file.

    Args:
        image_path: The path to the image file.
        duration: The duration of the image clip in seconds.

    Returns:
        An ImageClip object.

    Raises:
        FileNotFoundError: If the image file does not exist.
    """
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    return ImageClip(image_path, duration=duration)


def get_audio_clip(audio_path: str) -> AudioFileClip:
    """
    Creates an AudioFileClip from an audio file.

    Args:
        audio_path: The path to the audio file.

    Returns:
        An AudioFileClip object.

    Raises:
        FileNotFoundError: If the audio file does not exist.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    return AudioFileClip(audio_path)


def get_multiple_image_clips(
    images: list[str], durations: list[float], duration_limit: float
) -> list[ImageClip]:
    """
    Combines multiple images into a list of ImageClips, adjusting the last clip's duration
    to match the total duration limit.

    Args:
        images: A list of image paths.
        durations: A list of durations for each image (in seconds).
        duration_limit: The maximum allowed total duration for the combined clips (in seconds).

    Returns:
        A list of ImageClip objects.

    Raises:
        AssertionError: If the sum of durations (excluding the last one) exceeds the duration limit.
    """
    clips: list[ImageClip] = []
    total_duration = 0

    # Ensure the sum of durations (excluding the last one) is within the limit
    assert sum(durations[:-1]) <= duration_limit, (
        f"Duration limit ({duration_limit}) exceeded by the sum of durations "
        f"before the last clip: {sum(durations[:-1])}"
    )

    # Adjust the last clip's duration to fit the limit
    durations[-1] = duration_limit - sum(durations[:-1])

    logger.info(f"{Status.WIP} Adjusted durations: {durations}")

    for img, dur in zip(images, durations):
        total_duration += dur
        logger.debug(
            f"{Status.WIP} Preparing video clips: {total_duration:.2f} (secs) out of {duration_limit:.2f} (secs)"
        )
        clips.append(get_image_clip(img, dur))

    return clips


def generate_video_with_audio(
    images: list[str],
    durations: list[float],
    audio_path: str,
    output_path: str,
) -> None:
    """
    Generates a video by combining multiple images with audio.

    Args:
        images: A list of image paths.
        durations: A list of durations for each image (in seconds).
        audio_path: The path to the audio file.
        output_path: The path to save the generated video.
    """
    audio_clip = get_audio_clip(audio_path)
    image_clips = get_multiple_image_clips(
        images, durations, duration_limit=audio_clip.duration
    )
    final_clip = concatenate_videoclips(image_clips).with_audio(audio_clip)

    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=config.VIDEO_FPS,
        preset="faster",
    )
    logger.info(f"{Status.OK} Video file created at: {output_path}")


def combine_audio_and_image(image_path: str, audio_path: str, output_path: str) -> None:
    """
    Combines a single image and an audio file into a video.

    Args:
        image_path: The path to the image file.
        audio_path: The path to the audio file.
        output_path: The path to save the generated video.
    """
    audio_clip = get_audio_clip(audio_path)
    mins, secs = divmod(audio_clip.duration, 60)
    logger.info(f"Audio file duration: {int(mins)} mins {secs:.2f} secs")

    image_clip = get_image_clip(image_path, duration=audio_clip.duration)
    final_clip = CompositeVideoClip(clips=[image_clip]).with_audio(audio_clip)

    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=config.VIDEO_FPS,
        preset="faster",
    )
    logger.info(f"{Status.OK} Video file created at: {output_path}")


#
# # Example usage
# combine_audio_image(
#     image_path="my_image.png",
#     audio_path="test_audio.mp3",
#     output_path=f"output_fps{config.VIDEO_FPS}.mp4",
# )
