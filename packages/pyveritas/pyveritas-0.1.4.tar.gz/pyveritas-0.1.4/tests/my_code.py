import argparse
from pyveritas import VeritasTestSuite, VeritasFuzzer

# Function to test
def calculate_discount(price: float, discount: float) -> float:
    """
    Calculates the discounted price.
    
    Args:
        price (float): The original price.
        discount (float): The discount percentage.
    
    Returns:
        float: The final price after applying the discount.
    
    Raises:
        ValueError: If the price is non-positive or discount is out of range.
    """
    if price <= 0 or discount < 0 or discount > 100:
        raise ValueError("Invalid price or discount")
    return price * (1 - discount / 100)
# Add these new functions and tests to your existing my_code.py file

# New function to test string_range
def reverse_string(the_string: str) -> str:
    """
    Reverses a given string.

    Args:
        the_string (str): The string to reverse.

    Returns:
        str: The reversed string.

    Raises:
        ValueError: If the input is not a string.
    """
    if not isinstance(the_string, str):
        raise ValueError("Input must be a string")
    return the_string[::-1]

# New function to test char_range
def is_single_vowel(the_character: str) -> bool:
    """
    Checks if a given character is a vowel (a, e, i, o, u).

    Args:
        the_character (str): The character to check.

    Returns:
        bool: True if the character is a vowel, False otherwise.

    Raises:
        ValueError: If the input is not a single character.
    """
    if not isinstance(the_character, str) or len(the_character) != 1:
        raise ValueError("Input must be a single character")
    return the_character.lower() in {'a', 'e', 'i', 'o', 'u'}

def run_tests():
    """Runs unit tests using VeritasTestSuite."""
    suite = VeritasTestSuite("DiscountCalculatorTests")
    
    # Test valid discount calculations
    suite.test(
        "Valid discount calculation",
        calculate_discount,
        test_cases=[
            {"input": {"price": 100, "discount": 20}, "expected_output": 80},
            {"input": {"price": 50, "discount": 10}, "expected_output": 45},
            {"input": {"price": 200, "discount": 50}, "expected_output": 100},
        ]
    )
    
    # Test invalid discount scenarios
    suite.test(
        "Invalid discount should raise ValueError",
        calculate_discount,
        test_cases=[
            {"input": {"price": -10, "discount": 50}, "expected_exception": ValueError},
            {"input": {"price": 100, "discount": -5}, "expected_exception": ValueError},
            {"input": {"price": 100, "discount": 150}, "expected_exception": ValueError},
        ]
    )

    # Test reverse_string function
    suite.test(
        "Reverse string",
        reverse_string,
        test_cases=[
            {"input": {"the_string": "hello"}, "expected_output": "olleh"},
            {"input": {"the_string": "python"}, "expected_output": "nohtyp"},
            {"input": {"the_string": "12345"}, "expected_output": "54321"},
            {"input": {"the_string": 12345}, "expected_exception": ValueError},  # Invalid input, should raise ValueError
        ]
    )

    # Test is_single_vowel function
    suite.test(
        "Check if character is a vowel",
        is_single_vowel,
        test_cases=[
            {"input": {"the_character": "a"}, "expected_output": True},
            {"input": {"the_character": "E"}, "expected_output": True},
            {"input": {"the_character": "z"}, "expected_output": False},
            {"input": {"the_character": "1"}, "expected_output": False},
            {"input": {"the_character": "ab"}, "expected_exception": ValueError},  # Invalid input, should raise ValueError
        ]
    )
    
    suite.run()
    suite.summary()

def run_fuzz_tests():
    """Runs fuzz tests using VeritasFuzzer."""
    fuzzer = VeritasFuzzer("DiscountCalculatorFuzzing")
    
    # Define test cases for fuzzing with automatic input generation
    fuzzer.test(
        test_cases=[
            {"input": {"price": {"range": (0.1, 1000.0)}, "discount": {"range": (0.0, 100.0)}}, "expected_output": None},
            {"input": {"price": {"range": (-100.0, 0.0)}, "discount": {"range": (0.0, 100.0)}}, "expected_exception": ValueError},
            {"input": {"price": {"range": (0.1, 1000.0)}, "discount": {"range": (-10.0, 0.0)}}, "expected_exception": ValueError},
            {"input": {"price": {"range": (0.1, 1000.0)}, "discount": {"range": (100.0, 150.0)}}, "expected_exception": ValueError},
        ],
        iterations=1000,
    )

    # Fuzz test for reverse_string function
    fuzzer_string = VeritasFuzzer("ReverseStringFuzzing")
    fuzzer_string.test(
        test_cases=[
            {"input": {"the_string": {"range": ("a", "z"), "length": 5}}, "expected_output": None},  # Random 5-letter string
            {"input": {"the_string": {"range": ("A", "Z"), "length": 10}}, "expected_output": None},  # Random 10-letter uppercase string
            {"input": {"the_string": {"range": ("0", "9"), "length": 3}}, "expected_output": None},  # Random 3-digit string
        ],
        iterations=500,
    )

    # Fuzz test for is_single_vowel function
    fuzzer_char = VeritasFuzzer("IsVowelFuzzing")
    fuzzer_char.test(
        test_cases=[
            {"input": {"the_character": {"range": ("a", "z")}}, "expected_output": None},  # Random lowercase character
            {"input": {"the_character": {"range": ("A", "Z")}}, "expected_output": None},  # Random uppercase character
            {"input": {"the_character": {"range": ("0", "9")}}, "expected_output": False},  # Random digit (should not be a vowel)
        ],
        iterations=500,
    )
    
    fuzzer.run(calculate_discount)
    fuzzer_string.run(reverse_string)
    fuzzer_char.run(is_single_vowel)
    fuzzer.summary()

def main():
    parser = argparse.ArgumentParser(description="Run unit tests or fuzz tests with PyVeritas.")
    parser.add_argument('action', choices=['test', 'fuzz'], help="Specify 'test' for unit tests or 'fuzz' for fuzzing tests.")
    args = parser.parse_args()
    
    if args.action == 'test':
        run_tests()
    elif args.action == 'fuzz':
        run_fuzz_tests()

if __name__ == "__main__":
    main()