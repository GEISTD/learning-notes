# 第一段实习

项目：学生信息管理系统（Qt 5.8 + SQLite，Windows 桌面端）

代码在 `my-learning/qt/homework/studentscontroler`：登录、注册、学生信息、成绩管理，数据库访问按 user / student / score 分成三个 DAO，上面一层 businesslayer，界面是 widget + ui。

记录方式：按任务编号写，保留当时的报错和处理过程，不做事后美化。

| 文件 | 内容 |
|---|---|
| note1.md | 版本管理：Git 建仓、分支、回滚 |
| note2.md | Qt 工程结构：.pro、对象树、信号与槽 |
| note3.md | 定时器做图片轮播、文件读写 |
| note4.md | TCP 客户端与服务器 |

## 我做过的模块

- 登录 / 注册界面，账号密码校验走 userdao
- 学生信息增删改查，列表用 QTableWidget，数据经 studentdao 落库
- 成绩录入与查询，scoredao
- 主界面图片轮播（QTimer + QPixmap）
- 文本文件的新建 / 打开 / 保存
- TCP 通信 demo（QTcpServer / QTcpSocket）

## 遗留

- `build-*`、`*.o`、`students.db` 还没加进 `.gitignore`，提交时容易带上编译产物
- 网络部分只做到收发字符串，消息边界没处理，长消息会粘包
