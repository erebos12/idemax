import unittest

from utils import *
from config import *


class TestUtils(unittest.TestCase):

    def test_parse_json(self):
        json_dict = '{"gg" : "1"}'
        res = validate_and_convert_json_to_dict(json_dict)
        self.assertIs(res['gg'], '1')

    def test_parse_invalid_json(self):
        invalid = '"gg" : 1'
        with self.assertRaises(Exception):
            validate_and_convert_json_to_dict(invalid)

        invalid = "{'gg' : '1'}"
        with self.assertRaises(Exception):
            validate_and_convert_json_to_dict(invalid)

    def test_parse_None_as_json_string(self):
        with self.assertRaises(Exception):
            validate_and_convert_json_to_dict(None)

    def test_convert_json_to_csv(self):
        content = """[{"anlagennummer": "123", "anlagenbezeichnung": "Asset 1", "anlagen_klasse_nr": "1040"}]"""
        json_dict = validate_and_convert_json_to_dict(content)
        csv_content = convert_json_to_csv(json_dict, DELIMITER)

        expected_header = "anlagennummer;anlagenbezeichnung;anlagen_klasse_nr"
        expected_data = "123;Asset 1;1040"
        self.assertIn(expected_header, csv_content)
        self.assertIn(expected_data, csv_content)

        content = """[{"anlagennummer": "1", "anlagenbezeichnung": "A", "anlagen_klasse_nr": "10"}, {"anlagennummer": "2", "anlagenbezeichnung": "B", "anlagen_klasse_nr": "10"}]"""
        json_dict = validate_and_convert_json_to_dict(content)
        csv_content = convert_json_to_csv(json_dict, DELIMITER)

        expected_header = "anlagennummer;anlagenbezeichnung;anlagen_klasse_nr"
        expected_data = "1;A;10\n2;B;10"
        self.assertIn(expected_header, csv_content)
        self.assertIn(expected_data, csv_content)

    def test_create_file(self):
        file_name = "test.csv"
        create_file("", file_name)
        self.assertTrue(os.path.exists(file_name))

    def test_delete_file(self):
        file_name = "test.csv"
        create_file("", file_name)
        self.assertTrue(os.path.exists(file_name))
        delete_file(file_name)
        self.assertFalse(os.path.exists(file_name))
        delete_file("unknown.txt")
        self.assertFalse(os.path.exists(file_name))

    def test_get_json_attribute_value(self):
        json_str = """
        {            
           "yearId": "12345",
           "masterConfigName": "test config1"                  
        }
        """
        self.json = json.loads(json_str)
        self.assertIsNotNone(self.json)

        year_id = get_json_attribute_value(self, '["yearId"]')
        self.assertEqual("12345", year_id)
        master_config_name = get_json_attribute_value(self, '["masterConfigName"]')
        self.assertEqual("test config1", master_config_name)

    def test_store_value_in_context_attribute(self):
        store_value_in_context_attribute(self, "test", "id2")
        self.assertEqual("test", self.id2)

    def test_replace_context_var_with_value(self):
        class context():
            var1 = 42
            var2 = "lala"

        res = replace_context_var_with_value("https://erase/(context.var1)/(context.var2)", context)
        self.assertEqual(res, "https://erase/42/lala")
        res = replace_context_var_with_value("https://erase/42/anyValue", context)
        self.assertEqual(res, "https://erase/42/anyValue")

    def test_replace_context_var_with_value_exception(self):
        with self.assertRaises(AttributeError) as ex:
            replace_context_var_with_value("https://erase/(context.unknown)", ex)
        self.assertTrue("object has no attribute 'unknown'" in str(ex.exception))

    def test_eval_string(self):
        class context():
            var1 = 42
            var2 = "lala"

        res = eval_string(context, "1 + context.var1")
        self.assertEqual(res, "43")
        res = eval_string(context, "context.var2")
        self.assertEqual(res, "lala")
        with self.assertRaises(AttributeError) as ex:
            eval_string(context, "1 + context.unknownVariable")
        self.assertEqual("type object 'context' has no attribute 'unknownVariable'", str(ex.exception))


if __name__ == '__main__':
    unittest.main()
