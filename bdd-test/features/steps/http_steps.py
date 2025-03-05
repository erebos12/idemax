import time
from io import *

import yaml
from hamcrest import *

from utils import *

integrateTests = "false"
from os import environ

if environ.get('INTEGRATE_TESTS') is not None:
    integrateTests = os.environ['INTEGRATE_TESTS']


@given('following csv file content')
def set_content_for_upload_as_csv_file(context):
    context.file = validate_and_convert_json_to_dict(context.text)


@when('sending post to "{url:String}" with auth token')
def sending_post_with_auth(context, url):
    assert_that(context.variable, is_not(None), "No context.variable set!")
    header = {'Authorization': 'Bearer ' + context.variable}
    assert_that(context.json, is_not(None))
    response = requests.post(url, json=context.json, headers=header)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    context.json = response.json()
    assert_that(context.json, is_not(None))


@when('sending get to "{url}" with auth token')
def sending_get(context, url):
    assert_that(context.variable, is_not(None), "No context.variable set!")
    header = {'Authorization': 'Bearer ' + context.variable}
    response = requests.get(url, headers=header)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    context.json = response.json()
    assert_that(context.json, is_not(None))


@when('sending get to "{url}" and query param "{query_params:String}"')
def get_endpoint_with_query_param(context, url, query_params):
    q_params = eval(query_params)  # query_params passed as python dictionary
    response = requests.get(url, params=q_params)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    try:
        context.json = response.json()
    except ValueError:  # no json available, so need to store it
        pass


@when('send delete to "{url}" with auth token')
def delete_endpoint_with_token(context, url):
    assert_that(context.variable, is_not(None), "No context.variable set!")
    header = {'Authorization': 'Bearer ' + context.variable}
    response = requests.delete(url, headers=header)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    try:
        context.json = response.json()
    except ValueError:  # no json available, so need to store it
        pass


@when('send post to "{url}" and query param "{query_params:String}" with auth token')
def post_endpoint_with_query_param_and_token(context, url, query_params):
    assert_that(context.variable, is_not(None), "No context.variable set!")
    header = {'Authorization': 'Bearer ' + context.variable}
    q_params = eval(query_params)  # query_params passed as python dictionary
    response = requests.post(url, headers=header, params=q_params, json=context.json)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    try:
        context.json = response.json()
    except ValueError:  # no json available, so need to store it
        pass


@when('sending delete to "{url}" and query param "{query_params:String}" with auth token')
def delete_endpoint_with_query_param_and_token(context, url, query_params):
    assert_that(context.variable, is_not(None), "No context.variable set!")
    header = {'Authorization': 'Bearer ' + context.variable}
    q_params = eval(query_params)  # query_params passed as python dictionary
    response = requests.delete(url, headers=header, params=q_params)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    try:
        context.json = response.json()
    except ValueError:  # no json available, so need to store it
        pass


@when('sending get to "{url}""{endpoint}"')
def sending_get(context, url, endpoint):
    response = requests.get(urls[url] + endpoint)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    context.json = response.json()
    assert_that(context.json, is_not(None))
    assert_that(context.json, is_not(None))


@when('sending post to "{url}""{endpoint}"')
def sending_post(context, url, endpoint):
    response = requests.post(urls[url] + endpoint, json=context.json)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    context.json = response.json()
    assert_that(context.json, is_not(None))


@when('sending post to "{url}"')
def sending_post_to_simple_url(context, url):
    response = requests.post(url, json=context.json)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    try:
        context.json = response.json()
    except ValueError:  # no json available
        pass


@when('sending get to "{url}"')
def sending_get_to_simple_url(context, url):
    response = requests.get(url)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    try:
        context.json = response.json()
    except:  # no json in response available
        pass


@when('send get to "{url}" append value of context variable "{last_uri_param_value}"')
def send_get_to_url_and_append_value_to_url(context, url, last_uri_param_value):
    response = requests.get(url + eval(last_uri_param_value))
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    try:
        context.json = response.json()
    except:  # no json in response available
        pass


# adds context.id to url
@when('send get to "{url}" with "{variable}"')
def sending_get_to_simple_url_with_id_appended(context, url, variable):
    response = requests.get(url + eval(variable))
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    context.json = response.json()
    assert_that(context.json, is_not(None))


# adds context.id to url
@when('send delete to "{url}" with "{variable}"')
def send_delete_to_simple_url_with_id_appended(context, url, variable):
    response = requests.delete(url + eval(variable))
    context.status_code = response.status_code
    try:
        context.json = response.json()
    except ValueError:  # no json available
        pass


@when('(bulk load) send "{number_of_requests:Number}" post requests to "{url:String}""{endpoint:String}"')
def send_load_of_post_requests(context, url, endpoint, number_of_requests):
    success_counter = 0
    failure_counter = 0
    for i in range(number_of_requests):
        response = requests.post(urls[url] + endpoint, json=context.json)
        if response.status_code == 200:
            success_counter = success_counter + 1
        else:
            failure_counter = failure_counter + 1
    assert_that(failure_counter, equal_to(0), "Failure count should be 0.")
    assert_that(success_counter, equal_to(number_of_requests), "Success count should be equal to number of requests.")


@then('expect response code "{status_code:Number}"')
def expect_status_code(context, status_code):
    json_string = ""
    try:
        json_string = context.json
    except AttributeError:
        pass
    check_response_code(context.status_code, status_code, json_string)


@then('sleep for "{secs}" sec(s)')
def sleep_for(context, secs):
    time.sleep(int(secs))


@when('sending request to "{url}""{endpoint}"')
def get_endpoint(context, url, endpoint):
    resp = requests.get(urls[url] + endpoint)
    assert_that(resp.status_code, equal_to(200))


@when('send delete to "{url}"')
def simple_delete_endpoint(context, url):
    response = requests.delete(url)
    context.status_code = response.status_code
    assert_that(context.status_code, not_none())
    try:
        context.json = response.json()
    except ValueError:  # no json available
        pass


@when('sending delete to "{url}""{endpoint}"')
def delete_endpoint(context, url, endpoint):
    response = requests.delete(urls[url] + endpoint)
    context.status_code = response.status_code
    assert_that(context.status_code, not_none())
    try:
        context.json = response.json()
    except ValueError:  # no json available
        pass


@given('following file "{file}"')
def following_file(context, file):
    context.file = file
    assert_that(context.file, not_none())


@given('read variable from yaml file "{yaml_file:String}" and read variable "{dict_entry:String}"')
def read_entry_from_yaml_file(context, yaml_file, dict_entry):
    try:
        with open(yaml_file) as a_yaml_file:
            parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)
            if not parsed_yaml_file:
                raise Exception("Error parsing YAML file from '{}'".format(yaml_file))
            context.variable = eval(str(parsed_yaml_file) + dict_entry)
        assert_that(context.variable, not_none(),
                    "No value found for variable '{}' from yaml file '{}'".format(dict_entry, yaml_file))
    except Exception as e:
        print("Exception >>>>> {}".format(str(e)))


@when('send file by post to "{url}""{endpoint}"')
def send_file_by_post(context, url, endpoint):
    assert_that(context.file, not_none(), "No file was set in context.")
    files = {'file': open(context.file, 'rb')}
    response = requests.post(urls[url] + endpoint, files=files)
    context.json = response.json()
    assert_that(context.json, not_none())
    assert_that(response.status_code, equal_to(200))


# Legacy: Don't use this step anymore !!!!
@DeprecationWarning
@given('request body in form of python dictionary')
def python_dictionary_request_body(context):
    assert_that(context.text, not_none(), "No dictionary was set to send as request body.")
    try:
        content = eval(context.text)
        file_content = content.get("fileContent")

        if file_content is not None:
            input_json = json.loads(re.sub(r'\'', '"', str(file_content)))

            # create a new csv file based on the given JSON save it and set the reference to this file in the context
            file_location = '/tests/files/file_for_eater.csv'
            create_csv_file_by_json(input_json, ";", file_location)
            content["uploadFile"] = eval("open('" + file_location + "', 'rb')")

            content.pop("fileContent")
            context.file = content
        else:
            context.file = content
    except Exception as e:
        print("Exception >>>>> {}".format(str(e)))


@when('send file by post to "{url}"')
def send_json_file_by_post(context, url):
    assert_that(context.file, not_none(), "No file was set in context.")
    files = context.file
    response = requests.post(url, files=files)
    context.json = response.json()
    context.status_code = response.status_code
    assert_that(context.json, not_none())


@when('sending put to "{url}"')
def sending_put_to_simple_url(context, url):
    response = requests.put(url, json=context.json)
    context.status_code = response.status_code
    assert_that(context.status_code, is_not(None))
    try:
        context.json = response.json()
    except ValueError:  # no json available
        pass


@when('send "{http_method}" to "{url}"')
def send_generic_http_request(context, http_method, url):
    converted_url = replace_context_var_with_value(url, context)
    if hasattr(context, 'json'):
        arguments = f"('{converted_url}', json=context.json)"
    else:
        arguments = f"('{converted_url}')"
    response = eval("requests." + str(http_method).lower() + arguments)
    context.status_code = response.status_code
    try:
        context.json = response.json()
    except ValueError:  # no json available
        pass


@given('header "{header_name}" is "{header_value}"')
def set_request_header(context, header_name, header_value):
    if not hasattr(context, "headers"):
        context.headers = {}
    context.headers[header_name] = header_value


@given('form-data "{field}" is "{value}"')
def set_form_data(context, field, value):
    if not hasattr(context, "form_data"):
        context.form_data = {}
    context.form_data[field] = value

@when('wait for "{msecs}" msecs')
def wait_for_msecs(context, msecs):
    try:
        milliseconds = int(msecs)
        time.sleep(milliseconds / 1000.0)  # Convert to seconds
    except ValueError:
        raise ValueError(f"Invalid milliseconds value: {msecs}")