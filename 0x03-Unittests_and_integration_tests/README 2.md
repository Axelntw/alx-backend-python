# Unit Testing and Integration Testing Project

This project contains unit tests and integration tests for Python utilities and client classes.

## Files Structure

- `test_utils.py`: Unit tests for utility functions including:
  - `access_nested_map`: Tests for nested dictionary access functionality
  - Other utility function tests (to be added)

## Test Cases

### TestAccessNestedMap
Tests the `access_nested_map` function with various input cases:
- Simple one-level dictionary access
- Nested dictionary access with single path
- Nested dictionary access with multiple path elements

## Running Tests

To run the tests:

```bash
python3 -m unittest test_utils.py
```

## Requirements

- Python 3.7+
- unittest
- parameterized
