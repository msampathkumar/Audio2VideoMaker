import logging
import os

import yaml

from utils import Status, logger

logger = logger.setLevel(logging.DEBUG)


class Validation(Status):
    """User input configuration's validater"""

    def __init__(self, config_file_path: str) -> None:
        logger.info(f" User input: {config_file_path}")
        self._config_file_path = config_file_path
        self._folder_path = os.path.dirname(self._config_file_path)
        self.config_data = None
        # audio & video
        self.audio_file_path = None
        self.video_file_path = None
        # audio & video
        self.txt_image_durations = list()
        self.txt_image_text = list()
        self.txt_image_names = list()
        # run validations
        self.read_config()
        self.check_file_inputs()

    def read_config(self) -> None:
        with open(self._config_file_path, "rt", encoding="utf8") as fp:
            self.config_data = yaml.safe_load(fp)
        logger.debug(f"{self.ok} Load config")

    def check_file_path(self, file_path: str) -> bool:
        status = os.path.isfile(file_path)
        if status:
            logger.debug(f"{self.ok} Checking file - {file_path}")
        else:
            logger.debug(f"{self.not_ok} Checking file - {file_path}")
        return status

    def check_file_inputs(self) -> None:
        # check if `audio` data
        if "audio" not in self.config_data:
            logger.info(f"Missing `audio` section in {self._config_file_path}")
            raise Exception(f"Missing `audio` section in {self._config_file_path}")
        else:
            self.audio_file_path = os.path.join(
                self._folder_path, self.config_data["audio"]
            )
            self.check_file_path(self.audio_file_path)

        # check if `video` data
        if "video" not in self.config_data:
            logger.warning(f"Missing `video` section in {self.config_data}")
        else:
            _name = self.config_data.get("video", "movie.mp4")
            self.video_file_path = os.path.join(self._folder_path, _name)
            # self.check_file_path(self._video_file_path)

        # check images data
        if "images" not in self.config_data:
            logger.warning(f"Missing `images` section in {self._config_file_path}")
        else:
            i = 0
            for image_record in self.config_data.get("images"):
                logger.info(f" - ({ i }) Loading image data: {str(image_record)[:50]}...")
                self.txt_image_text.append(image_record["text"])
                self.txt_image_durations.append(image_record["duration"])

                # image name
                i += 1
                _name = image_record.get("name", "text_image_" + str(i) + ".png")
                if not os.path.isfile(_name):
                    _name = os.path.join(self._folder_path, _name)
                    # self.check_file_path(_name)
                self.txt_image_names.append(_name)


class GetConfig(Validation):

    def show(self) -> None:
        logger.info("----" * 12)
        logger.info(f" - Config file path: {self._config_file_path}")
        logger.info(f" - Audio input path: {self.audio_file_path}")
        logger.info(f" - Video Output path: {self.video_file_path}")
        logger.info(f" - Image text duration: {self.txt_image_durations}")
        logger.info(f" - Image file names: {self.txt_image_names}")
        logger.info("----" * 12)


if __name__ == "__main__":
    config = GetConfig("../data/sample_data/config.yaml")
    config.show()
