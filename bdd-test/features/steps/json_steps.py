import json

from utils import *
from hamcrest import assert_that, is_not, less_than_or_equal_to, not_none, equal_to, matches_regexp, contains_string, empty


@then('print context json')
def print_json_context(context):
    logging.error("CONTEXT.JSON >>> {}".format(json.dumps(context.json, indent=2)))


@then('overwrite json attribute "{attribute_name}" from file "{file_name}"')
def overwrite_json_attribute_from_file(context, attribute_name, file_name):
    json_string = open_and_validate_json_file(file_name)
    columns = getColumnSet(attribute_name)
    if columns is not None:
        json_array = json_string[attribute_name]
        context.file['uploadFile'] = parse_json_to_csv(json_array, ';', columns)
    else:
        if context.json is not None and context.json[attribute_name] is not None:
            context.json[attribute_name].update(json_string)
        else:
            context.json[attribute_name] = json_string[attribute_name]


@then('overwrite json attribute "{attribute_name}" with')
def overwrite_json_attribute(context, attribute_name):
    new_dict = validate_and_convert_json_to_dict(context.text)
    try:
        columns = getColumnSet(attribute_name)
        if columns is not None:
            json_array = new_dict[attribute_name]
            context.file['uploadFile'] = parse_json_to_csv(json_array, ';', columns)
        else:
            context.json[attribute_name].update(new_dict)
    except:
        # in case attribute does not exist, then create it
        context.json[attribute_name] = new_dict[attribute_name]


@then('partial overwrite of json attribute "{attribute_name}" with json from context-variable "{context_variable}"')
def overwrite_json_attribute_with_partial_json(context, attribute_name, context_variable):
    assert_that(context.json, is_not(None), "Ensure that context.json is set correctly!")
    try:
        eval_str = "context.json" + attribute_name
        var = eval(context_variable)
        eval_json = eval_str + ' = var'
        exec(eval_json)
    except Exception as e:
        print(">>>>> Exception {}".format(e))
        raise e


@then('partial overwrite of json attribute "{attribute_name}" with following json')
def overwrite_json_attribute_with_partial_json(context, attribute_name):
    assert_that(context.json, is_not(None), "Ensure that context.json is set correctly!")
    json_string = validate_and_convert_json_to_dict(context.text)
    context.json[attribute_name] = json_string[attribute_name]


@then('overwrite single json attribute "{attribute_name}" with value "{attribute_value}" in context.json')
def overwrite_single_json_attribute_generic(context, attribute_name, attribute_value):
    assert_that(context.json, is_not(None), "Ensure that context.json is set correctly!")
    try:
        left = "context.json" + attribute_name
        exec(left + "=" + attribute_value)
    except Exception as e:
        print(">>>>> Exception {}".format(e))
        raise e


@DeprecationWarning
@then('set single json attribute "{attribute_name}" with value "{attribute_value}" in context.json')
def overwrite_single_json_attribute(context, attribute_name, attribute_value):
    assert_that(context.json, is_not(None), "Ensure that context.json is set correctly!")
    try:
        try:
            context.json[attribute_name] = eval(attribute_value)
        except Exception as ex:
            context.json[attribute_name] = attribute_value
    except Exception as e:
        print(">>>>> Exception {}".format(e))
        raise e


@then(
    'set json attribute "{attribute_name}" child attribute "{attribute_child_name}" with value "{attribute_value}" in context.json')
def overwrite_single_json_attribute_and_child(context, attribute_name, attribute_child_name, attribute_value):
    assert_that(context.json, is_not(None), "Ensure that context.json is set correctly!")
    assert_that(eval(attribute_value), is_not(None), "Ensure that attribute_value set in context correctly!")
    try:
        context.json[attribute_name][attribute_child_name] = eval(attribute_value)
    except Exception as e:
        print(">>>>> Exception {}".format(e))
        raise e


@then(
    'set nested json attribute "{attribute_name}" child attribute "{attribute_child_name}" child attribute "{attribute_child_child_name}" with value "{attribute_value}" in context.json')
def overwrite_single_json_attribute_and_child_and_child(context, attribute_name, attribute_child_name,
                                                        attribute_child_child_name, attribute_value):
    assert_that(context.json, is_not(None), "Ensure that context.json is set correctly!")
    assert_that(eval(attribute_value), is_not(None), "Ensure that attribute_value set in context correctly!")
    try:
        context.json[attribute_name][attribute_child_name][attribute_child_child_name] = eval(attribute_value)
    except Exception as e:
        print(">>>>> Exception {}".format(e))
        raise e


@given('following json')
def given_json(context):
    context.json = json.loads(context.text)
    assert_that(context.json, is_not(None))


@given('following parameter with name "{var_name}" and value {var_value}"')
def given_json(context, var_name, var_value):
    context.variable = var_value
    assert_that(context.variable, is_not(None))


@given('following json in file "{file_location}"')
def given_json(context, file_location):
    context.json = open_and_validate_json_file(file_location)
    # validate json here
    assert_that(context.json, is_not(None))


@then('json attribute "{json_attribute}" exists')
def check_json_attribute_exists(context, json_attribute):
    eval_str = "context.json" + json_attribute
    try:
        value = eval(eval_str)
    except Exception as e:
        value = None
        print_key_error(eval_str, context.json)
        print(">>>>> Exception {}".format(e))
    assert_that(value, is_not(None))


@then('expect json response is equal to content of file "{json_file}"')
def is_json_body_equal_to_json_file(context, json_file):
    expected = None
    received = None
    try:
        expected = open_and_validate_json_file(json_file)
        received = context.json
    except Exception as e:
        print(">>>>> Exception {}".format(e))
    assert_that(expected, not_none(), "No json found in file.")
    assert_that(received, not_none(), "No json body received.")
    assert_that(expected, equal_to(received))


@then('json attribute "{json_attribute}" is equal to "{expected_value}"')
def check_json_attribute_value(context, json_attribute, expected_value):
    eval_str = "context.json" + json_attribute
    try:
        value = str(eval(eval_str))
    except KeyError as e:
        print("ERROR: Cannot access json with {}".format(eval_str))
        raise KeyError(e)
    if value != expected_value:
        raise AssertionError("Expected value '{}' but received '{}'.".format(expected_value, value))


@then('store context.json in context variable "{context_variable:String}"')
def store_context_json_in_customized_context_variable(context, context_variable):
    assert_that(context.json, is_not(None))
    assert_that(context_variable, is_not(None))
    var = eval("context_variable")
    eval_str = var + " = context.json"
    exec(eval_str)


@then('store json attribute "{json_attribute}" in context variable "{context_variable:String}"')
def store_json_atr_value_context_id1(context, json_attribute, context_variable):
    assert_that(context.json, is_not(None))
    assert_that(json_attribute, is_not(None))
    assert_that(context_variable, is_not(None))
    eval_str = "context.json" + json_attribute
    var = eval("context_variable")
    eval_json = var + ' = eval(eval_str)'
    exec(eval_json)


@then('store json attribute "{json_attribute}" in variable context.id')
def store_json_atr_value_context_id1(context, json_attribute):
    value = get_json_attribute_value(context, json_attribute)
    store_value_in_context_attribute(context, value, "id")


@then('store json attribute "{json_attribute}" in variable context.id2')
def store_json_atr_value_context_id2(context, json_attribute):
    value = get_json_attribute_value(context, json_attribute)
    store_value_in_context_attribute(context, value, "id2")


@then('store json attribute "{json_attribute}" in variable context.id3')
def store_json_atr_value_context_id3(context, json_attribute):
    value = get_json_attribute_value(context, json_attribute)
    store_value_in_context_attribute(context, value, "id3")


@then('json attribute "{json_attribute}" is less equal than "{expected_value:Number}" msecs')
def check_json_attribute_value(context, json_attribute, expected_value):
    eval_str = "context.json" + json_attribute
    try:
        value = int(eval(eval_str))
    except KeyError:
        print_key_error(eval_str, context.json)
    assert_that(value, less_than_or_equal_to(expected_value))


@then('response body is equal to json from file "{json_file}"')
def check_json_attribute_value(context, json_attribute, expected_value):
    eval_str = "context.json" + json_attribute
    try:
        value = int(eval(eval_str))
    except KeyError:
        print_key_error(eval_str, context.json)
    assert_that(value, less_than_or_equal_to(expected_value))


@then('json attribute "{json_attribute}" does not exist')
def json_attribute_does_not_exist(context, json_attribute):
    eval_str = "context.json" + json_attribute
    try:
        value = str(eval(eval_str))
        msg = "Attribute '{}' must not be there!".format(json_attribute)
        assert_that(value, equal_to(None), msg)
    except KeyError:
        print_key_error(eval_str, context.json)


@then('json attribute "{json_attribute:String}" contains "{expected_value:String}"')
def check_json_attribute_value_contains(context, json_attribute, expected_value):
    eval_str = "context.json" + json_attribute
    try:
        value = str(eval(eval_str))
    except KeyError:
        print_key_error(eval_str, context.json)
    assert_that(value, contains_string(expected_value))


@then('json attribute "{json_attribute:String}" matches regex "{regex_value:String}"')
def check_json_attribute_value_matching_regex(context, json_attribute, regex_value):
    try:
        regex_pattern = re.compile(regex_value)
    except Exception as e:
        msg = "Invalid regex: {}".format(e)
        raise Exception(msg)
    eval_str = "context.json" + json_attribute
    try:
        value = str(eval(eval_str))
    except KeyError:
        print_key_error(eval_str, context.json)
    assert_that(value, matches_regexp(regex_pattern))


@then('json attribute "{json_attribute:String}" has length "{expected_length:Number}"')
def check_json_attribute_length(context, json_attribute, expected_length):
    eval_str = "context.json" + json_attribute
    length = len(eval(eval_str))
    if length != expected_length:
        pretty_logging_json(context.json)
        raise AssertionError("Expected length '{}' but received '{}'.".format(expected_length, length))


@then('json attribute "{json_attribute:String}" has at least length "{expected_length:Number}"')
def check_json_attribute_length(context, json_attribute, expected_length):
    eval_str = "context.json" + json_attribute
    length = len(eval(eval_str))
    if length < expected_length:
        pretty_logging_json(context.json)
        raise AssertionError("Expected length '{}' but received '{}'.".format(expected_length, length))


@then('json attribute "{json_attribute}" is empty')
def check_json_attribute_value_is_empty(context, json_attribute):
    eval_str = "context.json" + json_attribute
    try:
        value = str(eval(eval_str))
    except KeyError:
        print_key_error(eval_str, context.json)
    assert_that(value, empty())


@then('json attribute "{json_array_name:String}" contains object')
def check_json_object_in_json_array(context, json_array_name):
    expected_json_object = json.loads(context.text)
    assert_that(context.json, is_not(None))
    eval_str = "context.json" + json_array_name
    match = None
    try:
        received_json_array = eval(eval_str)
    except KeyError as e:
        print_key_error(eval_str, context.json)
        raise AssertionError(e)
    for expected_json_attribute in expected_json_object:
        expected_value = expected_json_object[expected_json_attribute]
        print(f"Checking for '{expected_json_attribute}' with value '{expected_value}'")
        match = find_matching_array_entry(expected_json_attribute, expected_value, received_json_array)
        if match is not None:
            break
    assert_that(match, is_not(None), f"Did not find '{expected_json_attribute}' with value '{expected_value}'")
    for expected_json_attribute in expected_json_object:
        expected_value = expected_json_object[expected_json_attribute]
        received_value = str(match[expected_json_attribute])
        assert_that(received_value, equal_to(expected_value),
                    f"'Expected for '{expected_json_attribute}' with '{expected_value}' but received '{received_value}'")


@then('sort json array "{json_array_name}" by "{sort_by}" and store in context variable "{context_variable}"')
def sort_json_array_by_and_store_in_context_var(context, json_array_name, sort_by, context_variable):
    try:
        received_json_array = eval(json_array_name)
    except KeyError as e:
        print_key_error(json_array_name, context.json)
        raise AssertionError(e)
    sort_cmd = f"sorted(received_json_array, key=lambda x: x['{sort_by}'])"
    sorted_list = eval(sort_cmd)
    eval_json = f"{context_variable} = {sorted_list}"
    exec(eval_json)
    assert_that(eval(context_variable), is_not(None))


@then('context variable "{context_variable}" is equal to "{expected_value}"')
def check_context_variable_value(context, context_variable, expected_value):
    value = eval_string(context, context_variable)
    assert_that(value, equal_to(expected_value), f"'Expected '{expected_value}' but received '{value}'")


@then('context variable "{context_variable}" is empty')
def check_context_variable_value(context, context_variable):
    assert_that(eval_string(context, context_variable), empty())


def find_matching_array_entry(expected_attribute: str, expected_value: str, received_json_array: list) -> object:
    received_json_obj: object
    for received_json_obj in received_json_array:
        received_value = received_json_obj[expected_attribute]
        if expected_value == received_value:
            return received_json_obj
    return None
