import unittest
from services.behave_services import *


class TestBehaveServices(unittest.TestCase):

    def test_extract_results_single_test(self):
        text = """ 
                Feature: Test error behaviour # features/post_with_id.feature:1
                Scenario: POST a pet with ID - error response                                               # features/post_with_id.feature:3
                Given following json                                                                      # features/steps/json_steps.py:111 0.000s
                When sending POST to "http://springboot:8080/pets"                                        # features/steps/http_steps.py:117 0.091s
                Then expect response code "400"                                                           # features/steps/http_steps.py:185 0.000s
                And json attribute "["message"]" is equal to "Id in POST must be empty! Provided id: 999" # features/steps/json_steps.py:156 0.000s

            1 feature passed, 0 failed, 0 skipped
            1 scenario passed, 0 failed, 0 skipped
            1 step passed, 0 failed, 0 skipped, 0 undefined
            Took 0m0.092s
            """

        res = extract_results(text)
        self.assertEqual(res['Result'], 'Tests ended successfully ✅✅✅🍺🍺🍺')
        self.assertEqual(res['Features']['Passed'], 1)
        self.assertEqual(res['Features']['Failed'], 0)
        self.assertEqual(res['Features']['Skipped'], 0)

        self.assertEqual(res['Scenarios']['Passed'], 1)
        self.assertEqual(res['Scenarios']['Failed'], 0)
        self.assertEqual(res['Scenarios']['Skipped'], 0)

        self.assertEqual(res['Steps']['Passed'], 1)
        self.assertEqual(res['Steps']['Failed'], 0)
        self.assertEqual(res['Steps']['Skipped'], 0)

    def test_extract_results_multiple_test(self):
        text = """ something here 
            2 features passed, 0 failed, 0 skipped
            3 scenarios passed, 0 failed, 0 skipped
            8 steps passed, 0 failed, 0 skipped, 0 undefined
            Took 0m0.092s
            """
        res = extract_results(text)
        self.assertEqual(res['Result'], 'Tests ended successfully ✅✅✅🍺🍺🍺')
        self.assertEqual(res['Features']['Passed'], 2)
        self.assertEqual(res['Features']['Failed'], 0)
        self.assertEqual(res['Features']['Skipped'], 0)

        self.assertEqual(res['Scenarios']['Passed'], 3)
        self.assertEqual(res['Scenarios']['Failed'], 0)
        self.assertEqual(res['Scenarios']['Skipped'], 0)

    def test_extract_results_failure(self):
        text = """ 
            2 features passed, 1 failed, 88 skipped
            3 scenarios passed, 1 failed, 99 skipped
            8 steps passed, 0 failed, 0 skipped, 1 undefined
            Took 0m0.092s
            """
        res = extract_results(text)
        self.assertEqual(res['Result'], 'Tests ended with errors 🚨🚨🚨🙀🙀🙀')
        self.assertEqual(res['Features']['Passed'], 2)
        self.assertEqual(res['Features']['Failed'], 1)
        self.assertEqual(res['Features']['Skipped'], 88)

        self.assertEqual(res['Scenarios']['Passed'], 3)
        self.assertEqual(res['Scenarios']['Failed'], 1)
        self.assertEqual(res['Scenarios']['Skipped'], 99)

        self.assertEqual(res['Steps']['Passed'], 8)
        self.assertEqual(res['Steps']['Failed'], 0)
        self.assertEqual(res['Steps']['Skipped'], 0)
        self.assertEqual(res['Steps']['Undefined'], 1)

    def test_extract_not_implemented_exception(self):
        text = "You can implement step definitions for undefined steps with these snippets: def step_impl(context): raise NotImplementedError('STEP: Then expect 400')"
        extracted = extract_not_implemented_exception(text)
        self.assertEqual(extracted, "'STEP: Then expect 400'")

    def test_get_undefined_number_2(self):
        text = """ 
                   2 features passed, 1 failed, 88 skipped
                   3 scenarios passed, 1 failed, 99 skipped
                   8 steps passed, 0 failed, 0 skipped, 2 undefined
                   Took 0m0.092s
                   """
        res = get_undefined_steps_number(text)
        self.assertEqual(res, 2)

    def test_get_undefined_number_0(self):
        text = """ 
                   2 features passed, 1 failed, 88 skipped
                   3 scenarios passed, 1 failed, 99 skipped
                   8 steps passed, 0 failed, 0 skipped, 0 undefined
                   Took 0m0.092s
                   """
        res = get_undefined_steps_number(text)
        self.assertEqual(res, 0)

    def test_remove_ansi_codes(self):
        text = "Feature: Not implemented error - ALL INVALID\u001b[90m # features/all_test_invalid.feature:1\u001b[0m\n\n  Scenario: POST a pet with ID - error response \u001b[90m # features/all_test_invalid.feature:3\u001b[0m\n    \u001b[90mGiven \u001b[0m\u001b[90mfollowing json\u001b[0m\u001b[90m                         # features/steps/json_steps.py:111\u001b[0m\n      \"\"\"\n      {\n        \"id\": \"999\",\n        \"name\": \"Cat\"\n      }\n      \"\"\"\n\u001b[8A    \u001b[32mGiven \u001b[0m\u001b[32mfollowing json\u001b[0m\u001b[90m                         # features/steps/json_steps.py:111 0.000s\u001b[0m\n      \"\"\"\n      {\n        \"id\": \"999\",\n        \"name\": \"Cat\"\n      }\n      \"\"\"\n    \u001b[90mWhen \u001b[0m\u001b[90mPOST to \"http://springboot:8080/pets\"\u001b[0m\u001b[90m   # None\u001b[0m\n\u001b[1A    \u001b[33mWhen \u001b[0m\u001b[33mPOST to \"http://springboot:8080/pets\"\u001b[0m\u001b[90m   # None\u001b[0m\n    \u001b[36mThen \u001b[0m\u001b[36mexpect  \"400\"\u001b[0m\u001b[90m                           # None\u001b[0m\n\n  Scenario: 2nd scenario \u001b[90m                      # features/all_test_invalid.feature:15\u001b[0m\n    \u001b[90mGiven \u001b[0m\u001b[90mfollowing json\u001b[0m\u001b[90m                       # features/steps/json_steps.py:111\u001b[0m\n      \"\"\"\n      {\n        \"id\": \"999\",\n        \"name\": \"Cat\"\n      }\n      \"\"\"\n\u001b[8A    \u001b[32mGiven \u001b[0m\u001b[32mfollowing json\u001b[0m\u001b[90m                       # features/steps/json_steps.py:111 0.000s\u001b[0m\n      \"\"\"\n      {\n        \"id\": \"999\",\n        \"name\": \"Cat\"\n      }\n      \"\"\"\n    \u001b[90mWhen \u001b[0m\u001b[90mPOST to \"http://springboot:8080/pets\"\u001b[0m\u001b[90m # None\u001b[0m\n\u001b[1A    \u001b[33mWhen \u001b[0m\u001b[33mPOST to \"http://springboot:8080/pets\"\u001b[0m\u001b[90m # None\u001b[0m\n    \u001b[36mThen \u001b[0m\u001b[36mexpect  \"400\"\u001b[0m\u001b[90m                         # None\u001b[0m\n\n  Scenario: 3rd scenario \u001b[90m                      # features/all_test_invalid.feature:26\u001b[0m\n    \u001b[90mGiven \u001b[0m\u001b[90mfollowing json\u001b[0m\u001b[90m                       # features/steps/json_steps.py:111\u001b[0m\n      \"\"\"\n      {\n        \"id\": \"999\",\n        \"name\": \"Cat\"\n      }\n      \"\"\"\n\u001b[8A    \u001b[32mGiven \u001b[0m\u001b[32mfollowing json\u001b[0m\u001b[90m                       # features/steps/json_steps.py:111 0.000s\u001b[0m\n      \"\"\"\n      {\n        \"id\": \"999\",\n        \"name\": \"Cat\"\n      }\n      \"\"\"\n    \u001b[90mWhen \u001b[0m\u001b[90mPOST to \"http://springboot:8080/pets\"\u001b[0m\u001b[90m # None\u001b[0m\n\u001b[1A    \u001b[33mWhen \u001b[0m\u001b[33mPOST to \"http://springboot:8080/pets\"\u001b[0m\u001b[90m # None\u001b[0m\n    \u001b[36mThen \u001b[0m\u001b[36mexpect  \"400\"\u001b[0m\u001b[90m                         # None\u001b[0m\n\n\nFailing scenarios:\n  features/all_test_invalid.feature:3  POST a pet with ID - error response\n  features/all_test_invalid.feature:15  2nd scenario\n  features/all_test_invalid.feature:26  3rd scenario\n\n0 features passed, 1 failed, 0 skipped\n0 scenarios passed, 3 failed, 0 skipped\n3 steps passed, 0 failed, 0 skipped, 6 undefined\nTook 0m0.000s\n"
        res = remove_ansi_codes(text)
        # print(res)

    def test_delete_test_file_from_fs_failure(self):
        with self.assertRaises(FileNotFoundError) as context:
            delete_file_from_fs("unknown_file")
        self.assertEqual(str(context.exception), "Cannot delete file 'unknown_file'")

    def test_delete_test_file_from_fs_success(self):
        location = "filename.feature"
        write_file_with_content("content", location)
        delete_file_from_fs(location)
        self.assertEqual(os.path.exists(location), False)
