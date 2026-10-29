# 01 版本管理：从建仓到回滚

任务：项目代码量大、改动频繁，先把版本管理跑通，保证每次修改都能退回去。

环境：Windows + Git 2.x + Gitee 私有仓库。

## 建仓和首次推送

```bash
git config --global user.name "xxx"      # 只配一次
git config --global user.email "xxx@xx"

git init                                  # 当前目录变成仓库
git add .
git commit -m "初始化"
git remote add origin git@gitee.com:xxx/xxx.git
git push -u origin master
```

`origin` 是远程仓库的别名，`-u` 的作用是记住这个分支的上游，以后直接 `git push` 就行。

## 分支

主分支保持可运行，功能在子分支写：

```bash
git switch -c feature/login     # 新建并切过去
# 写代码
git add .
git commit -m "登录界面"
git push -u origin feature/login
git switch master
git merge feature/login
```

分支之间是隔离的，子分支的改动不合并，master 上看不到。

## 遇到的三个问题

**1. push 被拒绝**

两个人先后往同一个仓库提交，后一个 push 报：

```
! [rejected]  main -> main (fetch first)
```

不是权限问题，是远程比本地多了一个提交。先 `git pull` 合并再 push；想让历史保持一条直线就用 `git pull --rebase`。

**2. 以为改完就保存了**

没执行 `git commit` 之前，改动只在工作区，既传不上去，也回不到上一个版本。后来的习惯是"一个能跑通的功能点提交一次"，提交信息写清楚做了什么。

**3. 回滚方式用错**

| 目的 | 命令 |
|---|---|
| 只想看看旧版本 | `git checkout <commit>`，看完 `git switch master` 回来 |
| 本地没 push，想重来 | `git reset --mixed <commit>`（`--hard` 会连工作区一起清） |
| 已经 push，多人协作 | `git revert <commit>`，生成一条反向提交，不动历史 |

`reset --hard` 之后再强推，会把别人的提交冲掉，团队协作里不要这么干。

## 结论

- master 只放能运行的版本，功能在分支上做。
- 提交前 `git status` 看一眼，确认没把 build 目录和数据库文件带进去。
- 待补：`.gitignore` 里加上 `build-*/`、`*.o`、`*.db`。
