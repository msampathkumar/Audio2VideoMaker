import logging
import os
import yaml
from typing import List, Dict, Any

from utils import Status


logger = logging.getLogger(__name__)


class ConfigValidationError(Exception):
    """Custom exception for configuration validation errors."""

    pass


class ConfigValidator(Status):
    """
    Validates user input configuration from a YAML file.
    """

    def __init__(self, config_file_path: str) -> None:
        """
        Initializes the ConfigValidator.

        Args:
            config_file_path: The path to the YAML configuration file.
        """
        logger.debug(f"Initializing configuration from: {config_file_path}")
        self.config_file_path = config_file_path
        self.folder_path = os.path.dirname(self.config_file_path)
        self.config_data: Dict[str, Any] = {}
        self.audio_file_path: str = ""
        self.video_file_path: str = ""
        self.image_durations: List[float] = []
        self.image_texts: List[str] = []
        self.image_names: List[str] = []

        self._validate_config()

    def _validate_config(self) -> None:
        """
        Validates the entire configuration file.
        """
        self._read_config()
        self._validate_audio_section()
        self._validate_video_section()
        self._validate_images_section()

    def _read_config(self) -> None:
        """
        Reads the YAML configuration file.

        Raises:
            ConfigValidationError: If there is an error reading the file.
        """
        try:
            with open(self.config_file_path, "rt", encoding="utf8") as fp:
                self.config_data = yaml.safe_load(fp)
            logger.debug(f"{self.OK} Configuration file loaded successfully.")
        except FileNotFoundError:
            raise ConfigValidationError(
                f"Configuration file not found: {self.config_file_path}"
            )
        except yaml.YAMLError as e:
            raise ConfigValidationError(
                f"Error parsing YAML file: {self.config_file_path}\n{e}"
            )

    def _validate_audio_section(self) -> None:
        """
        Validates the 'audio' section of the configuration.

        Raises:
            ConfigValidationError: If the 'audio' section is missing or invalid.
        """
        if "audio" not in self.config_data:
            raise ConfigValidationError(
                f"Missing 'audio' section in configuration file: {self.config_file_path}"
            )

        audio_filename = self.config_data["audio"]
        self.audio_file_path = os.path.join(self.folder_path, audio_filename)
        if not os.path.isfile(self.audio_file_path):
            raise ConfigValidationError(f"Audio file not found: {self.audio_file_path}")
        logger.debug(f"{self.OK} Audio file found: {self.audio_file_path}")

    def _validate_video_section(self) -> None:
        """
        Validates the 'video' section of the configuration.
        """
        if "video" not in self.config_data:
            logger.warning(
                f"Missing 'video' section in configuration file: {self.config_file_path}. Using default 'movie.mp4'"
            )
            self.video_file_path = os.path.join(self.folder_path, "movie.mp4")
        else:
            self.video_file_path = os.path.join(
                self.folder_path, self.config_data["video"]
            )
        logger.debug(f"{self.OK} Video output path set to: {self.video_file_path}")

    def _validate_images_section(self) -> None:
        """
        Validates the 'images' section of the configuration.

        Raises:
            ConfigValidationError: If the 'images' section is missing or invalid.
        """
        if "images" not in self.config_data:
            raise ConfigValidationError(
                f"Missing 'images' section in configuration file: {self.config_file_path}"
            )

        for i, image_record in enumerate(self.config_data["images"]):
            logger.debug(
                f"{self.WIP} ({i}) Validating image data: {str(image_record)[:50]}..."
            )
            self._validate_image_record(image_record, i)

    def _validate_image_record(self, image_record: Dict[str, Any], index: int) -> None:
        """
        Validates a single image record.

        Args:
            image_record: The image record to validate.
            index: The index of the image record.

        Raises:
            ConfigValidationError: If the image record is invalid.
        """
        if "text" not in image_record:
            raise ConfigValidationError(
                f"Missing 'text' in image record at index {index}"
            )
        if "duration" not in image_record:
            raise ConfigValidationError(
                f"Missing 'duration' in image record at index {index}"
            )
        if not isinstance(image_record["duration"], (int, float)):
            raise ConfigValidationError(
                f"'duration' must be a number in image record at index {index}"
            )

        self.image_texts.append(image_record["text"])
        self.image_durations.append(float(image_record["duration"]))

        image_name = image_record.get("name", f"text_image_{index + 1}.png")
        image_path = os.path.join(self.folder_path, image_name)
        self.image_names.append(image_path)
        logger.debug(
            f"{self.WIP} Image {index} text: {str(image_record['text'])[:50]}..."
        )
        logger.debug(f"{self.WIP} Image {index} duration: {image_record['duration']}")
        logger.debug(f"{self.WIP} Image {index} name: {image_path}")
        logger.debug(f"{self.OK} Image {index} data validated.")

    def show_config(self) -> None:
        """
        Displays the loaded configuration.
        """
        logger.debug("----" * 12)
        logger.debug(f"Configuration file path: {self.config_file_path}")
        logger.debug(f"Audio input path: {self.audio_file_path}")
        logger.debug(f"Video output path: {self.video_file_path}")
        logger.debug(f"Image text durations: {self.image_durations}")
        logger.debug(f"Image file names: {self.image_names}")
        logger.debug("----" * 12)

    @property
    def txt_image_text(self) -> List[str]:
        return self.image_texts

    @property
    def txt_image_durations(self) -> List[float]:
        return self.image_durations

    @property
    def txt_image_names(self) -> List[str]:
        return self.image_names

    @property
    def ok(self) -> str:
        return Status.OK

    @property
    def not_ok(self) -> str:
        return Status.NOT_OK


class GetConfig(ConfigValidator):
    pass


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        config = GetConfig("../data/Shabad01/config.yaml")
        config.show_config()
    except ConfigValidationError as e:
        logger.error(f"{ Status.NOT_OK } Configuration error: {e}")
