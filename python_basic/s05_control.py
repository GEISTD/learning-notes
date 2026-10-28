# -*- coding: utf-8 -*-
"""S05 · 循环 / enumerate / zip / while

【Python 的 for 不是 C 的那种 for，它是「遍历可迭代对象」，这是最大的思维转变】

1. **不要写出 C 风格的下标循环**：
        for i in range(len(lst)):          # 不推荐
            print(i, lst[i])
        for i, x in enumerate(lst):        # 推荐，干净且不会越界
            print(i, x)
2. `zip(a, b)` 把两个序列配对，长度取短的。同时遍历两个列表就用它。
3. `range(start, stop, step)` 含头不含尾，`range(5)` 是 0..4。
4. `while` 用于「不知道要循环几次」的场景；`break` 跳出，`continue` 跳过本次。
5. 循环里 `else` 子句：没有 break 才会执行 —— 初学者先别用，读懂别人代码即可。

【练习】改完运行：python s05_control.py
"""
from itertools import zip_longest
from unittest import result


# ============ 练习区 ============
def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))

    return result

def find_first(nums, target):
    """返回 target 首次出现的下标，找不到返回 -1。
    提示：用 enumerate，找到就 return，不要写完整的 for 循环再判断。
    """
    if nums is None or len(nums) == 0:
        return -1
    enumerated = enumerate(nums)
    return enumerated



def zip_pairs(a, b):
    """把两个序列配对，长度不齐时按较短的截断。"""
    result = []
    for x, y in zip(a, b):
        result.append((x, y))
    return result


def collatz_steps(n):
    """考拉兹猜想：偶数除以 2，奇数乘 3 加 1，问多少步到 1。
    6 -> 6,3,10,5,16,8,4,2,1 共 8 步。
    提示：这里是典型的 while（步数未知），记得用整数除法 //。
    """
    count = 0
    while n!=1 :
        if n % 2 == 0 :
            n = n // 2
            count += 1
        else :
            n = 3 * n + 1
            count += 1

    return count


def sum_until_negative(nums):
    """从头累加，遇到第一个负数就停下（不包含该负数）。
    [1, 2, -1, 5] -> 3
    提示：for + break。
    """
    sum = 0
    for num in nums:
        if num < 0:
            break
        else :
            sum += num
    return sum


# ============ 自测区（不用改） ============

CHECKS = [
    ("fizzbuzz",          lambda: (_eq(fizzbuzz(5), ["1", "2", "Fizz", "4", "Buzz"]),
                                   _eq(fizzbuzz(15)[14], "FizzBuzz"))),
    ("find_first",        lambda: (_eq(find_first([5, 3, 8], 8), 2),
                                   _eq(find_first([1, 2], 9), -1))),
    ("zip_pairs",         lambda: _eq(zip_pairs([1, 2, 3], "ab"), [(1, "a"), (2, "b")])),
    ("collatz_steps",     lambda: (_eq(collatz_steps(6), 8), _eq(collatz_steps(1), 0))),
    ("sum_until_negative", lambda: _eq(sum_until_negative([1, 2, -1, 5]), 3)),
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
