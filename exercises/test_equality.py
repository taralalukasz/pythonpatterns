from domain.model import Money, Name, Line
import unittest

class TestEq(unittest.TestCase):

    def test_equality(self):
        self.assertTrue(Money('gbp', 10) == Money('gbp', 10))
        self.assertTrue(Name('Harry', 'Percival') != Name('Bob', 'Gregory'))
        self.assertTrue(Line('RED-CHAIR', 5) == Line('RED-CHAIR', 5))
    