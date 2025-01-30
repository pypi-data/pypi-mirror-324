import argparse
from colorama import Fore, Style

class VeritasTestSuite:
    """
    A suite for running unit tests with customizable test cases and result summaries.

    Attributes:
        name (str): The name of the test suite.
        tests (list): A list of tests, each represented by a tuple (description, test_function, test_cases).
        passed (int): The number of tests that passed.
        failed (int): The number of tests that failed.
        failed_tests (list): A list of failed test descriptions.
    """

    def __init__(self, name):
        """
        Initializes the test suite with a name.

        Args:
            name (str): The name of the test suite.
        """
        self.name = name
        self.tests = []
        self.passed = 0
        self.failed = 0
        self.failed_tests = []

    def test(self, description, test_function, test_cases):
        """
        Adds a test case to the suite, supporting flexible input and output specifications.

        Args:
            description (str): A brief description of the test case.
            test_function (callable): The function to be tested.
            test_cases (list of dicts): A list of dictionaries specifying the input parameters, expected outputs, and expected exceptions.
        """
        self.tests.append((description, test_function, test_cases))

    def run(self):
        """
        Executes all tests in the suite and reports results, handling flexible input and output specifications.
        """
        print(f"Running test suite: {self.name}")
        for i, (desc, func, test_cases) in enumerate(self.tests, 1):
            for case in test_cases:
                input_params = case.get("input", {})
                expected_output = case.get("expected_output", None)
                expected_exception = case.get("expected_exception", None)

                try:
                    # Call the function with the current input parameters
                    result = func(**input_params)

                    if expected_exception:
                        # If an exception was expected but not raised, it's a failure
                        self.failed += 1
                        self.failed_tests.append(f"{desc} with params {input_params} (Expected exception: {expected_exception}, but no exception was raised)")
                        print(f"{Fore.RED}Test {i} FAILED: {desc} with params {input_params} (Expected exception: {expected_exception}, but no exception was raised){Style.RESET_ALL}")
                    elif expected_output is not None and result != expected_output:
                        # If the output doesn't match the expected output, it's a failure
                        self.failed += 1
                        self.failed_tests.append(f"{desc} with params {input_params} (Expected: {expected_output}, Got: {result})")
                        print(f"{Fore.RED}Test {i} FAILED: {desc} with params {input_params} (Expected: {expected_output}, Got: {result}){Style.RESET_ALL}")
                    else:
                        # If no exception was expected and the output matches, it's a success
                        self.passed += 1
                        print(f"{Fore.GREEN}Test {i} PASSED: {desc} with params {input_params}{Style.RESET_ALL}")
                except Exception as e:
                    if expected_exception and isinstance(e, expected_exception):
                        # If the expected exception was raised, it's a success
                        self.passed += 1
                        print(f"{Fore.GREEN}Test {i} PASSED: {desc} with params {input_params} (Expected exception raised: {e}){Style.RESET_ALL}")
                    else:
                        # If an unexpected exception was raised, it's a failure
                        self.failed += 1
                        self.failed_tests.append(f"{desc} with params {input_params} (Unexpected exception: {e})")
                        print(f"{Fore.RED}Test {i} FAILED: {desc} with params {input_params} (Unexpected exception: {e}){Style.RESET_ALL}")

    def summary(self):
        """
        Prints a summary of test results, including passed and failed tests.
        """
        print("\n" + "-" * 40)
        print(f"Test Summary for Suite: {self.name}")
        print(f"Total Tests Run: {len(self.tests)}")
        print(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        if self.failed_tests:
            print("\nFailed Tests:")
            for failure in self.failed_tests:
                print(f"  - {failure}")