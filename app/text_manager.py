import logging

import utils


class SlideManager:
    """
    Content manager for preparing a text slide
    """

    def __init__(self):
        # special slides (first & slides)
        self.start = None
        self.end = None
        #
        # regular slides with 3 sections (header, body, footer)
        self.header = list()  # 0-2 rows
        self.body = list()  # 40 letters limit
        self.footer = list()  # 2 rows
        #
        # limits
        self._line_text_limits = 40  # Characters
        self._multi_line_text_limits = 12  # lines
        #
        self._debug_show_full_logs = False

    def _is_line_within_limits(self, text_line):
        # check if the number of characters in the text line is within the limits
        return len(text_line) < self._line_text_limits

    def _is_text_within_limits(self, multiline_text):
        # check if the number of lines in the text is within the limits
        return len(multiline_text.split("\n")) < self._multi_line_text_limits

    def _validate_text(self, multiline_text):
        logging.info("> Running Validator")
        if not self._is_text_within_limits(multiline_text):
            print("> Height: ❌ Too many lines in the input text")
            print(">>>>" * 12)
            print(multiline_text)
            print("<<<" * 12)
        else:
            if self._debug_show_full_logs:
                logging.info("> Height: ✅ Lines with in the limit")
        for line in multiline_text.splitlines("\n"):
            line = line.strip()
            if not self._is_line_within_limits(line):
                print(
                    "> Length: ❌ Too many words in one lines"
                    + f"\n\t[{line}]\n\tReduce ({len(line) - self._line_text_limits}) letters!"
                )
            else:
                if self._debug_show_full_logs:
                    logging.info(f"> Length: ✅")

    def is_text_with_limits(self, text):
        self.end = text

    def add_start_slide(self, text):
        self.start = text

    def end_slide(self, text):
        self.end = text

    def add_header(self, text):
        self.header = text

    def add_body(self, text):
        self.body = text
        self._validate_text(self.body)

    def add_footer(self, text):
        pass

    @staticmethod
    def print_row(text):
        if not text:
            return
        if type(text) == list:
            for line in text:
                logging.info(line)
        elif type(text) == str:
            logging.info(text)
        else:
            raise Exception("Error: Unexpected input error!")

    def show(self):
        # special slides (start, end)
        logging.info("# Start - slide")
        self.print_row(self.start)
        logging.info("# End - slide")
        self.print_row(self.end)

        # regular slide with 3 sections
        logging.info("# Header")
        self.print_row(self.header)
        logging.info("# Body")
        self.print_row(self.body)
        logging.info("# Footer")
        self.print_row(self.footer)

    def generate_image(self, text, output_path):
        from .image import generate_text_image

        self.add_body(text)
        generate_text_image(text, output_path)


if __name__ == "__main__":
    manager = SlideManager()
    manager.add_body(
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
