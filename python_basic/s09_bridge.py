# -*- coding: utf-8 -*-
"""S09 · 衔接 LeetCode 的 6 道基础题

【收到这里，说明你已经能独立写函数了。这 6 道就是 LeetCode「简单」的真实难度】

做法建议：
1. 先在纸上/注释里写清思路（一句话），再动手写代码。
2. 用本文件底部的测试验证，全过了再去 LeetCode 原题提交（题号写在每道题注释里）。
3. 想不出来时，先写暴力解法，跑通再想优化 —— 暴力也是答案。

完成这 6 道，就可以正式开始每日算法闯关了。

【练习】改完运行：python s09_bridge.py
"""


# ============ 练习区 ============

def two_sum(nums, target):
    """返回两数之和等于 target 的两个下标。"""
    seen = {}

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

def is_valid(s):
    """判断括号是否一一配对且顺序正确。"""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []

    for char in s:
        if char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack or stack.pop() != pairs[char]:
                return False

    return not stack

def merge_sorted(a, b):
    """合并两个有序列表，返回新的有序列表。"""
    result = []
    i = j = 0

    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1

    result.extend(a[i:])
    result.extend(b[j:])
    return result


def max_subarray(nums):
    """返回最大连续子数组的和。"""
    cur = ans = nums[0]

    for x in nums[1:]:
        cur = max(x, cur + x)
        ans = max(ans, cur)

    return ans

def move_zeros(nums):
    """把所有 0 移到末尾，返回新列表。"""
    result = []
    for num in nums:
        if num != 0:
            result.append(num)

    result.extend([0] * (len(nums) - len(result)))
    return result


def roman_to_int(s):
    """把罗马数字转换成整数。"""
    values = {
        "I": 1, "V": 5, "X": 10, "L": 50,
        "C": 100, "D": 500, "M": 1000,
    }

    total = 0
    for i, char in enumerate(s):
        value = values[char]
        if i + 1 < len(s) and value < values[s[i + 1]]:
            total -= value
        else:
            total += value

    return total


# ============ 自测区（不用改） ============

CHECKS = [
    ("two_sum",       lambda: (_eq(two_sum([2, 7, 11, 15], 9), [0, 1]),
                               _eq(two_sum([3, 3], 6), [0, 1]))),
    ("is_valid",      lambda: (_eq(is_valid("()[]{}"), True),
                               _eq(is_valid("(]"), False),
                               _eq(is_valid("([)]"), False),
                               _eq(is_valid(""), True))),
    ("merge_sorted",  lambda: _eq(merge_sorted([1, 2, 3], [2, 5, 6]), [1, 2, 2, 3, 5, 6])),
    ("max_subarray",  lambda: (_eq(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6),
                               _eq(max_subarray([-1]), -1))),
    ("move_zeros",    lambda: _eq(move_zeros([0, 1, 0, 3, 12]), [1, 3, 12, 0, 0])),
    ("roman_to_int",  lambda: (_eq(roman_to_int("MCMXCIV"), 1994),
                               _eq(roman_to_int("III"), 3),
                               _eq(roman_to_int("LVIII"), 58))),
]


def _eq(actual, expected):
    assert actual == expected, f"期望 {expected!r}，你返回了 {actual!r}"


def tests():
    out = []
    for name, fn in CHECKS:
        try:
            fn()
            out.append((name, None))
        except AssertionError as e:
            out.append((name, str(e)))
        except Exception as e:
            out.append((name, f"{type(e).__name__}: {e}"))
    return out


if __name__ == "__main__":
    for name, err in tests():
        print(("[通过] " if err is None else "[未过] ") + name + ("" if err is None else f"\n        {err}"))
