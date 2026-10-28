# -*- coding: utf-8 -*-
"""S06 · 字符串处理 / 文件读写

【字符串处理的常用三件套】

1. `s.split()` 不传参数会自动按「任意空白」切并且忽略首尾空白；
   `s.split(",")` 按指定分隔符切；`",".join(lst)` 是切的反操作，比 += 拼接快得多。
2. `s.strip() / lstrip() / rstrip()` 去首尾空白；`s.replace(old, new)` 全部替换。
3. 判断类：`s.isdigit() / isalpha() / startswith() / endswith()`，别自己写正则。
4. 字符串不可变，但 `"".join(...)` 拼装是 O(n)，`+=` 在循环里是 O(n^2)，注意区别。

【文件读写，永远用 with】
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()          # 一次读全部
    with open(path, "w", encoding="utf-8") as f:
        f.write("...")           # 覆盖写；追加用 "a"
`with` 会在块结束时自动关闭文件，等价于 C++ 的 RAII。

【练习】改完运行：python s06_str_file.py
"""

import os
import tempfile

# ============ 练习区 ============

def normalize_ws(s):
    """压缩空白：首尾空白去掉，中间连续空白变成一个空格。
    "  a   b \\n c " -> "a b c"
    提示：split() 不带参数时已经帮你做了「按任意空白切且丢掉空串」，
          再用 " ".join(...) 拼回去即可。
    """
    # TODO
    return ""


def is_palindrome(s):
    """判断回文，只考虑字母数字，忽略大小写和标点。
    "A man, a plan, a canal: Panama" -> True
    "abc" -> False
    提示：先 [c.lower() for c in s if c.isalnum()]，再和反转比较。
    """
    # TODO
    return False


def write_upper(path, lines):
    """把 lines 每一行转成大写写入 path（UTF-8，每行一个 \\n）。"""
    # TODO
    pass


def count_nonempty_lines(path):
    """统计文件中非空行的数量（去掉首尾空白后仍非空的才算）。"""
    # TODO
    return 0


def csv_parse(line):
    """把 "a, 1, 2.5" 解析成 ["a", 1, 2.5]：
    每段先 strip，能转 int 就转 int，否则能转 float 就转 float，都不行保持字符串。
    提示：用 try/except 依次尝试，或者自己判断 "." in token。
    """
    # TODO
    return []


# ============ 自测区（不用改） ============

def _test_file_roundtrip():
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "t.txt")
        write_upper(p, ["hello", "world"])
        with open(p, "r", encoding="utf-8") as f:
            content = f.read()
        _eq(content, "HELLO\nWORLD\n")

        q = os.path.join(d, "u.txt")
        with open(q, "w", encoding="utf-8") as f:
            f.write("a\n\n  \nb\n")
        _eq(count_nonempty_lines(q), 2)


CHECKS = [
    ("normalize_ws",        lambda: _eq(normalize_ws("  a   b \n c "), "a b c")),
    ("is_palindrome",       lambda: (_eq(is_palindrome("A man, a plan, a canal: Panama"), True),
                                     _eq(is_palindrome("abc"), False))),
    ("write_upper",         _test_file_roundtrip),
    ("csv_parse",           lambda: _eq(csv_parse("a, 1, 2.5"), ["a", 1, 2.5])),
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
