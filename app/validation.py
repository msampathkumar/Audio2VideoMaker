import os
from logging import raiseExceptions

import yaml
from mesop import audio


class Status:
    ok = "✅ OK!"
    not_ok = "❌ Not ok!"
    overriding = "☑️ Overriding old one!"
    to_create = "☑️ Overriding old one!"


class Validation(Status):

    def __init__(self, config_file_path: str) -> None:
        print(f" User input: {config_file_path}")
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
        print(f"[{self.ok}] Load config")

    def check_file_path(self, file_path: str) -> bool:
        status = os.path.isfile(file_path)
        if status:
            print(f"[{self.ok}] Checking file - {file_path}")
        else:
            print(f"[{self.not_ok}] Checking file - {file_path}")
        return status

    def check_file_inputs(self) -> None:
        # check if `audio` data
        if "audio" not in self.config_data:
            print(f"Missing `audio` section in {self._config_file_path}")
            raise Exception(f"Missing `audio` section in {self._config_file_path}")
        else:
            self.audio_file_path = os.path.join(
                self._folder_path, self.config_data["audio"]
            )
            self.check_file_path(self.audio_file_path)

        # check if `video` data
        if "video" not in self.config_data:
            print(f"Missing `video` section in {self.config_data}")
        else:
            _name = self.config_data.get("video", "movie.mp4")
            self.video_file_path = os.path.join(self._folder_path, _name)
            # self.check_file_path(self._video_file_path)

        # check images data
        if "images" not in self.config_data:
            print(f"Missing `images` section in {self._config_file_path}")
        else:
            i = 0
            for image_record in self.config_data.get("images"):
                print(f" - [Image: { i }] Loading image: {image_record}")
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
        print("----" * 12)
        print(f" - Config file path:\t{self._config_file_path}")
        print(f" - Audio input path:\t{self.audio_file_path}")
        print(f" - Video Output path:\t{self.video_file_path}")
        print(f" - Image text duration:\t {self.txt_image_durations}")
        print(f" - Image file names:\t{self.txt_image_names}")
        print("----" * 12)


if __name__ == "__main__":
    config = GetConfig("data/sample_data/config.yaml")
    config.show()
