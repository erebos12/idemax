from io import *

from utils import *


@when('upload csv file from location "{file_location}" with file type "{file_type}" for year "{year}"')
def upload_csv_file(context, file_location, file_type, year):
    if not is_valid_file_type(file_type):
        raise Exception(">>> ERROR: Wrong file type specified. Must be in {}".format(valid_csv_file_type))
    response = upload_file_to_eater(file_location, file_type, year, EATER_CSV_UPLOAD_URL)
    check_response_code(response.status_code, 200, response.json)

@when('upload csv file from location "{file_location}" with file type "{file_type}" for year "{year}" in context.json')
def upload_csv_file(context, file_location, file_type, year):
    if not is_valid_file_type(file_type):
        raise Exception(">>> ERROR: Wrong file type specified. Must be in {}".format(valid_csv_file_type))
    response = upload_file_to_dice(file_location, file_type, eval(year), DICE_CSV_UPLOAD_URL)
    context.status_code = response.status_code

@when('upload csv file from location by DICE "{file_location}" with file type "{file_type}" for year "{year}"')
def upload_csv_file(context, file_location, file_type, year):
    if not is_valid_file_type(file_type):
        raise Exception(">>> ERROR: Wrong file type specified. Must be in {}".format(valid_csv_file_type))
    response = upload_file_to_dice(file_location, file_type, year, DICE_CSV_UPLOAD_URL)
    context.status_code = response.status_code


@when('upload csv file from location by DICE "{file_location}" with file type "{file_type}" for year "{year}" in context.json')
def upload_csv_file(context, file_location, file_type, year):
    if not is_valid_file_type(file_type):
        raise Exception(">>> ERROR: Wrong file type specified. Must be in {}".format(valid_csv_file_type))
    response = upload_file_to_dice(file_location, file_type, eval(year), DICE_CSV_UPLOAD_URL)
    context.status_code = response.status_code


@when('upload json file as csv from location "{file_location}" with file type "{file_type}" for year "{year}"')
def upload_json_file_as_csv_file(context, file_location, file_type, year):
    columns = getColumnSetByFileType(file_type)
    if columns is not None:
        json_array = None
        with open(file_location, 'r') as json_file:
            file_content = json.loads(json_file.read().rstrip())
            json_array = file_content[list(file_content.keys())[0]]
        csv_string = parse_json_to_csv(json_array, ';', columns)
        create_file(csv_string, "temp.csv")
        response = upload_file_to_eater("temp.csv", file_type, year, EATER_CSV_UPLOAD_URL)
        check_response_code(response.status_code, 200, response.json)
    else:
        raise Exception(">>> ERROR: Wrong file type specified. Must be in {}".format(valid_csv_file_type))


@when('upload csv file with given content and file type "{file_type}" for year "{year}"')
def upload_csv_file_with_given_content(context, file_type, year):
    assert_that(context.file, is_not(None))
    columns = getColumnSetByFileType(file_type)
    if columns is not None:
        csv_string = parse_json_to_csv(context.file, ';', columns)
        create_file(csv_string, "temp.csv")
        response = upload_file_to_eater("temp.csv", file_type, year, EATER_CSV_UPLOAD_URL)
        check_response_code(response.status_code, 200, response.json)
    else:
        raise Exception(">>> ERROR: Wrong file type specified. Must be in {}".format(valid_csv_file_type))


@given('following csv file content as json')
def given_csv_content_as_json(context):
    context.json = validate_and_convert_json_to_dict(context.text)


@When('upload given csv file with file type "{file_type}" and year "{year}"')
def upload_given_csv_file_with_file_type(context, file_type, year):
    try:
        assert_that(context.json, is_not(None))
        csv_content = convert_json_to_csv(context.json, DELIMITER)
        file_name = "temp.csv"
        create_file(csv_content, file_name)
        response = upload_file_to_eater(file_name, file_type, year, EATER_CSV_UPLOAD_URL)
        check_response_code(response.status_code, 200, response.json)
    finally:
        delete_file(file_name)


@When('upload csv content to eater with file type "{file_type}" and year "{year}"')
def upload_csv_content_to_eater(context, file_type, year):
    try:
        assert_that(context.json, is_not(None))
        csv_content = convert_json_to_csv(context.json, DELIMITER)
        file_name = "temp.csv"
        create_file(csv_content, file_name)
        response = upload_file_to_eater(file_name, file_type, year, EATER_CSV_UPLOAD_URL)
        context.json = response.json()
        context.status_code = response.status_code
    finally:
        delete_file(file_name)
