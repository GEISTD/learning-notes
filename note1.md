1.gitee GitHub
2.我们项目的代码非常多 保存很费事
3.是否可以随时回档 随时可以找回来
4.凡事留痕
后续代码笔记保存并上传
5.git命令 git为版本控制软件==》SVN 
SVN介绍
程序员入职后找项目经理要网址 程序员就可以用命令clone URL克隆到自己的电脑
前提：必须在公司，必须在同一个网络上。
git 解决了在断网的情况下一也可以上传和下载
安装了git软件以后 使用了git命令电脑就变成了本地仓库
再通过push发送到远程仓库还是项目经理的电脑
（1）安装git软件
（2）创建gitee账户 就有gitlab
（3）使用git命令把代码保存到gitee上
新建code txt
和notepad txt
git init 本地仓库初始化
git add *添加当前目录下所有的文件到暂存区
git commit -m添加描述，一次为一个版本
git config user.name and user.email一次就够了
git remote add origin URL建立本地与远程的联系（origin可以为别名 URL为地址）
git push -u origin “master” 把本地仓库的代码推送到远程仓库去
本地仓库的版本为1.0
两个程序员入职后gitclone 再开发上传之后会有两个2.0版本，会报错不能上传成功
此时要先gitpull
只要git commit之后版本+1，但是只要没有commit就相当于没有保存，此时既不是2.0版本又不能返回去1.0版本
分支
master是主分支 可以创建子分支
在子分支不会影响主分支
这样避免了在主分支写代码
在 Git 中，分支操作是核心功能。针对你刚解决完推送问题的现状，以下是创建和切换分支最清晰、最实用的操作方法：

一、查看当前分支

在操作前，先确认自己在哪里。执行以下命令：
git branch

•   结果：你会看到一个列表，带星号（\*）且高亮的就是你当前所处的分支（比如你现在应该在 master 上）。

二、创建新分支

假设你想创建一个名为 dev 的分支用于开发新功能。

方法 1：仅创建，不切换（传统方式）
git branch dev

执行后，系统会创建一个名为 dev 的新分支，但你的光标依然停留在当前的 master 分支上。

方法 2：创建并立即切换（推荐）
这是最常用的方式，一条命令搞定两件事：
git checkout -b dev

或者使用 Git 后来新增的、语义更清晰的命令：
git switch -c dev

•   -c 是 create 的缩写。

•   执行后，命令行提示符前面的括号里会变成 (dev)，表示你已经进入了新分支。

三、切换分支

如果你想从 dev 分支切回 master，或者切换到其他已有的分支：

方法 1：使用 checkout（经典通用）
git checkout master


方法 2：使用 switch（推荐，不易混淆）
git switch master


四、完整的实操演示

假设你现在在 master 分支，想要新建一个功能分支并工作：
# 1. 确保当前在 master 分支，并且代码是最新的
git status
# 如果不是，先切回去：git switch master

# 2. 基于当前最新的 master，创建并切换到新分支 feature-login
git switch -c feature-login

# 3. 在新分支上修改代码（比如修改了 login.js）
# ... 写代码 ...

# 4. 提交代码到这个新分支
git add .
git commit -m "添加了用户登录功能"

# 5. 将这个新分支推送到远程仓库（Gitee）
# 因为是远程第一次见到这个分支，所以需要加 -u 参数建立关联
git push -u origin feature-login

•   注意：-u 参数的作用和刚才成功提示里的 set up to track 是一个意思。加了它之后，下次在这个分支推送，只需要敲 git push 即可。

五、常用辅助命令

命令 作用

git branch 查看本地所有分支

git branch -r 查看远程所有分支

git branch -a 查看本地+远程所有分支

git branch -d dev 删除名为 dev 的本地分支（已合并才可删）

git branch -D dev 强制删除名为 dev 的本地分支（未合并也删）

💡 核心概念提醒（非常重要）

•   分支是独立的：你在 dev 分支写的代码，如果不进行合并操作，master 分支是看不见的。这保证了主分支的稳定性。

•   切换前请保持干净：切换分支前，最好保证当前分支的工作区是干净的（即没有未提交的修改），否则有时会导致切换失败或代码混乱。

"返回以前版本"在 Git 里有好几种玩法，选哪个取决于你是想"看看旧代码"，还是"真要把历史倒回去"，以及有没有已经 push 到 Gitee。

先建立一个共同动作——找版本号：
git log --oneline


会看到类似：

a1b2c3d 完善计算器，加了个 bug
e4f5g6h 计算器v2，支持加减乘除
i7j8k9l 计算器v1，只能加

每条前面的 a1b2c3d 就是提交 ID（不用全抄，前 6-7 位够用）。记住你想回到的那个 ID，下面都用它。

场景一：我就想"看看"旧版本长啥样，不改历史

git checkout e4f5g6h


这时候 Git 会提示你 HEAD is now at e4f5g6h...，你切到了一个"分离 HEAD"状态，文件夹里的代码就是当时那个版本。

想回去？直接切回主分支就行：
git switch master   # 或 git checkout master


💡 这种姿势最安全，不改变任何历史，看完就溜。

场景二：本地改炸了，想撤到旧版本（还没 push 过）

用 git reset，它有三档，差别很大，看清楚再敲：

命令 分支指针 暂存区 工作区（你看到的文件） 用啥场景

--soft 移到旧提交 不变 不变 想重改提交信息 / 合并几次 commit

--mixed（默认） 移到旧提交 清空 不变 想重新 git add 选文件

--hard 移到旧提交 清空 清空 彻底不要了，回到旧版本样子

举例，想回到"计算器v1"那个提交：
# 只挪指针，代码还留着（暂存区）
git reset --soft i7j8k9l

# 挪指针+清暂存，代码还在工作区
git reset --mixed i7j8k9l
# 等价于 git reset i7j8k9l

# 彻底回到那个版本，后面的提交全扔（危险！）
git reset --hard i7j8k9l


⚠️ --hard 会真·销毁后面的提交和工作区改动，敲之前确认 git status 里没你要留的东西。

场景三：已经 push 到 Gitee 了，想撤掉某次提交

别用 reset + force push，你前面刚把仓库修好，强行盖容易把远程搞乱。正确姿势是 git revert——它会新建一个提交来"反向抵消"旧提交，历史还在，安全。
# 撤销某一次提交（比如撤销 a1b2c3d 那次"加了 bug"的提交）
git revert a1b2c3d


Git 会弹编辑器让你写 revert 的提交信息，保存退出后：
git push


远程就多了一条"反向提交"，等于那次改动被取消了，但历史链条没断，队友也不会炸。

怎么选，一句话对号入座

• 只看不碰 → git checkout 提交ID，看完 git switch master 回来

• 本地 solo、没 push、想重来 → git reset --mixed 提交ID（保守）或 --hard（狠）

• 已经 push 到 Gitee / 多人协作 → git revert 提交ID，别动 reset

一个你大概率马上会用的组合

前面你说"两个文件夹分别 commit 再 push 报 rejected"——如果其中一个文件夹的提交你想整个扔掉重来（还没 push 成功的话）：
git reset --hard origin/master   # 把本地分支硬拽回和远程一样
# 然后重新 add / commit / push


这样就不用 pull --rebase 也能清掉本地那次"孤儿提交"。



