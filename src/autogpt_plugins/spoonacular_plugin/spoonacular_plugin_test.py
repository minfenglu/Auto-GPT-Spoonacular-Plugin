import http.client
import json
import os
import unittest
from functools import partial
from unittest.mock import patch
from unittest.mock import mock_open
from spoonacular_plugin import Chef


MOCK_HOST = "MOCK_HOST"
MOCK_SPOONACULAR_API_KEY = "test_spoonacular_api_key"
MOCK_DATA_LOCATION = "test_data"
MOCK_SEARCH_RECIPE_RESPONSE = "paneer_recipes.json"
MOCK_RECIPE_INSTRUCTION_RESPONSE = "paneer_tikka_instructions.json"


class MockHttpResponse:
    def __init__(self, test_data: str):
        json_file_path = os.path.join(
            os.path.dirname(__file__), os.path.join(MOCK_DATA_LOCATION, test_data)
        )
        with open(json_file_path) as json_file:
            json_data = json.loads(json_file.read())
            self.bytes_data = bytes(json.dumps(json_data), "utf-8")

    def read(self):
        return self.bytes_data


class TestSpoonacularPlugin(unittest.TestCase):
    @unittest.mock.patch.dict(
        os.environ, {"SPOONACULAR_API_KEY": MOCK_SPOONACULAR_API_KEY}
    )
    def setUp(self) -> None:
        self.chef = Chef()

    @unittest.mock.patch.dict(
        os.environ, {"SPOONACULAR_API_KEY": MOCK_SPOONACULAR_API_KEY}
    )
    def test_api_key_set(self):
        self.assertTrue(self.chef.api_key_set())

    @patch("http.client.HTTPSConnection.request")
    @patch("http.client.HTTPSConnection.getresponse")
    def test_search_recipes(self, mock_getresponse, mock_request):
        mock_request.side_effect = [http.client.HTTPConnection(MOCK_HOST)]
        mock_getresponse.side_effect = [MockHttpResponse(MOCK_SEARCH_RECIPE_RESPONSE)]
        ids, recipes = self.chef.search_recipes("paneer")
        self.assertEqual(
            ids,
            [
                674506,
                1674557,
                609175,
                654534,
                667926,
                654532,
                22202,
                617061,
                1084087,
                654523,
            ],
        )
        self.assertEqual(
            recipes,
            [
                "Paneer Tikka (Version 1)",
                "Paneer Tikka (Version 2)",
                "Paneer Tikka (Version 3)",
                "Paneer Makhani (Version 1)",
                "Paneer Makhani (Version 2)",
                "Paneer jalfrezi",
                "Paneer Jalfrezi",
                "Paneer Do Pyaza",
                "Paneer Manchurian",
                "Paneer & Fig Pizza",
            ],
        )

    @patch("http.client.HTTPSConnection.request")
    @patch("http.client.HTTPSConnection.getresponse")
    def test_get_analyzed_recipe_instructions(self, mock_getresponse, mock_request):
        mock_request.side_effect = [http.client.HTTPConnection(MOCK_HOST)]
        mock_getresponse.side_effect = [
            MockHttpResponse(MOCK_RECIPE_INSTRUCTION_RESPONSE)
        ]
        instructions = self.chef.get_analyzed_recipe_instructions(674506)
        self.assertEqual(len(instructions), 6)


if __name__ == "__main__":
    unittest.main()
