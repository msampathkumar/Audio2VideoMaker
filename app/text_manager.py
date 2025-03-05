import logging

import config

from utils import Status

logger = logging.getLogger(__name__)


class TextManager:
    """
    Manages and validates text content for image generation.
    """

    def __init__(self) -> None:
        """
        Initializes the TextManager with default settings.
        """
        self.text_content: str = ""
        self.max_line_length: int = config.IMAGE_TEXT_MAX_LINE_CHAR_LIMIT
        self.max_lines: int = config.IMAGE_TEXT_MAX_LINES_LIMIT
        self.debug_show_full_logs: bool = False

    def _is_line_within_limits(self, text_line: str) -> bool:
        """
        Checks if a single line of text is within the character limit.

        Args:
            text_line: The line of text to check.

        Returns:
            True if the line is within the limit, False otherwise.
        """
        return len(text_line) <= self.max_line_length

    def _is_text_within_limits(self, multiline_text: str) -> bool:
        """
        Checks if the number of lines in a multi-line text is within the limit.

        Args:
            multiline_text: The multi-line text to check.

        Returns:
            True if the text is within the limit, False otherwise.
        """
        return len(multiline_text.splitlines()) <= self.max_lines

    def _validate_text(self, multiline_text: str) -> None:
        """
        Validates a multi-line text against length and line limits.

        Args:
            multiline_text: The multi-line text to validate.

        Raises:
            ValueError: If the text exceeds the defined limits.
        """
        logger.debug(f"{Status.WIP} Running Text Validator")
        if not self._is_text_within_limits(multiline_text):
            error_message = (
                f"{Status.NOT_OK} Height: Too many lines in the input text "
                f"(max {self.max_lines} lines allowed):\n"
                f"{multiline_text}"
            )
            logger.error(error_message)
            # raise ValueError(error_message)
        else:
            if self.debug_show_full_logs:
                logger.debug(f"{Status.OK} Height: Lines within the limit")

        for line_number, line in enumerate(multiline_text.splitlines()):
            line = line.strip()
            if not self._is_line_within_limits(line):
                error_message = (
                    f"{Status.NOT_OK} Length: Too many characters in line {line_number+1} "
                    f"(max {self.max_line_length} characters allowed):\n"
                    f"\t[{line}]\n"
                    f"\tReduce ({len(line) - self.max_line_length}) characters!"
                )
                logger.error(error_message)
                # raise ValueError(error_message)
            else:
                if self.debug_show_full_logs:
                    logger.debug(
                        f"{Status.OK} Length: Line {line_number+1} within limits"
                    )

        logger.debug(f"{Status.OK} Text validated successfully.")

    def set_text(self, text: str) -> list[str]:
        """
        Sets the text content and validates it.

        Args:
            text: The text content to set.

        Raises:
            ValueError: If the text is invalid.
        """
        self._validate_text(text)
        self.text_content = text

    def rearrange_text(self) -> str:
        """To re-arrange the input text to be at the center of the image."""
        text = self.text_content.strip()
        # text = self._rearrange_text_by_line(text)
        text = self._rearrange_text_by_height(text)
        return text

    def _rearrange_text_by_line(self, text, center_by_line=False) -> str:
        if center_by_line:
            return self._rearrange_text_by_line2(text)
        else:
            return self._rearrange_text_by_line1(text)

    @staticmethod
    def _rearrange_text_by_line1(text) -> str:
        # todo: check and remove this un-used method
        #   when using mono-spaced fonts, they may be of use
        """Adjust the text to be at the center by width"""
        import math

        text_lines = text.splitlines()
        diffs = [len(line) for line in text_lines]
        _diff = config.IMAGE_TEXT_MAX_LINE_CHAR_LIMIT - max(diffs)
        prefix = " " * math.ceil(_diff / 0.80)
        if _diff > 0:
            # print('-' * len(prefix), diffs, _diff, len(prefix))
            text_lines = [prefix + line for line in text_lines]
        return "\n".join(text_lines)

    @staticmethod
    def _rearrange_text_by_line2(text) -> str:
        """Adjust the text to be at the center by width"""
        text_lines = text.splitlines()
        limit = config.IMAGE_TEXT_MAX_LINE_CHAR_LIMIT
        text_lines = [line.center(limit) for line in text_lines]
        return "\n".join(text_lines)



    @staticmethod
    def _rearrange_text_by_height(text) -> str:
        """Adjust the text to be at the center by height"""
        import math

        lines = len(text.strip().splitlines())
        diff = config.IMAGE_TEXT_MAX_LINES_LIMIT - lines
        prefix = "\n" * math.ceil(diff / 2)
        return prefix + text

    # For only testing purposes
    def generate_image(self, output_path: str) -> str:
        """
        Generates an image from the current text content.

        Args:
            output_path: The path to save the generated image.

        Returns:
            The path to the generated image.

        Raises:
            ValueError: If no text content is set.
        """
        if not self.text_content:
            raise ValueError("No text content set. Call set_text() first.")

        from image import generate_text_image

        logger.debug(
            f"{Status.WIP} Generating image for text: {self.text_content[:50]}..."
        )
        image_path = generate_text_image(self.text_content, output_path)
        logger.info(f"{Status.OK} Image generated at: {image_path}")
        return image_path

    def show(self) -> None:
        """
        Displays the current text content.
        """
        if self.text_content:
            logger.debug("---- Current Text Content ----")
            logger.debug(str(self.text_content.strip()))
            logger.debug("---- End of Text Content ----")
        else:
            logger.warning("No text content set.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    manager = TextManager()
    try:
        manager.set_text(
            """
Odkupiłeś grzeszników takich jak Ajamil
a także przeprowadziłeś
przez nieszlachetnych jak Sadhana
Chroń mnie, o miłosierny Panie!

You redeemed sinners like Ajamil
                            You redeemed sinners like Ajamil
and also ferried across
ignoble ones like Sadhana.
Protect me, O merciful Lord!
"""
        )
        manager.show()
        manager.generate_image("test_image.png")  # For only testing purposes
    except ValueError as e:
        logger.error(f"{Status.NOT_OK} Text validation error: {e}")
