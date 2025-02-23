import sys

import validation
import image
import video


def main(
    config: validation.GetConfig,
    generate_image: bool = True,
    generate_video: bool = False,
):
    config_data = config
    # generate images
    if generate_image:
        image.generate_multiple_text_images(
            text_inputs=config_data.txt_image_text,
            output_paths=config_data.txt_image_names,
        )

    # generate video
    if generate_video:
        video.generated_multi_image_video_with_audio(
            images=config_data.txt_image_names,
            durations=config_data.txt_image_durations,
            output_path=config_data.video_file_path,
            audio_path=config_data.audio_file_path,
        )
    # end of main


if __name__ == "__main__":
    # Test Image
    if "test" in sys.argv:
        image.create_test_image()
        sys.exit()

    # main program
    print("-" * 50)
    config_path = None
    for each in sys.argv:
        if each.endswith(".yaml"):
            config_path = each
    if not config_path:
        raise Exception("Missing config .yaml input file!")
    else:
        print(f"Found provided input config file {config_path}")
    config_info = validation.GetConfig(config_path)
    config_info.show()

    # validate_and_show_config(config_path)
    if "image" in sys.argv:
        main(config=config_info, generate_image=True)
    if "video" in sys.argv:
        main(config=config_info, generate_video=True)
    print("-" * 50)
