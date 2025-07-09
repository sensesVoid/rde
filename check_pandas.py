try:
    import pandas
    print("Pandas is installed and importable in this environment.")
except ImportError:
    print("Error: Pandas is NOT installed or NOT importable in this environment.")
    print("Please ensure you have installed pandas using: pip install pandas")