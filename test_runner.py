import unittest
import os

def run_tests():
    # Discover and run all the unit tests in the current directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.dirname(__file__), pattern="unit_tests.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("All tests passed!")
        exit(0)
    else:
        print("Some tests failed.")
        exit(1)

if __name__ == "__main__":
    run_tests()