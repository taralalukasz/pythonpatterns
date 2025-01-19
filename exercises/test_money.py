import unittest
from domain.model import Money


m5 = Money("gbp", 5)
m10  = Money("gbp", 10)

class MoneyTest(unittest.TestCase):

    def test_add_same_currency_success(self):
        self.assertEqual(m5 + m5, m10)
    
    def test_multiply_by_number_success(self):
        self.assertEqual(m5 * 5, Money("gbp", 25))

    def test_multiply_by_currency_success(self):
        self.assertEqual(m5 * m5, Money("gbp", 25))

    def test_subtract_same_currency_success(self):
        self.assertEqual(m10 - m5, m5)

    def test_add_different_currency_fail(self):
        usd5=Money("usd", 5)
        with self.assertRaises(ValueError):
            usd5 + m5

    def test_multiply_different_currency_fail(self):
        usd5=Money("usd", 5)
        with self.assertRaises(ValueError):
            usd5 + m5
