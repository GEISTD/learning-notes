# -*- coding: utf-8 -*-
"""S08 · 标准库 / 异常处理

【Python 真正的手感来自标准库，下面 5 个是刷题和写脚本的高频工具】

1. `collections.Counter`：一行完成计数，`.most_common(k)` 直接给 top-k。
2. `collections.defaultdict`：访问不存在的键时自动创建默认值，省掉 if 判断。
3. `collections.deque`：双端队列，`popleft()` 是 O(1) —— BFS 的标准队列。
   （list.pop(0) 是 O(n)，别用它当队列）
4. `itertools.combinations / permutations / chain`：组合、排列、拼接。
5. 异常：`try / except / else / finally`。
   **EAFP 精神**：与其事先检查，不如直接做、出错再兜住。
   但 except 要写具体异常类型，不要裸 `except:`（会吞掉 KeyboardInterrupt）。

【练习】改完运行：python s08_stdlib.py
"""

from collections import Counter, defaultdict, deque
from datetime import datetime
from itertools import combinations

# ============ 练习区 ============

def top_words_counter(text, k):
    """用 Counter 返回 top-k 的 (单词, 次数) 列表。
    "a b a c a", k=2 -> [("a", 3), ("b", 1)]
    提示：Counter(text.split()).most_common(k) 已经是你要的顺序。
    """
    # TODO
    return []


def group_by_first_letter(words):
    """用 defaultdict(list) 按首字母分组。["apple","banana","avocado"]
    -> {"a": ["apple","avocado"], "b": ["banana"]}
    """
    # TODO
    return {}


def pair_sum(nums, target):
    """用 itertools.combinations 找第一对和等于 target 的下标组合，返回 tuple；没有返回 None。
    pair_sum([1, 2, 3, 4], 5) -> (0, 3)
    提示：遍历 combinations(range(len(nums)), 2)，找到就 return。
    """
    # TODO
    return None


def safe_int(s, default=-1):
    """把字符串转 int，失败时返回 default（不要抛异常出去）。
    safe_int("42") -> 42；safe_int("abc") -> -1
    提示：try / except ValueError。
    """
    # TODO
    return 0


def days_between(d1, d2):
    """计算两个 "YYYY-MM-DD" 日期相差的天数（绝对值）。
    ("2024-01-01", "2024-03-01") -> 60（2024 是闰年，2 月有 29 天）
    提示：datetime.strptime(s, "%Y-%m-%d") 解析，相减得 timedelta，取 .days。
    """
    # TODO
    return 0


def bfs_order(graph, start):
    """用 deque 做 BFS，返回访问顺序（同一层按边给出顺序）。
    graph = {"A": ["B","C"], "B": ["D"], "C": [], "D": []}
    bfs_order(graph, "A") -> ["A", "B", "C", "D"]
    提示：出队 -> 记录 -> 把未访问邻居入队；一定要用集合记录已访问，防止成环死循环。
    """
    # TODO
    return []


# ============ 自测区（不用改） ============

def _test_defaultdict_type():
    d = group_by_first_letter(["apple"])
    assert isinstance(d, dict), f"应返回 dict，你返回了 {type(d).__name__}"


CHECKS = [
    ("top_words_counter",    lambda: _eq(top_words_counter("a b a c a", 2), [("a", 3), ("b", 1)])),
    ("group_by_first_letter", lambda: (_eq(group_by_first_letter(["apple", "banana", "avocado"]),
                                           {"a": ["apple", "avocado"], "b": ["banana"]}),
                                       _test_defaultdict_type())),
    ("pair_sum",             lambda: (_eq(pair_sum([1, 2, 3, 4], 5), (0, 3)),
                                      _eq(pair_sum([1, 2], 100), None))),
    ("safe_int",             lambda: (_eq(safe_int("42"), 42), _eq(safe_int("abc"), -1))),
    ("days_between",         lambda: _eq(days_between("2024-01-01", "2024-03-01"), 60)),
    ("bfs_order",            lambda: _eq(bfs_order({"A": ["B", "C"], "B": ["D"], "C": [], "D": []}, "A"),
                                          ["A", "B", "C", "D"])),
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
