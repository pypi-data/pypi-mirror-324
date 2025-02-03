import argparse
from pyveritas.unit import VeritasUnitTester
from pyveritas.fuzz import VeritasFuzzer

def convert_celsius_to_fahrenheit(celsius):
    """Convert temperature from Celsius to Fahrenheit."""
    return (celsius * 9/5) + 32

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two points on earth in kilometers."""
    from math import radians, sin, cos, sqrt, atan2
    R = 6371  # Earth radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c

def validate_ip_address(ip):
    """Validate if the given string is a valid IP address."""
    import re
    pattern = re.compile(r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$')
    return bool(pattern.match(ip))

def validate_email(email):
    """Validate if the given string is a valid email address."""
    import re
    pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    return bool(pattern.match(email))

def original_script_logic():
    """Demonstrates the functionality of each function with example parameters."""
    print(f"Convert 25°C to Fahrenheit: {convert_celsius_to_fahrenheit(25)}°F")
    print(f"Distance between Berlin and London: {calculate_distance(52.5200, 13.4050, 51.5074, -0.1278):.2f} km")
    print(f"IP Address '192.168.0.1' valid: {validate_ip_address('192.168.0.1')}")
    print(f"IP Address '256.1.2.3' valid: {validate_ip_address('256.1.2.3')}")
    print(f"Email 'test@example.com' valid: {validate_email('test@example.com')}")
    print(f"Email 'invalid.email@' valid: {validate_email('invalid.email@')}")

def run_unit_tests():
    """Runs unit tests for the IoT functions."""
    unit_tester = VeritasUnitTester("IoT Unit Tests")
    
    # Unit Tests
    unit_tester.add(
        "Convert 0°C to 32°F",
        convert_celsius_to_fahrenheit,
        [{"input": [{"name": "celsius", "value": 0}], "output": [{"name": "result", "value": 32, "type": "float"}]}]
    )

    unit_tester.add(
        "Calculate distance between two points",
        calculate_distance,
        [
            {
                "input": [
                    {"name": "lat1", "value": 52.5200, "type": "float"},
                    {"name": "lon1", "value": 13.4050, "type": "float"},
                    {"name": "lat2", "value": 51.5074, "type": "float"},
                    {"name": "lon2", "value": -0.1278, "type": "float"}
                ],
                "output": [{"name": "distance", "value": 925.8, "type": "float"}]  # Approximate distance in km
            }
        ]
    )

    unit_tester.add(
        "Validate IP Address",
        validate_ip_address,
        [
            {"input": [{"name": "ip", "value": "192.168.0.1"}], "output": [{"name": "is_valid", "value": True}]},
            {"input": [{"name": "ip", "value": "256.1.2.3"}], "output": [{"name": "is_valid", "value": False}]}
        ]
    )

    unit_tester.add(
        "Validate Email Address",
        validate_email,
        [
            {"input": [{"name": "email", "value": "test@example.com"}], "output": [{"name": "is_valid", "value": True}]},
            {"input": [{"name": "email", "value": "invalid.email@"}], "output": [{"name": "is_valid", "value": False}]}
        ]
    )

    unit_tester.run()
    unit_tester.summary()

def run_fuzz_tests():
    """Runs fuzz tests for the IoT functions."""
    fuzz_tester = VeritasFuzzer("IoT Fuzz Tests")

    # Fuzz Tests
    fuzz_tester.add(
        "Fuzz temperature conversion",
        convert_celsius_to_fahrenheit,
        [
            {
                "input": [
                    {"name": "celsius", "type": "float", "range": {"min": -100, "max": 100}}
                ],
                "output": [],
                "iterations": 100
            }
        ]
    )

    fuzz_tester.add(
        "Fuzz IP validation",
        validate_ip_address,
        [
            {
                "input": [
                    {"name": "ip", "type": "str", "regular_expression": r"\b(?:\d{1,3}\.){3}\d{1,3}\b"}
                ],
                "output": [],
                "iterations": 1000
            }
        ]
    )

    fuzz_tester.add(
        "Fuzz Email validation",
        validate_email,
        [
            {
                "input": [
                    {"name": "email", "type": "str", "regular_expression": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"}
                ],
                "output": [],
                "iterations": 1000
            }
        ]
    )

    fuzz_tester.run()
    fuzz_tester.summary()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run IoT functions or perform tests")
    parser.add_argument("--unit", action="store_true", help="Run unit and fuzz tests")
    parser.add_argument("--fuzz", action="store_true", help="Run unit and fuzz tests")    
    args = parser.parse_args()

    if args.unit:
        run_unit_tests()
    elif args.fuzz:
        run_fuzz_tests()
    else:
        original_script_logic()