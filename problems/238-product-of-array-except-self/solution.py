#!/usr/bin/env python

# LeetCode Problem: Product of Array Except Self
# URL: https://leetcode.com/problems/product-of-array-except-self/

from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        result = [1] * len(nums)
        suffix = 1
        prefix = 1
        for i in range(len(nums)):
            result[i] = prefix
            prefix *= nums[i]
        for i in range(len(nums)):
            end = len(nums) - i - 1
            result[end] *= suffix
            suffix *= nums[end]
        return result
