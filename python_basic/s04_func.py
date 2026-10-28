# -*- coding: utf-8 -*-
"""S04 · 函数 / 参数 / 闭包

【Python 函数比 C++ 灵活得多，也更容易踩坑】

1. 函数是**一等对象**：能赋值、能当参数传、能返回。C++ 里要写 std::function。
2. 默认参数：`def f(a, b=2)`。注意默认值只在定义时求值一次，
   所以千万别写 `def f(x, acc=[])`（可变默认值坑，所有调用共用同一个列表）。
3. `*args` 收多余位置参数成 tuple，`**kwargs` 收多余关键字参数成 dict。
4. 闭包：内层函数能记住外层函数的变量。Python 2 的 `nonlocal` 就是为改外层变量而生。
5. lambda 只能写一个表达式，适合当 key= 或短回调，不要拿它写复杂逻辑。

【练习】改完运行：python s04_func.py
"""

# ============ 练习区 ============

def apply_all(funcs, x):
    """把 x 依次喂给每个函数，返回最终结果。
    apply_all([str.upper, lambda s: s + "!"], "hi") -> "HI!"
    """
    for func in funcs:
        x = func(x)
    return x


def make_counter():
    count = 0

    def counter():
        nonlocal count
        count += 1
        return count

    return counter
    def counter():
        return 0
    return counter


def sum_all(*args):
    """接收任意个位置参数求和；不传参数返回 0。
    sum_all(1, 2, 3) -> 6，sum_all() -> 0
    提示：直接用内置 sum(args)。
    """
    num = sum(args)
    return num


DEFAULTS = {"lr": 0.01, "epochs": 10}


def build_config(**kwargs):
    """把 kwargs 合并进 DEFAULTS 的副本并返回，不能修改全局 DEFAULTS。
    build_config(epochs=20) -> {"lr": 0.01, "epochs": 20}
    提示：先 dict(DEFAULTS)，再 .update(kwargs)。
    """
    dict(DEFAULTS)
    DEFAULTS.update(kwargs)
    return DEFAULTS


def compose(f, g):
    """返回一个新函数，等价于 f(g(x))。
    compose(str.upper, lambda s: s + "!"), 传入 "hi" -> "HI!"
    """
    def composed(x):
        return f(g(x))
    return composed


# ============ 自测区（不用改） ============

def _test_counter():
    c = make_counter()
    _eq(c(), 1)
    _eq(c(), 2)
    d = make_counter()
    _eq(d(), 1)  # 两个计数器互不影响


def _test_config_isolated():
    build_config(lr=0.1)
    _eq(DEFAULTS, {"lr": 0.01, "epochs": 10})


CHECKS = [
    ("apply_all",     lambda: _eq(apply_all([str.upper, lambda s: s + "!"], "hi"), "HI!")),
    ("make_counter",  _test_counter),
    ("sum_all",       lambda: (_eq(sum_all(1, 2, 3), 6), _eq(sum_all(), 0))),
    ("build_config",  lambda: (_eq(build_config(epochs=20), {"lr": 0.01, "epochs": 20}),
                               _test_config_isolated())),
    ("compose",       lambda: _eq(compose(str.upper, lambda s: s + "!")("hi"), "HI!")),
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
