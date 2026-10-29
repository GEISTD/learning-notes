# 03 定时器做图片轮播 + 文件读写

任务：主界面顶部加一个图片轮播（2 秒一张，11 张循环）；另外把"新建 / 打开 / 保存"三个菜单项接上文件读写。

## 轮播

拆成四部分：

| 部分 | 作用 |
|---|---|
| `currentIndex` | 当前第几张，1~11 |
| `QLabel` | 显示图片 |
| `QTimer` | 定时发出 timeout 信号 |
| `nextpix()` | 收到信号后换下一张 |

构造函数里初始化：

```cpp
ui->setupUi(this);
currentIndex = 1;
m_timer = new QTimer(this);
connect(m_timer, &QTimer::timeout, this, &Widget::nextpix);
ui->label->setPixmap(QPixmap(":/images/p1.png"));   // 先显示第一张
```

换图：

```cpp
void Widget::nextpix()
{
    currentIndex++;
    if (currentIndex > 11) currentIndex = 1;        // 到末尾回到第一张
    QPixmap pix(QString(":/images/p%1.png").arg(currentIndex));
    if (pix.isNull()) { qDebug() << "load failed" << currentIndex; return; }
    ui->label->setPixmap(pix.scaled(ui->label->size(), Qt::KeepAspectRatio));
}
```

开始和停止：

```cpp
void Widget::on_startBtn_clicked()
{
    if (!m_timer->isActive()) m_timer->start(2000);  // 已经在跑就不重复启动
}

void Widget::on_stopBtn_clicked()
{
    m_timer->stop();
}
```

## 三个错误

**1. 把 `nextpix()` 写进了析构函数的大括号里**

C++ 不允许函数嵌套，编译直接报错。析构函数和普通成员函数必须是平级的两段。

**2. 定时器写成了构造函数里的局部变量**

```cpp
QTimer timer;          // 错：构造函数结束就析构，图不动
QTimer *m_timer;       // 对：成员变量，start/stop 操作的是同一个对象
```

**3. connect 写在了槽函数里**

点一次 Start 连一次，信号发了 N 遍，切换速度越来越快。连接只能放在构造函数里，只连一次。

## 文件读写

菜单项的 `triggered` 信号接到槽，用 `QFile` + `QTextStream`：

```cpp
void Widget::on_saveAction_triggered()
{
    QString name = QFileDialog::getSaveFileName(this, "保存", "", "文本文件 (*.txt)");
    if (name.isEmpty()) return;
    QFile f(name);
    if (!f.open(QIODevice::WriteOnly | QIODevice::Text)) return;
    QTextStream out(&f);
    out << ui->textEdit->toPlainText();
}
```

打开时先 `QFileDialog::getOpenFileName` 取路径，再 `readAll()` 填回控件。

打开失败要判断返回值，不要假设一定成功；路径为空说明用户点了取消，直接返回。

## 图片资源

图片放在项目目录里，用 `.qrc` 资源文件加进去，代码里写 `:/images/p1.png`。用相对路径在当前目录下能跑，打包以后经常找不到。

## 结论

`start()` 只是打开定时器的开关，真正干活的是 timeout 触发的槽；`stop()` 关掉开关，槽就不再被调用。
