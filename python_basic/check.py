# -*- coding: utf-8 -*-
"""一键检测所有练习。

用法（在 python_basic 目录下）：
    python check.py          # 跑全部阶段
    python check.py s02      # 只跑 s02 阶段
    python check.py s07      # 只跑类与对象

输出 PASS 绿色即过关，FAIL 会告诉你期望值和实际值差在哪。
"""
import importlib
import os
import sys

STAGES = [
    "s01_basics",    # 变量 / 字符串 / f-string / 数字
    "s02_list",      # 列表 / 切片 / 推导式
    "s03_dict_set",  # 字典 / 集合 / 计数
    "s04_func",      # 函数 / 参数 / 闭包
    "s05_control",   # 循环 / enumerate / zip / while
    "s06_str_file",  # 字符串处理 / 文件读写
    "s07_class",     # 类与对象（对比 C++）
    "s08_stdlib",    # 标准库 / 异常处理
    "s09_bridge",    # 衔接 LeetCode 的 6 道基础题
]

STAGE_INFO = {
    "s01_basics": "变量 / 字符串 / f-string / 数字",
    "s02_list": "列表 / 切片 / 推导式",
    "s03_dict_set": "字典 / 集合 / 计数",
    "s04_func": "函数 / 参数 / 闭包",
    "s05_control": "循环 / enumerate / zip / while",
    "s06_str_file": "字符串处理 / 文件读写",
    "s07_class": "类与对象（对比 C++）",
    "s08_stdlib": "标准库 / 异常处理",
    "s09_bridge": "衔接 LeetCode 的 6 道基础题",
}


def stage_status():
    """返回每关的真实完成情况，供每日计划读取进度。

    每项: {"name", "title", "passed", "total", "pending", "error"}
    pending 是尚未通过的练习名，方便每天早上直接告诉你「今天该攻哪几个函数」。
    """
    base = os.path.dirname(os.path.abspath(__file__))
    if base not in sys.path:
        sys.path.insert(0, base)

    out = []
    for name in STAGES:
        try:
            mod = importlib.import_module(name)
            results = mod.tests()
        except Exception:
            out.append({"name": name, "title": STAGE_INFO[name], "passed": 0,
                        "total": 0, "pending": [], "error": True})
            continue
        passed = sum(1 for _, err in results if err is None)
        pending = [t for t, err in results if err is not None]
        out.append({"name": name, "title": STAGE_INFO[name], "passed": passed,
                    "total": len(results), "pending": pending, "error": False})
    return out


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    base = os.path.dirname(os.path.abspath(__file__))
    if base not in sys.path:
        sys.path.insert(0, base)

    total = 0
    passed = 0
    for name in STAGES:
        if only and only not in name:
            continue
        try:
            mod = importlib.import_module(name)
            results = mod.tests()
        except Exception as e:
            print(f"\n=== {name} === 加载失败: {type(e).__name__}: {e}")
            continue

        print(f"\n=== {name} ===")
        for title, err in results:
            total += 1
            if err is None:
                passed += 1
                print(f"  [通过] {title}")
            else:
                print(f"  [未过] {title}")
                for line in str(err).splitlines():
                    print(f"         {line}")

    if total:
        print(f"\n总计: {passed}/{total} 通过"
              + ("  —— 全过关，去下一关吧" if passed == total else "  —— 继续修，别急着看答案"))


if __name__ == "__main__":
    main()
