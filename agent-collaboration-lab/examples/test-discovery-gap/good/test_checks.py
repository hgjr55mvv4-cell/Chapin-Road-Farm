"""Equivalent checks implemented as discoverable standard-library unit tests."""
import unittest

def validate_age(value):
    return type(value) is int and 0 <= value <= 130

def reserve_before_action(predicted_cost, hard_cap):
    return predicted_cost <= hard_cap

class ContractTests(unittest.TestCase):
    def test_age_bool_guard(self):
        self.assertTrue(validate_age(25))
        self.assertFalse(validate_age(True))

    def test_budget_precheck(self):
        self.assertTrue(reserve_before_action(150, 150))
        self.assertFalse(reserve_before_action(216, 150))

if __name__ == '__main__':
    unittest.main()
