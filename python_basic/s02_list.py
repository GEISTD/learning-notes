# -*- coding: utf-8 -*-
"""S02 · 列表 / 切片 / 列表推导式

【这一关是 Python 手感的命门，LeetCode 里 80% 的代码都在和列表打交道】

1. 切片 `lst[a:b:c]`：含头不含尾，`c` 是步长。`lst[::-1]` 就是反转，不用写循环。
   负数下标从尾部数：`lst[-1]` 是最后一个元素。
2. 列表推导式 `[f(x) for x in xs if cond]`：把「循环 + 判断 + append」压成一行，
   这是 Python 最标志性的写法，务必练熟。
3. 列表是**可变**的（这点和字符串相反），`append / pop / sort` 会直接改原列表；
   想要副本要显式写 `lst[:]` 或 `list(lst)`。
4. `sort()` 原地排序返回 None，`sorted()` 返回新列表 —— 这是新手最常踩的坑。

【练习】改完运行：python s02_list.py
"""

# ============ 练习区 ============

def second_largest(nums):
    """返回第二大的「不同」数值。例如 [3,1,4,4,2] -> 3。
    不同值不足 2 个时返回 None。

    提示：sorted(set(nums)) 会得到一个去重且升序的新列表。
    """
    # TODO
    return None


def remove_dups_keep_order(nums):
    """去重但保持首次出现的顺序。[1,2,1,3,2] -> [1,2,3]。

    提示：用 seen = set() 记录见过的值，再用推导式过滤；
          不能直接 set(nums)，那样顺序就乱了。
    """
    # TODO
    return []


def squares_of_odds(n):
    """返回 0 到 n-1 中所有奇数的平方，要求用【一行列表推导式】。
    n=6 时 0..5 里的奇数是 1,3,5 -> [1,9,25]
    """
    # TODO
    return []


def flatten(matrix):
    """把二维列表拍平。[[1,2],[3],[4,5]] -> [1,2,3,4,5]。

    提示：双层推导式 [x for row in matrix for x in row]
    """
    # TODO
    return []


def rotate(lst, k):
    """把列表整体右移 k 位，循环移动。[1,2,3,4,5] 右移 2 -> [4,5,1,2,3]。

    提示：先对 len(lst) 取模（k 可能大于长度），再切片拼接。
          一行就能写完：lst[-k:] + lst[:-k]
    """
    # TODO
    return []


# ============ 自测区（不用改） ============

CHECKS = [
    ("second_largest",        lambda: (_eq(second_largest([3, 1, 4, 4, 2]), 3),
                                       _eq(second_largest([5, 5]), None),
                                       _eq(second_largest([1]), None))),
    ("remove_dups_keep_order", lambda: _eq(remove_dups_keep_order([1, 2, 1, 3, 2]), [1, 2, 3])),
    ("squares_of_odds",        lambda: _eq(squares_of_odds(6), [1, 9, 25])),
    ("flatten",                lambda: _eq(flatten([[1, 2], [3], [4, 5]]), [1, 2, 3, 4, 5])),
    ("rotate",                 lambda: (_eq(rotate([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]),
                                        _eq(rotate([1, 2, 3], 5), [2, 3, 1]))),
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
