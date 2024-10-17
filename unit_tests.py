
import unittest
import sys
import os

# Ensure the script directory is in the Python path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Adjust this to match your main script name
from st import transform, resolve_template  

class TestTemplateEngine(unittest.TestCase):

    def test_basic_interpolation(self):
        template = {"greeting": "{{'Hello, ' + name}}"}
        context = {"name": "Yoda"}
        expected = {"greeting": "Hello, Yoda"}
        result = transform(template, context)
        self.assertEqual(result, expected)

    def test_each_directive(self):
        template = {
            "quotes": {
                "#each": "quotes",
                "template": {"text": "{{text}}"}
            }
        }
        context = {
            "quotes": [
                {"text": "Do or do not, there is no try."},
                {"text": "Fear is the path to the dark side."}
            ]
        }
        expected = {
            "quotes": [
                {"text": "Do or do not, there is no try."},
                {"text": "Fear is the path to the dark side."}
            ]
        }
        result = transform(template, context)
        self.assertEqual(result, expected)

    def test_if_directive_true(self):
        template = {
            "status": {
                "#if": {
                    "condition": "{{active}}",
                    "#then": "Active",
                    "#else": "Inactive"
                }
            }
        }
        context = {"active": True}
        expected = {"status": "Active"}
        result = transform(template, context)
        self.assertEqual(result, expected)

    def test_if_directive_false(self):
        template = {
            "status": {
                "#if": {
                    "condition": "{{active}}",
                    "#then": "Active",
                    "#else": "Inactive"
                }
            }
        }
        context = {"active": False}
        expected = {"status": "Inactive"}
        result = transform(template, context)
        self.assertEqual(result, expected)

    def test_complex_interpolation(self):
        template = {
            "message": "{{'May the force be with ' + character}}"
        }
        context = {"character": "you"}
        expected = {"message": "May the force be with you"}
        result = transform(template, context)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()