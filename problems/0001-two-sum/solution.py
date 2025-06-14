from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        val_to_index = {}

        for i, num in enumerate(nums):
            diff = target - num
            if diff in val_to_index:
                return [val_to_index[diff], i]
            else:
                val_to_index[num] = i


if __name__ == "__main__":
    s = Solution()
    print(s.twoSum([2, 7, 11, 15], 9))  # Expected: [0, 1]
    print(s.twoSum([3, 3], 6))  # Expected: [0, 1]
