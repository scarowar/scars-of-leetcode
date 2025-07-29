#!/usr/bin/env python

# LeetCode Problem: Container With Most Water
# URL: https://leetcode.com/problems/container-with-most-water/

from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        max_area = 0
        while left < right:
            current_area = (right - left) * min(height[left], height[right])
            max_area = max(max_area, current_area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return max_area


s = Solution()

print(s.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]))
# Expected: 49

print(s.maxArea([1, 1]))
# Expected: 1

print(s.maxArea([4, 3, 2, 1, 4]))
# Expected: 16

print(s.maxArea([1, 2, 1]))
# Expected: 2

print(s.maxArea([2, 3, 10, 5, 7, 8, 9]))
