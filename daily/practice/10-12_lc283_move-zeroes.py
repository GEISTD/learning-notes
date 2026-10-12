"""
LeetCode 283. 移动零  [Easy]  —  新题
链接: https://leetcode.cn/problems/move-zeroes/
日期: 2026-10-12 周一  |  目标用时: 20 分钟本地跑通
思路提示（卡住 10 分钟再看）: 快慢双指针：慢指针指向下一个非零应放的位置，快指针扫描；最后把慢指针之后全置 0
"""
from typing import List, Optional

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:  # 原地修改
        """TODO: 你的手写代码从这里开始 —— 先自己写，跑通后再让 AI review"""
        pass

# ---- 本地测试：看到 AC! 再 commit ----
def test():
    sol = Solution()
    nums = [0, 1, 0, 3, 12]
    sol.moveZeroes(nums)
    assert nums == [1, 3, 12, 0, 0], 'case 1'
    print("AC!")

if __name__ == "__main__":
    test()
