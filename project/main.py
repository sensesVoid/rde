# This is the main application file.
# It contains a function with a deliberate bug.

def add(a, b):
    """This function is supposed to add two numbers, but it subtracts them instead."""
    return a - b # <-- The bug is here
