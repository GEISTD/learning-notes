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
    """LC 1. 两数之和：返回和为 target 的两个数的下标 [i, j]（i < j）。
    nums = [2,7,11,15], target = 9 -> [0, 1]
    提示：一遍哈希。遍历时用 dict 存「值 -> 下标」，查 target - x 是否已经出现过，
          这样是 O(n) 而不是双重循环 O(n^2)。
    """
    # TODO
    return []


def is_valid(s):
    """LC 20. 有效的括号：判断括号是否一一配对且顺序正确。
    "()[]{}" -> True；"(]" -> False；"([)]" -> False
    提示：栈 + 配对字典 {")": "(", "]": "[", "}": "{"}；遇左括号入栈，
          遇右括号时栈顶必须是对应的左括号。
    """
    # TODO
    return False


def merge_sorted(a, b):
    """LC 88 的简化版：合并两个有序列表，返回新的有序列表（不修改原列表）。
    [1,2,3] + [2,5,6] -> [1,2,2,3,5,6]
    提示：双指针，分别指向 a 和 b，每次取较小的那个；最后把剩下的整段接上。
          也可以直接用 sorted(a + b) —— 但那不算练双指针，先手写一遍。
    """
    # TODO
    return []


def max_subarray(nums):
    """LC 53. 最大子序和：返回和最大的连续子数组之和。
    [-2,1,-3,4,-1,2,1,-5,4] -> 6（子数组 [4,-1,2,1]）
    提示：Kadane 算法。cur = max(x, cur + x)，ans = max(ans, cur)。
          一句话理解：如果「之前累计的和」还不如「从当前重新开始」，就重新开始。
    """
    # TODO
    return 0


def move_zeros(nums):
    """LC 283. 移动零：把所有 0 移到末尾，非零元素保持相对顺序，返回新列表。
    [0,1,0,3,12] -> [1,3,12,0,0]
    提示：双指针（写指针）。遍历数组，遇到非零就写到 write 位置并 write += 1，
          最后把剩余位置补 0。
    """
    # TODO
    return []


def roman_to_int(s):
    """LC 13. 罗马数字转整数。
    "MCMXCIV" -> 1994；"III" -> 3；"LVIII" -> 58
    提示：规则是「小值在大值左边就减，否则加」。
          用一个 dict 存 7 个符号的值，遍历时和下一个字符比较。
    """
    # TODO
    return 0


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
