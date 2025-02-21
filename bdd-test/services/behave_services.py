from behave.__main__ import main as behave_main
from io import StringIO
import sys
import os
import datetime
import re

""" This module includes all functions that handle python behave specific details. """


class TeeStream:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)

    def flush(self):
        for stream in self.streams:
            stream.flush()


def run_test_file(location: str) -> dict:
    res = run_behave_tests(location)
    return extract_results(res)


def write_file_with_content(content: str, location: str) -> None:
    try:
        with open(location, 'w') as file:
            file.write(content)
            file.close()
            print(f"File {location} created")
    except IOError as e:
        raise e


def delete_file_from_fs(location: str) -> None:
    if os.path.exists(location):
        os.remove(location)
        print(f"File {location} deleted")
    else:
        raise FileNotFoundError(f"Cannot delete file '{location}'")


def run_behave_tests(file_location='features') -> str:
    print(f"run_behave_tests() - {file_location}")
    new_stdout = StringIO()
    old_stdout = sys.stdout
    sys.stdout = TeeStream(new_stdout, old_stdout)
    behave_main([file_location])
    sys.stdout = old_stdout
    return new_stdout.getvalue()


def extract_results_for_topic(text: str, topic: str) -> dict:
    regex = r"(\d+) " + topic + "[s]? passed, (\d+) failed, (\d+) skipped"
    match = re.search(regex, text)
    number_undefined = 0
    if match:
        number_passed = int(match.group(1))
        number_failed = int(match.group(2))
        number_skipped = int(match.group(3))
    else:
        raise Exception("extract_results_for_topic() - Cannot read result from test")
    if topic == 'step':
        number_undefined = get_undefined_steps_number(text)
    result = {'Passed': number_passed,
              'Failed': number_failed,
              'Skipped': number_skipped,
              }
    if number_undefined != 0:
        result['Undefined'] = number_undefined
    return result


def get_undefined_steps_number(text: str) -> int:
    regex_undefined = r"(\d+) undefined"
    match = re.search(regex_undefined, text)
    if match:
        return int(match.group(1))
    return 0


def extract_results(text: str) -> dict:
    full_output = text
    feature = extract_results_for_topic(text, 'feature')
    scenarios = extract_results_for_topic(text, 'scenario')
    steps = extract_results_for_topic(text, 'step')
    if feature["Failed"] == 0:
        text = "Tests ended successfully ✅✅✅🍺🍺🍺"
    else:
        text = "Tests ended with errors 🚨🚨🚨🙀🙀🙀"
    return {
        'Result': text,
        'Features': feature,
        'Scenarios': scenarios,
        'Steps': steps,
        'Timestamp': datetime.datetime.now(),
        'debugging': {
            'console': full_output
        }
    }


def extract_not_implemented_exception(text: str):
    match = re.search(r'NotImplementedError\((.*?)\)', text)
    if match:
        return match.group(1)
    return None


def remove_ansi_codes(text):
    ansi_escape = re.compile(r'''
        \x1B  # ESC
        (?:   # 7-bit C1 Fe (nicht erfassen)
            [@-Z\\-_]
        |     # oder [ for 8-bit C1 Fe (nicht erfassen)
            \[
            [0-?]*  # 0 oder mehr Parameterzeichen
            [ -/]*  # 0 oder mehr Zwischenzeichen
            [@-~]   # Abschlusszeichen
        )
    ''', re.VERBOSE)
    return ansi_escape.sub('', text)
