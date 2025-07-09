# This is the test file for our application.
# It uses pytest to test the functionality in main.py.

from main import add

def test_add():
    """This test will fail because of the bug in the add function."""
    assert add(2, 3) == 5
