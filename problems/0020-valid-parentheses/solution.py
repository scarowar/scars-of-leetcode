from collections import deque


class Solution:
    def isValid(self, s: str) -> bool:
        result = deque()

        for c in s:
            if c in "({[":
                result.append(c)
            else:
                if result:
                    left = result.pop()
                    if left != self.getLeft(c):
                        return False
                else:
                    return False

        return not result

    def getLeft(self, c):
        if c == ")":
            return "("
        elif c == "}":
            return "{"
        return "["


if __name__ == "__main__":
    s = Solution()
    print(s.isValid("()"))  # Expected: True
    print(s.isValid("()[]{}"))  # Expected: True
    print(s.isValid("(]"))  # Expected: False
    print(s.isValid("([])"))  # Expected: True
    print(s.isValid("(()"))  # Expected: False
    print(s.isValid("("))  # Expected: False
    print(s.isValid("]"))  # Expected: False
