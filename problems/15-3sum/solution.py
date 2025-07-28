#!/usr/bin/env python

# LeetCode Problem: 3Sum
# URL: https://leetcode.com/problems/3sum/

from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        results = []
        for a in range(len(nums)):
            if a > 0 and nums[a] == nums[a - 1]:
                continue
            left = a + 1
            right = len(nums) - 1
            while left < right:
                total = nums[left] + nums[right] + nums[a]
                if total == 0:
                    results.append([nums[a], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left = left + 1
                    while left < right and nums[right] == nums[right + 1]:
                        right = right - 1
                elif total > 0:
                    right -= 1
                else:
                    left += 1
        return results


print(Solution().threeSum([-1, 0, 1, 2, -1, -4]))
# Expected: [[-1, -1, 2], [-1, 0, 1]]

print(Solution().threeSum([0, 0, 0, 0]))
# Expected: [[0, 0, 0]]

print(Solution().threeSum([-2, 0, 1, 1, 2]))
# Expected: [[-2, 0, 2], [-2, 1, 1]]
