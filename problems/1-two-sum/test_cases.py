import unittest
from solution import Solution


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_example_1(self):
        self.assertEqual(self.solution.twoSum([2, 7, 11, 15], 9), [0, 1])


if __name__ == "__main__":
    unittest.main()
