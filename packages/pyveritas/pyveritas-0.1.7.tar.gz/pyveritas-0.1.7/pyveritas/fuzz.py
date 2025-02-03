import re
import exrex
import random
import string
import concurrent.futures
from pyveritas.base import VeritasBase
from pyveritas.base import logger


class VeritasFuzzer(VeritasBase):
    """
    A fuzz testing utility for dynamically testing functions with randomized inputs.
    """

    def _generate_value(self, input_spec):
        name = input_spec["name"]
        if "value" in input_spec:
            if "regular_expression" in input_spec or "range" in input_spec:
                logger.warning(
                    f"Warning: 'value' precedence over 'regular_expression'/'range' for {name}"
                )
            return input_spec["value"]

        if "regular_expression" in input_spec:
            regex = input_spec["regular_expression"]
            value = next(exrex.generate(regex))
            return self._convert_value(value, input_spec["type"])

        if "range" in input_spec:
            range_spec = input_spec["range"]
            min_value, max_value = range_spec["min"], range_spec["max"]
            if min_value > max_value:
                raise ValueError(
                    f"Invalid range for {name}: min {min_value} must be less than max {max_value}"
                )
            if input_spec["type"] == "float":
                return random.uniform(min_value, max_value)
            elif input_spec["type"] == "int":
                return random.randint(min_value, max_value)
            else:
                raise ValueError(
                    f"Unsupported input type for range: {input_spec['type']}"
                )

        raise ValueError(
            f"Either 'value', 'regular_expression', or 'range' must be specified for input '{name}'."
        )

    def _convert_value(self, value, data_type):
        if data_type == "int":
            return int(value)
        elif data_type == "float":
            return float(value)
        else:
            return value

    def _run_single_test(self, func, case, i):
        input_params = {}
        for input_spec in case.get("input", []):
            input_params[input_spec["name"]] = self._generate_value(input_spec)

        expected_exception = case.get("exception", None)
        exception_message = case.get("exception_message", None)

        try:
            result = func(**input_params)
            self._evaluate_test(
                f"FuzTest {i}",
                input_params,
                result,
                expected_exception,
                exception_message,
            )
        except Exception as e:
            self._evaluate_test(
                f"FuzTest {i}", input_params, e, expected_exception, exception_message
            )

    def run(self, parallel=True):
        iterations = 100
        logger.info(f"Running fuzz tests for suite: {self.name}")
        # iterations = self.test_cases[0].get('iterations', 100)
        for desc, func, test_cases in self.test_cases:
            iterations = test_cases.get("iterations", 100)
            logger.info(f"\nTEST CASES: {test_cases}")
            print(f"\Test cases: {test_cases}")

            if parallel:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    futures = [
                        executor.submit(self._run_single_test, func, test_cases, i)
                        for i in range(iterations)
                    ]
                    concurrent.futures.wait(futures)
            else:
                for i in range(iterations):
                    self._run_single_test(func, test_cases, i)
