import unittest
from IntegerMatrix import IntegerMatrix


class IntegerMatrixTestCase(unittest.TestCase):
    """Tests for `IntegerMatrix.py`."""

    def test_bidon(self):
        p = 9
        """is the initial peek value, for an empty stack, None?"""
        self.assertEquals(p, 9)
##        
##    def test_pushing_states(self):
##        p = GenericStack()
##        p.push(1)
##        p.push(2)
##        p.push(3)
##        p.peek()
##        """Are numbers pushed correctly onto the stack?"""
##        self.assertEqual(p.peek(), 3)
##
##    def test_pop_empty_stack(self):
##        p = GenericStack()
##        found_some_value = p.peek() is not None
##        """initial pop returns None"""
##        self.assertFalse(found_some_value)

main.test()
