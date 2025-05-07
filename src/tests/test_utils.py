# Importing the `unittest` module, which is a built-in Python library
# used for writing and running tests.
import unittest

# Importing the `get_message` function from the `utils` module in the `src.app` package.
# This is the function we are going to test.
from src.app.utils import get_message

# Defining a test class `TestUtils` that inherits from `unittest.TestCase`.
# This class contains test cases for the `utils` module.
class TestUtils(unittest.TestCase):
    # Defining a test method to check if `get_message` returns the expected output.
    def test_get_message(self):
        # Using `assertEqual` to verify that the output of `get_message`
        # matches the expected string "Hello from InfraAuditAI!".
        self.assertEqual(get_message(), "Hello from InfraAuditAI!")

# This block ensures that the tests are executed only when this script
# is run directly (not when imported as a module).
if __name__ == '__main__':
    # Running all the test cases defined in the `TestUtils` class.
    unittest.main()
