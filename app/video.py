import os
import config
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips


def get_image_clip(image_path, duration):
    """Fetch image clip"""
    if os.path.isfile(image_path):
        image_clip = ImageClip(image_path, duration=duration)
    else:
        raise FileNotFoundError(f"Not able to find {image_path}!")
    return image_clip


def get_audio_clip(audio_path):
    """Fetch audio clip"""
    if os.path.isfile(audio_path):
        audio_clip = AudioFileClip(audio_path)
    else:
        raise FileNotFoundError(f"Not able to find {audio_path}!")
    return audio_clip


def get_multiple_image_clip(images: list, durations: list, duration_limit: int) -> list:
    """Combines multiple images into a single ImageClip, respecting the duration limit.

    Args:
        images: List of image paths.
        durations: List of durations for each image (in seconds).
        duration_limit: Maximum allowed duration for the combined clip (in seconds).

    Returns:
        An ImageClip consisting of the concatenated images, or None if an error occurs.
    """
    clips = list()
    total_duration = 0

    # If the total duration exceed the required time limit, then last adjust the last clip.
    # If the total duration is under the required time limit, last clip is extended.
    assert (
        sum(durations[:-1]) < duration_limit
    ), f"Duration limit ({duration_limit}) exceeded!"
    durations[-1] = duration_limit - sum(durations[:-1])

    print("New durations", durations)
    for img, dur in zip(images, durations):
        total_duration += dur
        print(
            f"Video clips preparation: {total_duration} (secs) out of {duration_limit} (secs) "
        )
        clips.append(get_image_clip(img, dur))
    return clips


def generated_multi_image_video_with_audio(images, durations, audio_path, output_path):
    audio_clip = get_audio_clip(audio_path)

    image_clips = get_multiple_image_clip(
        images, durations, duration_limit=audio_clip.duration
    )

    # final_clip = CompositeVideoClip(clips=image_clips).with_audio(audio_clip)
    # final_clip = CompositeVideoClip(
    #     clips=concatenate_videoclips(image_clips)
    # ).with_audio(audio_clip)
    final_clip = concatenate_videoclips(image_clips).with_audio(audio_clip)

    # Write the result to a file
    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=config.VIDEO_FPS,
        preset="faster",
    )
    print(f"Video file is created at {output_path}")


def combine_audio_image(image_path, audio_path, output_path):
    """Combines an image and audio file into a video using MoviePy."""
    # Create an image clip with the same duration as the audio
    audio_clip = AudioFileClip(audio_path)
    mins, secs = divmod(audio_clip.duration, 60)
    print(f"Audio file duration: {mins} mins {secs} secs")

    # Generate Image Clips
    image_clip = ImageClip(image_path, duration=audio_clip.duration)

    # Overlay the audio on the image
    final_clip = CompositeVideoClip(clips=[image_clip]).with_audio(audio_clip)

    # Write the result to a file
    final_clip.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        fps=config.VIDEO_FPS,
        preset="faster",
    )  # Use appropriate codecs
    print(final_clip.__dict__)


#
# # Example usage
# combine_audio_image(
#     image_path="my_image.png",
#     audio_path="test_audio.mp3",
#     output_path=f"output_fps{config.VIDEO_FPS}.mp4",
# )
