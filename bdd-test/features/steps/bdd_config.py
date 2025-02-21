import logging

import parse
from behave import *


def parse_number(text):
    return int(text)


@parse.with_pattern(r".*")
def parse_string(text):
    return text.strip()


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

register_type(Number=parse_number, String=parse_string)
use_step_matcher("cfparse")
