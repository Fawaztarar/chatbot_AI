# test_search.py
# test_search.py
import pytest
from lib.search import simple_search  # Replace 'your_module' with the actual name of the module where simple_search is defined

# Test for simple_search function
def test_simple_search():
    # Mock data for testing
    mock_data = {
        "doc1.txt": "Python is an interpreted, high-level and general-purpose programming language.",
        "doc2.txt": "Python's design philosophy emphasizes code readability with its notable use of significant whitespace."
    }

    # Test case 1: Query that exists in the mock data
    query = "Python"
    expected_snippet = "Python is an interpreted, high-level"  # Update this based on the expected output of your function
    result = simple_search(query, mock_data)
    assert result == expected_snippet, f"Expected '{expected_snippet}', but got '{result}'"

    # Test case 2: Query that does not exist in the mock data
    query = "Java"
    expected_response = "No relevant information found."
    result = simple_search(query, mock_data)
    assert result == expected_response, f"Expected '{expected_response}', but got '{result}'"

# This allows the test to be run via the command line
if __name__ == "__main__":
    pytest.main()









