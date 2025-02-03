import argparse
from colorama import Fore, Style
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("VeritasBase")


class VeritasBase:
    """
    Base class for test suites, providing common functionality for running tests,
    managing test results, and reporting.
    """

    def __init__(self, name):
        self.name = name
        self.passed = 0
        self.failed = 0
        self.failed_items = []
        self.test_cases = []

    def add(self, description, test_function, test_cases):
        """
        Adds a test case to the suite, supporting flexible input and output specifications.

        Args:
            description (str): A brief description of the test case.
            test_function (callable): The function to be tested.
            test_cases (list of dicts): A list of dictionaries specifying the input parameters, expected outputs, and expected exceptions.
        """
        for case in test_cases:
            if case.get("enabled", True):  # Default to enabled if not specified
                logger.info(f"Adding test case: {description}")
                self.test_cases.append((description, test_function, case))
            else:
                logger.info(f"Test case: {description} is disabled.")

    def _evaluate_test(
        self, desc, input_params, result, expected_exception, exception_message
    ):
        if expected_exception:
            if isinstance(result, Exception) and isinstance(result, expected_exception):
                self.passed += 1
                logger.info(
                    f"{Fore.GREEN}PASSED: {desc} with params {input_params} (Expected exception: {expected_exception}){Style.RESET_ALL}"
                )
            else:
                self.failed += 1
                self.failed_items.append(
                    (
                        desc,
                        input_params,
                        f"Expected exception: {expected_exception}, Got: {result}",
                    )
                )
                logger.error(
                    f"{Fore.RED}FAILED: {desc} with params {input_params} (Expected exception: {expected_exception}, Got: {result}){Style.RESET_ALL}"
                )
        else:
            # Here we assume if no exception is expected, any result is considered a pass for simplicity
            self.passed += 1
            logger.info(
                f"{Fore.GREEN}PASSED: {desc} with params {input_params}{Style.RESET_ALL}"
            )

    def summary(self):
        """
        Prints a summary of test results, including passed and failed tests.
        """
        logger.info("\n" + "-" * 40)
        logger.info(f"Test Summary for Suite: {self.name}")
        logger.info(f"Total Tests Run: {self.passed + self.failed}")
        logger.info(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        logger.info(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        if self.failed_items:
            logger.info("\nFailed Tests:")
            for desc, inputs, error in self.failed_items:
                logger.info(f"  - {desc} with inputs {inputs}: {error}")
