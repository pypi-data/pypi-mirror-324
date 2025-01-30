import re
import random
import string
from colorama import Fore, Style

class VeritasFuzzer:
    """
    A fuzz testing utility for dynamically testing functions with randomized inputs.

    Attributes:
        name (str): The name of the function or module being tested.
        passed (int): The number of successful fuzz tests.
        failed (int): The number of failed fuzz tests.
        failed_inputs (list): A list of inputs and exceptions for failed tests.
        test_cases (list): A list of test cases, each containing input specifications, expected outputs, and expected exceptions.
        iterations (int): The number of fuzz test iterations.
    """

    @staticmethod
    def choice(options):
        """
        Returns a random element from a list of options.

        Args:
            options (list): A list of possible values.
        
        Returns:
            Any: A randomly chosen value from the options.
        """
        return random.choice(options)

    @staticmethod
    def float_range(min_value, max_value):
        """
        Generates a random floating-point number within a specified range.

        Args:
            min_value (float): The lower bound of the range.
            max_value (float): The upper bound of the range.

        Returns:
            float: A randomly generated float within the range.
        """
        return random.uniform(min_value, max_value)

    @staticmethod
    def int_range(min_value, max_value):
        """
        Generates a random integer within a specified range.

        Args:
            min_value (int): The lower bound of the range.
            max_value (int): The upper bound of the range.

        Returns:
            int: A randomly generated integer within the range.
        """
        return random.randint(min_value, max_value)

    @staticmethod
    def char_range(start_char, end_char):
        """
        Generates a random character within a specified range.

        Args:
            start_char (str): The starting character of the range.
            end_char (str): The ending character of the range.

        Returns:
            str: A randomly generated character within the range.
        """
        return chr(random.randint(ord(start_char), ord(end_char)))

    @staticmethod
    def string_range(length, start_char='a', end_char='z'):
        """
        Generates a random string of specified length with characters within a specified range.

        Args:
            length (int): The length of the string to generate.
            start_char (str): The starting character of the range.
            end_char (str): The ending character of the range.

        Returns:
            str: A randomly generated string within the specified character range.
        """
        return ''.join(VeritasFuzzer.char_range(start_char, end_char) for _ in range(length))

    def __init__(self, name):
        """
        Initializes the fuzzer with a name and default parameters.

        Args:
            name (str): The name of the fuzzing task.
        """
        self.name = name
        self.passed = 0
        self.failed = 0
        self.failed_inputs = []
        self.test_cases = []
        self.iterations = 100

    def test(self, test_cases, iterations=100):
        """
        Defines the test cases and number of iterations for fuzzing.

        Args:
            test_cases (list of dicts): A list of test cases, each containing input specifications, expected outputs, and expected exceptions.
            iterations (int, optional): The number of test iterations. Default is 100.
        """
        self.test_cases = test_cases
        self.iterations = iterations

    def run(self, function):
        """
        Executes fuzz tests on a specified function.

        Args:
            function (callable): The function to be fuzz-tested.

        Raises:
            ValueError: If `test()` is not called before running.
        """
        if not self.test_cases:
            raise ValueError("Test cases not set. Please call 'test()' first.")
        
        print(f"Running fuzz tests on function: {function.__name__}")
        for i in range(self.iterations):
            # Randomly select a test case
            case = random.choice(self.test_cases)
            inputs = case.get("input", {})
            expected_output = case.get("expected_output", None)
            expected_exception = case.get("expected_exception", None)

            # Automatically generate inputs if not provided
            for key, value in inputs.items():
                if isinstance(value, dict) and "range" in value:
                    min_val, max_val = value["range"]
                    if isinstance(min_val, float) or isinstance(max_val, float):
                        inputs[key] = self.float_range(min_val, max_val)
                    elif isinstance(min_val, int) or isinstance(max_val, int):
                        inputs[key] = self.int_range(min_val, max_val)
                    elif isinstance(min_val, str) and isinstance(max_val, str):
                        inputs[key] = self.char_range(min_val, max_val)

            try:
                result = function(**inputs)
                if expected_exception:
                    # If an exception was expected but not raised, it's a failure
                    self.failed += 1
                    self.failed_inputs.append((inputs, f"Expected exception: {expected_exception}, but no exception was raised"))
                    print(f"{Fore.RED}Fuzzing iteration {i+1}: FAILED with inputs {inputs} (Expected exception: {expected_exception}, but no exception was raised){Style.RESET_ALL}")
                elif expected_output is not None and result != expected_output:
                    # If the output doesn't match the expected output, it's a failure
                    self.failed += 1
                    self.failed_inputs.append((inputs, f"Expected: {expected_output}, Got: {result}"))
                    print(f"{Fore.RED}Fuzzing iteration {i+1}: FAILED with inputs {inputs} (Expected: {expected_output}, Got: {result}){Style.RESET_ALL}")
                else:
                    # If no exception was expected and the output matches, it's a success
                    self.passed += 1
                    print(f"{Fore.GREEN}Fuzzing iteration {i+1}: PASSED with inputs {inputs}{Style.RESET_ALL}")
            except Exception as e:
                if expected_exception and isinstance(e, expected_exception):
                    # If the expected exception was raised, it's a success
                    self.passed += 1
                    print(f"{Fore.GREEN}Fuzzing iteration {i+1}: PASSED with inputs {inputs} (Expected exception raised: {e}){Style.RESET_ALL}")
                else:
                    # If an unexpected exception was raised, it's a failure
                    self.failed += 1
                    self.failed_inputs.append((inputs, e))
                    print(f"{Fore.RED}Fuzzing iteration {i+1}: FAILED with inputs {inputs} (Exception: {e}){Style.RESET_ALL}")

    def summary(self):
        """
        Prints a summary of the fuzzing results, including passed and failed iterations.
        """
        print("\n" + "-" * 40)
        print(f"Fuzzing Summary for Function: {self.name}")
        print(f"Total Iterations: {self.passed + self.failed}")
        print(f"{Fore.GREEN}Passed: {self.passed}{Style.RESET_ALL}")
        print(f"{Fore.RED}Failed: {self.failed}{Style.RESET_ALL}")
        if self.failed_inputs:
            print("\nFailed Inputs:")
            for inputs, e in self.failed_inputs:
                print(f"  - Inputs: {inputs}, Exception: {e}")