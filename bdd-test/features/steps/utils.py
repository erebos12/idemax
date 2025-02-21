import os
import re
import json
import logging
from enum import Enum

import requests
from requests import Response


valid_csv_file_type = ['ASSETS', 'JOURNAL', 'LEDGER_ACCOUNT', 'LABELS', 'ACCOUNT_PLAN']


def validate_and_convert_json_to_dict(input_json: str) -> dict:
    try:
        return json.loads(input_json)
    except Exception as e:
        err = "Error: Invalid json: {}\n".format(e)
        err += "{}".format(input_json)
        logging.error(err)
        raise Exception(err)


def open_and_validate_json_file(file_location):
    with open(file_location) as json_file:
        file_content = json.load(json_file)
    return file_content


def print_key_error(eval_str: str, received_json):
    print(">>>>> KeyError: Cannot access {}".format(eval_str))
    print(">>>>> Received {}".format(json.dumps(received_json, indent=2)))


def prettify_json(json_string: str) -> str:
    return json.dumps(json_string, indent=2)


def pretty_logging_json(json_string: str):
    logging.info(">>>>> JSON {}".format(prettify_json(json_string)))


def is_valid_file_type(file_type):
    if file_type in valid_csv_file_type:
        return True
    else:
        return False


def getColumnSet(attribute_name):
    columns = {
        'transactions': transactions_columns,
        'ledgerAccounts': ledger_accounts_columns,
        'assetTransactions': asset_transactions_columns
    }
    return columns.get(attribute_name, None)


def getColumnSetByFileType(file_type):
    columns = {
        'JOURNAL': transactions_columns,
        'ASSETS': asset_transactions_columns,
        'LEDGER_ACCOUNT': ledger_accounts_columns
    }
    return columns.get(file_type, None)


def create_file(file_content, name):
    try:
        with open(name, "w") as f:
            f.write(file_content)
    except Exception as e:
        err = "Error creating file {}: {}".format(name, e)
        raise Exception(err)


def delete_file(name):
    try:
        if os.path.exists(name):
            os.remove(name)
    except Exception as e:
        err = "Error deleting file {}: {}".format(name, e)
        raise Exception(err)


class transactions_columns(Enum):
    index = "index", True
    konto_nr = 'accountId', True
    soll_haben = 'transactionType', True
    kostenstelle_nr = 'clientsCostCenterName', False
    betrag = 'transactionAmount', True
    profitcenter_nr = 'profitCenterId', False
    auftrag_nr = 'jobId', False
    buchungstext = 'description', True

    def __new__(cls, field, mandatory):
        obj = object.__new__(cls)
        obj._value_ = field
        obj.mandatory = mandatory
        return obj


class ledger_accounts_columns(Enum):
    anlagen_nr = "assetNumber", False
    anlagen_unr = "assetCategory", False
    anlagen_bez = "assetDescription", False
    klasse_nr = "assetAccount", False
    konto_nr = "accountId", True
    kst_nr = "clientsCostCenterName", False
    bw_anfang = "rbvCapitalAssetsBegin", True
    bw_ende = "rbvCapitalAssetsEnd", True

    def __new__(cls, field, mandatory):
        obj = object.__new__(cls)
        obj._value_ = field
        obj.mandatory = mandatory
        return obj


class asset_transactions_columns(Enum):
    anlagennummer = "assetNumber", True
    anlagenbezeichnung = "assetDescription", True
    anlagen_klasse_nr = "assetCategory", True
    anlagen_klasse_bez = "assetCategoryDescription", False
    anlagen_unr = "assetAccount", False
    restbuchwert_beginn = "rbvCapitalAssetsBegin", True
    restbuchwert_ende = "rbvCapitalAssetsEnd", True
    anschaffungsdatum = "purchasingDate", True
    nutzungsdauer_in_monaten = "lifeTime", False
    anschaffungswert_ende = "acquisitionValueEnd", False
    anlage_kostenstelle_nr = "clientsCostCenterName", False
    anlage_afa = "assetDepreciation", True
    afa_zugang_HGB = "depreciationHGB", False

    def __new__(cls, field, mandatory):
        obj = object.__new__(cls)
        obj._value_ = field
        obj.mandatory = mandatory
        return obj


def create_csv_columns_headers(delimiter, header_enum):
    result = ""
    headers_row = []
    for header in header_enum:
        headers_row.append(re.sub(r'^.*?\.', '', str(header)))
    result = delimiter.join(headers_row)
    return result + '\n'


def map_field_value_to_backend_format(field_value, column, index):
    field_value = field_value.replace(';', '')
    field_value = "S" if field_value == "DEBIT" else field_value
    field_value = "H" if field_value == "CREDIT" else field_value
    if "index" in str(column) and field_value == "":
        return str(index + 1)
    elif column.mandatory and field_value == "":
        return "-"
    else:
        return field_value


def parse_json_to_csv(input_json, delimiter, columns):
    try:
        result = ""
        new_line = '\n'

        # creating headers
        result += create_csv_columns_headers(delimiter, columns)

        # creating data rows
        for index in range(len(input_json)):
            row = []
            for column in columns:
                field_value = str(input_json[index].get(column.value, ""))
                mapped_field_value = map_field_value_to_backend_format(field_value, column, index)
                row.append(mapped_field_value)
            result += delimiter.join(row) + new_line
    except Exception as e:
        logging.error(">>> Exception : {}".format(e))
    return result


def upload_file_to_eater(file_name, file_type, year, url) -> Response:
    payload = {
        'uploadFile': open(file_name, 'rb'),
        'type': (None, file_type),
        'yearId': (None, year),
        'source': (None, "ESRA")
    }
    return requests.post(url, files=payload)


def upload_file_to_dice(file_name, file_type, year, url) -> Response:
    payload = {
        'uploadFile': open(file_name, 'rb'),
        'type': (None, file_type),
        'yearId': (None, year)
    }
    return requests.post(url, files=payload)


def check_response_code(actual, expected, response_json):
    if actual != expected:
        err_msg = "Expected response code '{}' but received '{}'.\n".format(expected, actual)
        err_msg += ("--> received response was \n {}".format(prettify_json(response_json)))
        raise AssertionError(err_msg)


def create_csv_file_by_json(input_json, delimiter, file_location):
    result = ""
    new_line = '\n'
    headers_row = []
    result += delimiter.join(input_json[0].keys()) + new_line
    # creating data rows
    for index in range(len(input_json)):
        row = []
        for key, value in input_json[index].items():
            field_value = value.replace(';', '')
            row.append(field_value)
        result += delimiter.join(row) + new_line
    with open(file_location, 'w') as f:
        f.write(result)


def convert_json_to_csv(json_dict: str, delimiter: str) -> str:
    try:
        keys = json_dict[0].keys()
        result = ""
        new_line = '\n'
        result += delimiter.join(keys) + new_line
        for index in range(len(json_dict)):
            row = []
            for key, value in json_dict[index].items():
                field_value = value.replace(';', '')
                row.append(field_value)
            result += delimiter.join(row) + new_line
        return result
    except Exception as e:
        err = "Error while converting JSON to csv {}".format(e)
        logging.error(err)
        raise Exception(err)


def get_json_attribute_value(context, json_attribute: str) -> str:
    eval_str = "context.json" + json_attribute
    try:
        value = str(eval(eval_str))
        return value
    except KeyError:
        print_key_error(eval_str, context.json)


def store_value_in_context_attribute(context, value: str, context_attribute: str):
    setattr(context, context_attribute, value)


def replace_context_var_with_value(url, context):
    all_attributes = {}
    context_vars = re.findall('\(+(.*?)\)', url)
    for context_var in context_vars:
        all_attributes[context_var] = eval(context_var)  # get value for context.var
    new_url = url
    for context_var_name in all_attributes:
        url = new_url
        context_var_value = str(all_attributes.get(context_var_name))
        new_url = url.replace("(" + context_var_name + ")", context_var_value)
    return new_url


def eval_string(context, s: str) -> str:
    assert_that(context, is_not(None))
    try:
        value = str(eval(s))
    except AttributeError as e:
        raise e
    return value
