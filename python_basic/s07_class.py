# -*- coding: utf-8 -*-
"""S07 · 类与对象（和 C++ 对照着看最快）

【C++ 程序员学 Python 类，只需要记住这几条差异】

1. `__init__` 相当于构造函数，第一个参数固定是 `self`（对应 C++ 的 this，但必须显式写）。
2. 所有成员函数第一个参数都是 self；`self.balance` 就是在访问成员变量。
3. 没有 public/private 关键字，约定：`_name` 表示「内部使用」。
4. `__repr__` 相当于给调试看的 toString；`__eq__` 相当于 operator==。
5. 运算符重载靠魔法方法：`__add__` 对应 +，`__len__` 对应 len()，`__lt__` 对应 <。
6. `@property` 让方法能像属性一样访问（`obj.area` 而不是 `obj.area()`）。

【练习】改完运行：python s07_class.py
"""

# ============ 练习区 ============

class BankAccount:
    """银行账户。

    __init__(self, owner, balance=0)
    deposit(amount)   -> 余额增加，返回新余额
    withdraw(amount)  -> 余额减少，返回新余额；余额不足时 raise ValueError("余额不足")
    """

    def __init__(self, owner, balance=0):
        # TODO: 保存 owner 和 balance 到 self
        pass

    def deposit(self, amount):
        # TODO
        return 0

    def withdraw(self, amount):
        # TODO
        return 0


class Vector2:
    """二维向量。

    __init__(self, x, y)
    __add__(self, other) -> 新的 Vector2，分量相加
    __repr__(self)       -> "Vector2(1, 2)" 这种形式
    __eq__(self, other)  -> 分量相同即相等
    """

    def __init__(self, x, y):
        # TODO
        pass

    def __add__(self, other):
        # TODO
        return None

    def __repr__(self):
        # TODO
        return ""


class Stack:
    """用 list 实现的栈（Python 里 list 的 append/pop 就是栈操作）。

    push(x)  -> 入栈
    pop()    -> 出栈并返回栈顶；空栈时 raise IndexError("栈为空")
    peek()   -> 只看栈顶不出栈；空栈返回 None
    is_empty() -> bool
    """

    def __init__(self):
        self._data = []

    def push(self, x):
        # TODO
        pass

    def pop(self):
        # TODO
        return None

    def peek(self):
        # TODO
        return None

    def is_empty(self):
        # TODO
        return True


class Student:
    """学生。__init__(self, name, age)；另需一个类方法：

        Student.from_string("张三,20", sep=",") -> Student("张三", 20)
    提示：类方法用 @classmethod，第一个参数是 cls 而不是 self。
    """

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, s, sep=","):
        # TODO
        return None


# ============ 自测区（不用改） ============

def _test_account():
    a = BankAccount("小明", 100)
    _eq(a.deposit(50), 150)
    _eq(a.withdraw(30), 120)
    try:
        a.withdraw(1000)
    except ValueError:
        pass
    else:
        raise AssertionError("余额不足时应该 raise ValueError")


def _test_vector():
    _eq(repr(Vector2(1, 2)), "Vector2(1, 2)")
    _eq(Vector2(1, 2) + Vector2(3, 4), Vector2(4, 6))
    assert Vector2(1, 2) == Vector2(1, 2), "相同分量应判等"


def _test_stack():
    s = Stack()
    assert s.is_empty()
    s.push(1); s.push(2)
    _eq(s.peek(), 2)
    _eq(s.pop(), 2)
    _eq(s.pop(), 1)
    assert s.is_empty()
    try:
        s.pop()
    except IndexError:
        pass
    else:
        raise AssertionError("空栈 pop 应该 raise IndexError")


def _test_student():
    st = Student.from_string("张三,20")
    _eq((st.name, st.age), ("张三", 20))


CHECKS = [
    ("BankAccount", _test_account),
    ("Vector2",     _test_vector),
    ("Stack",       _test_stack),
    ("Student",     _test_student),
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
