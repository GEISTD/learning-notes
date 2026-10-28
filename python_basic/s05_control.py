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

# ============ 练习区 ============

def fizzbuzz(n):
    """返回 1..n 的 FizzBuzz 结果列表（字符串）。
    3 的倍数 -> "Fizz"，5 的倍数 -> "Buzz"，15 的倍数 -> "FizzBuzz"，其余转字符串。
    n=5 -> ["1", "2", "Fizz", "4", "Buzz"]
    注意：15 的判断必须写在 3 和 5 前面，否则永远走不到。
    """
    # TODO
    return []


def find_first(nums, target):
    """返回 target 首次出现的下标，找不到返回 -1。
    提示：用 enumerate，找到就 return，不要写完整的 for 循环再判断。
    """
    # TODO
    return -1


def zip_pairs(a, b):
    """把两个序列配成 [(a0,b0), (a1,b1), ...]，长度不齐时按短的截断。
    zip_pairs([1,2,3], "ab") -> [(1,"a"), (2,"b")]
    """
    # TODO
    return []


def collatz_steps(n):
    """考拉兹猜想：偶数除以 2，奇数乘 3 加 1，问多少步到 1。
    6 -> 6,3,10,5,16,8,4,2,1 共 8 步。
    提示：这里是典型的 while（步数未知），记得用整数除法 //。
    """
    # TODO
    return 0


def sum_until_negative(nums):
    """从头累加，遇到第一个负数就停下（不包含该负数）。
    [1, 2, -1, 5] -> 3
    提示：for + break。
    """
    # TODO
    return 0


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
