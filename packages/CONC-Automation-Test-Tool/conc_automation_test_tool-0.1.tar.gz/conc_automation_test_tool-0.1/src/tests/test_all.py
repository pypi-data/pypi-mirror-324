import unittest

# Import test modules
from apps.app1.tests.test_app1 import TestApp1
from apps.app2.tests.test_app2 import TestApp2

# Create a test suite combining all test cases
def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(TestApp1))
    test_suite.addTest(unittest.makeSuite(TestApp2))
    return test_suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())