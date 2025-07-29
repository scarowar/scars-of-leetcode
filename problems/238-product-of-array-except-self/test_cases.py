import unittest
from solution import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_example_1(self):
        self.assertEqual(self.solution.productExceptSelf([1, 2, 3, 4]), [24, 12, 8, 6])

    def test_with_zero(self):
        self.assertEqual(self.solution.productExceptSelf([0, 1, 2, 3]), [6, 0, 0, 0])

    def test_all_zeros(self):
        self.assertEqual(self.solution.productExceptSelf([0, 0]), [0, 0])

    def test_single_element(self):
        self.assertEqual(self.solution.productExceptSelf([5]), [1])

    def test_two_elements(self):
        self.assertEqual(self.solution.productExceptSelf([1, 0]), [0, 1])

    def test_larger_numbers(self):
        self.assertEqual(
            self.solution.productExceptSelf([2, 3, 4, 5]), [60, 40, 30, 24]
        )


if __name__ == "__main__":
    unittest.main()
