#!/usr/bin/env python

# LeetCode Problem: Two Sum
# URL: https://leetcode.com/problems/two-sum/

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
