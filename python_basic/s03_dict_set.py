# -*- coding: utf-8 -*-
"""S03 · 字典 / 集合 / 计数

【C++ 里你写 std::map / std::set，Python 里对应 dict / set，但好用太多】

1. dict 的下标访问 `d[k]` 键不存在会抛 KeyError；安全访问用 `d.get(k, 默认值)`。
2. 遍历时同时拿键和值：`for k, v in d.items()`，比 C++ 的迭代器舒服。
3. set 会自动去重，并且 `& | -` 直接做交、并、差，不用写循环。
4. 计数别手写 if/else，`collections.Counter` 一行搞定（S08 会专门练）。
5. 排序时 `sorted(d.items(), key=lambda kv: (-kv[1], kv[0]))`
   表示「先按次数降序，次数相同按字母升序」——这个 key 函数模式必须掌握。

【练习】改完运行：python s03_dict_set.py
"""

# ============ 练习区 ============

def word_count(text):
    """统计每个单词出现次数，返回 dict。按空格切词。
    "a b a c" -> {"a": 2, "b": 1, "c": 1}
    """
    dic = {}
    for word in text.split():
        dic[word] = dic.get(word, 0) + 1
    return dic


def top_k_words(text, k):
    """返回出现次数最多的 k 个 (单词, 次数)，次数降序、同次数按字母升序。
    "the cat the dog the", k=2 -> [("the", 3), ("cat", 1)]

    提示：先 word_count，再 sorted(..., key=lambda kv: (-kv[1], kv[0]))[:k]
    """
    word_counts = {}
    for word in text.split():
        word_counts[word] = word_counts.get(word, 0) + 1
        sorted_word_count = sorted(word_counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return sorted_word_count [:k]


def invert(d):
    """键值互换。{"a": 1, "b": 2} -> {1: "a", 2: "b"}（假设值不重复）。"""
    result = {}
    for k,v in d.items():
        result[v] = k
    return result


def common_keys(d1, d2):
    """返回两个字典共同拥有的键，类型必须是 set。
    提示：dict 的 keys() 支持集合运算：d1.keys() & d2.keys()
    """
    result = set()
    for k in d1.keys():
        if k  in d2.keys():
            result.add(k)
    return result


def group_by_len(words):
    """按单词长度分组。"""
    groups = {}
    for w in words:
        length = len(w)
        groups.setdefault(length, []).append(w)
    return groups


# ============ 自测区（不用改） ============

CHECKS = [
    ("word_count",   lambda: _eq(word_count("a b a c"), {"a": 2, "b": 1, "c": 1})),
    ("top_k_words",  lambda: _eq(top_k_words("the cat the dog the", 2), [("the", 3), ("cat", 1)])),
    ("invert",       lambda: _eq(invert({"a": 1, "b": 2}), {1: "a", 2: "b"})),
    ("common_keys",  lambda: (_eq(common_keys({"a": 1, "b": 2}, {"b": 3, "c": 4}), {"b"}),
                              _type(common_keys({"a": 1}, {"a": 2}), set))),
    ("group_by_len", lambda: _eq(group_by_len(["a", "bb", "cc", "d"]),
                                 {1: ["a", "d"], 2: ["bb", "cc"]})),
]


def _eq(actual, expected):
    assert actual == expected, f"期望 {expected!r}，你返回了 {actual!r}"


def _type(value, expected):
    assert isinstance(value, expected), f"期望类型 {expected.__name__}，你返回了 {type(value).__name__}"


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
