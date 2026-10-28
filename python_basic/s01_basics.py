# -*- coding: utf-8 -*-
"""S01 · 变量 / 字符串 / f-string / 数字

【和 C++ 的核心差异，先记这 5 条】
1. 不用声明类型：`x = 1` 就够了，类型跟着值走；想看类型用 `type(x)`。
2. 不存在 `char`，单字符就是长度为 1 的字符串，用 `'a'` 或 `"a"` 都行。
3. 字符串**不可变**：`s[0] = 'X'` 会报错，要改只能重新拼一个新字符串。
4. 整数不会溢出（自动变长整数）；除法 `/` 结果永远是 float，整除要用 `//`。
5. 格式化统一用 f-string：`f"我叫{name}，今年{age}岁"`，比 C++ 的 printf 和 << 都省事。

【练习方式】
把每个函数里的 TODO 换成你的实现，然后运行本文件：
    python s01_basics.py
全部显示 [通过] 就过关。也可以用 `python check.py s01` 单独跑。
"""

# ============ 练习区（改这里） ============

def greet(name, age):
    """返回 "我叫{name}，今年{age}岁"。用 f-string。"""
    # TODO
    return f""


def celsius_to_f(c):
    """摄氏度转华氏度：F = C * 9/5 + 32，结果保留 1 位小数（用 round）。"""
    # TODO
    return 0


def first_last(full):
    """把 "李 小龙" 拆成 ("李", "小龙")。

    提示：str.split(maxsplit=1) 只切第一刀，剩下的整体保留，
          正好对应「姓 + 名」这种中文姓名。
    不足两段时，第二段返回空字符串。
    """
    # TODO
    return ("", "")


def is_even(n):
    """判断偶数，返回 bool。注意 Python 里 0 也是偶数。"""
    # TODO
    return False


def digit_sum(n):
    """求各位数字之和，例如 1234 -> 10，0 -> 0。

    提示：可以先 str(n) 再逐字符 int()，
          也可以用 while n > 0: total += n % 10; n //= 10
    """
    # TODO
    return 0


# ============ 自测区（下面的代码不用改） ============

CHECKS = [
    ("greet",            lambda: _eq(greet("小明", 20), "我叫小明，今年20岁")),
    ("celsius_to_f",     lambda: (_eq(celsius_to_f(100), 212.0),
                                  _eq(celsius_to_f(37), 98.6))),
    ("first_last",       lambda: (_eq(first_last("李 小龙"), ("李", "小龙")),
                                  _eq(first_last("张 三 丰"), ("张", "三 丰")),
                                  _eq(first_last("王"), ("王", "")))),
    ("is_even",          lambda: (_eq(is_even(4), True),
                                  _eq(is_even(7), False),
                                  _eq(is_even(0), True))),
    ("digit_sum",        lambda: (_eq(digit_sum(1234), 10),
                                  _eq(digit_sum(0), 0))),
]


def _eq(actual, expected):
    assert actual == expected, f"期望 {expected!r}，你返回了 {actual!r}"


def tests():
    """返回 [(练习名, 错误信息或 None)]，供 check.py 调用。"""
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
