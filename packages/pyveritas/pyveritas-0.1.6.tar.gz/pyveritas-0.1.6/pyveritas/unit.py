from pyveritas.base import VeritasBase
from pyveritas.base import logger


class VeritasUnitTester(VeritasBase):
    """
    A suite for running unit tests with customizable test cases and result summaries.
    """

    def run(self):
        """
        Executes all tests in the suite and reports results, handling flexible input and output specifications.
        """
        for desc, func, case in self.test_cases:
            logger.info(f"\nCase: {case}")
            input_params = {}
            for input_spec in case.get("input", []):
                name = input_spec["name"]
                if "value" in input_spec:
                    input_params[name] = input_spec["value"]
                    if "regular_expression" in input_spec or "range" in input_spec:
                        logger.warning(
                            f"Warning: 'value' precedence over 'regular_expression'/'range' for {name}"
                        )
                else:
                    logger.error(
                        f"Error: Missing 'value' for input {name} in unit test mode."
                    )
                    continue  # Skip this test if value is not provided

            expected_exception = case.get("exception", None)
            exception_message = case.get("exception_message", None)

            try:
                result = func(**input_params)
                self._evaluate_test(
                    desc, input_params, result, expected_exception, exception_message
                )
            except Exception as e:
                self._evaluate_test(
                    desc, input_params, e, expected_exception, exception_message
                )
