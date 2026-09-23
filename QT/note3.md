1.定时任务

（1）引入图片用Qpixmap引包

（2）要图片地址（一般用相对路径，即放在项目目录里），把图片用resource file添加到资源目录下。resource.rqc，再copy相对路径到需要的地方用ui->label->setPixmap(pix)来引用。

（3）一、 核心原理（脑海里要有这张图）

整个程序由 4个核心部分 组成：
1.  数据（Data）：currentIndex，用来记录当前是第几张图（1~11）。
2.  视图（View）：QLabel（名叫 picture），负责把图片展示出来。
3.  控制器（Controller）：QTimer，它是心脏，负责每隔一段时间跳一下（发出 timeout 信号）。
4.  业务逻辑（Logic）：nextpix()，它告诉程序“跳一下”的时候该干什么（换下一张图）。

运行流程：
定时器跳动 -> 触发 nextpix() -> currentIndex + 1 -> 拼出新路径 -> 加载图片 -> 显示到 Label -> 等待下一次跳动。

二、 项目结构 & 职责分工

1. widget.h（头文件：搭架子）

这里主要做声明，告诉编译器这个类有什么东西。
•   成员变量：

    ◦   Ui::Widget *ui：指向界面的指针。
    
    ◦   int currentIndex：非常重要，这是轮播的状态（现在播到第几张了）。
    
    ◦   QTimer *m_timer：非常重要，不能定义在构造函数里，必须定义为成员变量，否则 start 和 stop 槽函数没法操作同一个定时器。

•   槽函数（Slots）：

    ◦   nextpix()：处理切换图片的逻辑。
    
    ◦   on_startBtn_clicked()：处理开始按钮点击事件。
    
    ◦   on_stopBtn_clicked()：处理停止按钮点击事件。

2. widget.cpp（源文件：填肉）

这里写具体的实现逻辑。

A. 构造函数 Widget::Widget

这里是初始化的地方，只做一次。
1.  ui->setupUi(this)：加载 UI 界面。
2.  currentIndex = 1：初始化状态，从第 1 张开始。
3.  m_timer = new QTimer(this)：创建定时器，并指定父对象（防止内存泄漏）。
4.  连接信号与槽：connect(m_timer, &QTimer::timeout, this, &Widget::nextpix);
    ◦   意思是：把定时器的“心跳”信号，连接到“换图”的函数上。

5.  加载第一张图：在定时器启动前，先把第一张图显示出来，不然一开始是空白的。
6.  初始化按钮状态：比如一开始“Stop”按钮是灰色的（不可点击）。

B. 换图逻辑 Widget::nextpix

这是轮播的核心算法。
1.  currentIndex++：索引加 1。
2.  边界检测：if (currentIndex > 11) currentIndex = 1; 播完第 11 张，回到第 1 张，形成闭环。
3.  路径拼接：QString(".../p%1.png").arg(currentIndex)，生成正确的文件名。
4.  加载与显示：
    ◦   使用 QPixmap 加载图片。

    ◦   检查是否加载成功（isNull()）：这是调试神器，路径错了立马知道。

    ◦   scaled()：让图片适应 Label 大小，不变形。

    ◦   setPixmap()：把图片贴到 Label 上。

C. Start 按钮 Widget::on_startBtn_clicked

1.  防呆设计：if (!m_timer->isActive())，如果已经在跑了，就不再重复启动。
2.  m_timer->start(2000)：关键点。启动定时器，设定每 2000 毫秒（2秒）发射一次 timeout 信号。
3.  更新UI状态：Start 按钮变灰，Stop 按钮变亮（表示现在可以停止）。

D. Stop 按钮 Widget::on_stopBtn_clicked

1.  m_timer->stop()：关键点。停止定时器。定时器停止后，就不再发射 timeout 信号，图片也就不动了。
2.  更新UI状态：Stop 按钮变灰，Start 按钮变亮（表示现在可以开始）。

三、 最容易犯的 3 个错误（对照检查）

1.  函数嵌套错误（你之前遇到的）：
    ◦   错误：把 void Widget::nextpix() { ... } 写在了 ~Widget() { ... } 的大括号里面。

    ◦   正确：C++ 不允许函数套函数，它们必须是平行的。

2.  定时器生命周期错误：
    ◦   错误：在构造函数里写 QTimer timer;。

    ◦   后果：timer 是局部变量，构造函数执行完就被销毁了，根本起不到定时作用。

    ◦   正确：必须定义为类的成员变量 (QTimer *m_timer;)。

3.  信号槽连接错误：
    ◦   错误：在 on_startBtn_clicked 里写 connect。

    ◦   后果：每点一次 Start，就连一次，导致图片切换速度越来越快（因为信号发了 N 次）。

    ◦   正确：连接操作放在构造函数里，只连一次。

四、 最终总结一句话

start() 只是打开了定时器的开关，真正干活的是 timeout 信号触发的 nextpix()；stop() 关掉了开关，干活的动作就暂停了。

这套逻辑现在非常标准了。接下来如果你想升级，可以尝试：
1.  添加“上一张”“下一张”按钮（其实就是手动调用 nextpix() 或写一个 prevpix()）。
2.  鼠标移上去暂停（监听 enterEvent 和 leaveEvent）。
3.  用 QSS 美化按钮样式。

2.文件读写

下面给你一个**最小可运行的 MainWindow 示例**，只用**菜单栏 Action + triggered 信号 + QDebug**，实现**新建 / 打开 / 保存**三个功能，并且我会**逐行解释逻辑**，适合初学者理解 Qt 的事件与 UI 机制。

------

## 一、最终效果（逻辑概览）

- 

  菜单栏：`文件`

  - 

    `新建`：清空文本框

  - 

    `打开`：选择文件并读取内容

  - 

    `保存`：把文本框内容写回文件

- 

  使用 `QAction::triggered`

- 

  使用 `qDebug()`打印运行过程

- 

  不做异常处理，只讲流程

------

## 二、UI 操作（非常重要）

1. 

   打开 **Qt Designer**

2. 

   在 `MainWindow`的 **菜单栏** 输入：`文件(&F)`

3. 

   在下拉菜单里依次添加：

   - 

     `新建(&N)`

   - 

     `打开(&O)`

   - 

     `保存(&S)`

4. 

   分别选中这三个 Action，把它们的 `objectName`改为：

   - 

     `actionNew`

   - 

     `actionOpen`

   - 

     `actionSave`

5. 

   拖一个 **QTextEdit** 到窗口中央，命名为 `textEdit`

------

## 三、mainwindow.h（头文件）

```
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    // 三个 Action 的槽函数
    void on_actionNew_triggered();
    void on_actionOpen_triggered();
    void on_actionSave_triggered();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
```

### ✅ 关键点解释

| 内容                       | 含义                                   |
| -------------------------- | -------------------------------------- |
| `slots:`                   | Qt 的槽函数区，用来接收信号            |
| `on_actionNew_triggered()` | **自动连接规则**：`on_对象名_信号名()` |
| `Ui::MainWindow *ui`       | 指向 UI 里所有控件的指针               |

------

## 四、mainwindow.cpp（核心逻辑）

```
#include "mainwindow.h"
#include "ui_mainwindow.h"

#include <QFile>
#include <QFileDialog>
#include <QTextStream>
#include <QDebug>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    qDebug() << "MainWindow 初始化完成";
}

MainWindow::~MainWindow()
{
    delete ui;
}
```

------

### 1️⃣ 新建（清空文本）

```
void MainWindow::on_actionNew_triggered()
{
    qDebug() << "触发：新建文件";
    ui->textEdit->clear();   // 清空文本框
}
```

#### 🔍 逻辑解释

- 

  用户点击「新建」

- 

  Qt 发射 `triggered()`信号

- 

  自动调用 `on_actionNew_triggered()`

- 

  `clear()`清空 QTextEdit

------

### 2️⃣ 打开（读取文件）

```
void MainWindow::on_actionOpen_triggered()
{
    qDebug() << "触发：打开文件";

    QString fileName =
        QFileDialog::getOpenFileName(this, "打开文件", ".", "文本文件 (*.txt)");

    qDebug() << "选择的文件：" << fileName;

    QFile file(fileName);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
        return;

    QTextStream in(&file);
    ui->textEdit->setText(in.readAll());

    file.close();
    qDebug() << "文件读取完成";
}
```

#### 🔍 逻辑解释

| 代码                             | 作用                 |
| -------------------------------- | -------------------- |
| `QFileDialog::getOpenFileName()` | 弹出“打开文件”对话框 |
| `QFile`                          | Qt 的文件类          |
| `open(QIODevice::ReadOnly)`      | 以只读方式打开       |
| `QTextStream`                    | 文本流，方便读字符串 |
| `readAll()`                      | 一次性读取全部内容   |
| `setText()`                      | 显示到 QTextEdit     |

------

### 3️⃣ 保存（写入文件）

```
void MainWindow::on_actionSave_triggered()
{
    qDebug() << "触发：保存文件";

    QString fileName =
        QFileDialog::getSaveFileName(this, "保存文件", ".", "文本文件 (*.txt)");

    qDebug() << "保存路径：" << fileName;

    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        return;

    QTextStream out(&file);
    out << ui->textEdit->toPlainText();

    file.close();
    qDebug() << "文件保存完成";
}
```

#### 🔍 逻辑解释

| 代码                | 作用                  |
| ------------------- | --------------------- |
| `getSaveFileName()` | 弹出“另存为”对话框    |
| `WriteOnly`         | 写入模式              |
| `toPlainText()`     | 获取 QTextEdit 纯文本 |
| `<<`                | 写入文本流            |

------

## 五、为什么不用手写 connect？

你问到了 **action trigger**，这里用的是 Qt 的**自动连接机制**：

```
on_actionNew_triggered()
```

等价于：

```
connect(ui->actionNew, &QAction::triggered,
        this, &MainWindow::on_actionNew_triggered);
```

只要你：

- 

  函数名是 `on_控件名_信号名()`

- 

  控件在 UI 里

- 

  `setupUi()`已调用

✅ Qt 会自动帮你 connect

------

## 六、qDebug 的作用（你现在阶段很重要）

```
qDebug() << "触发：新建文件";
```

作用：

- 

  看程序“走到哪一步”

- 

  验证信号是否被触发

- 

  看变量值（比如文件名）

------

输入输出流：字符流（输入输出），字节流（输入输出）。

这三个类是 Qt 处理文件/IO 操作的「黄金三角」，分工非常明确，刚好对应你刚才写「打开/保存」时的完整流程，我结合你已经写过的代码给你拆明白：

一、先给总览（一句话记死）

类名 本质 负责的事 对应你代码里的角色

QFileDialog 图形化文件选择器 和用户交互，拿到文件的路径 「打开/保存」时弹出来的那个选文件的窗口

QFile 本地文件操作类 绑定硬盘上的真实文件，干「读/写」的活 拿着路径去开文件、关文件

QIODevice 所有IO设备的抽象基类 规定「所有能读写的设备都必须遵守的标准接口」 QFile的爹，定义了open()/read()/write()这些通用方法

二、逐个拆解（全是你刚用过的东西）

1. QFileDialog：「我只负责找路，不碰文件内容」

它是和用户交互的工具类，作用是弹出系统原生的文件选择窗口，帮你拿到用户选中的文件路径，完全不关心文件里装的是什么。

你代码里用的两个静态方法：

// 打开文件时：选已有文件，返回路径
QString fileName = QFileDialog::getOpenFileName(
    this,          // 父窗口
    "打开文件",     // 窗口标题
    ".",           // 默认打开的目录（.代表程序当前目录）
    "文本文件 (*.txt)"  // 过滤规则，只显示txt文件
);

// 保存文件时：选保存位置+文件名，返回路径
QString fileName = QFileDialog::getSaveFileName(
    this, 
    "保存文件", 
    ".", 
    "文本文件 (*.txt)"
);

✅ 特点：
• 不用new对象，直接调用静态方法，适合简单场景

• 返回值是QString类型的绝对路径（比如C:/test/a.txt），不是文件内容！

• 如果用户点了「取消」，返回空字符串

❌ 新手常踩的坑：以为QFileDialog打开了文件，其实它只是拿到了地址，真正的文件操作是QFile干的。

2. QFile：「我是真·文件搬运工」

它是专门操作本地硬盘文件的类，继承自QIODevice，负责和操作系统打交道，真正执行「打开文件、读内容、写内容、关闭文件」的操作。

你代码里的用法：

QFile file(fileName);  // 用刚才拿到的路径，绑定要操作的文件
if (!file.open(QIODevice::ReadOnly | QIODevice::Text))  // 申请打开文件
    return;

QTextStream in(&file);  // 借助文本流读内容
ui->textEdit->setText(in.readAll());

file.close();  // 用完关文件，释放系统资源

✅ 核心作用：
• 把「文件路径」和「真实文件」绑定起来

• 通过open()向操作系统申请文件操作权限（读/写/追加等）

• 通过read()/write()直接和文件交换数据

✅ 你用到的open()参数的意思：
参数 作用

QIODevice::ReadOnly 只读模式，不能写

QIODevice::WriteOnly 只写模式，文件不存在就创建，存在就清空原有内容

QIODevice::Text
 文本模式：自动处理不同系统的换行符（Windows的\r\n和Linux的\n互相转换），只有读写文本文件时才加，读写图片/二进制文件绝对不能加！（你之前轮播图读png的时候就不能加这个，不然图片会坏）

3. QIODevice：「我是所有IO设备的通用标准」

它是一个抽象基类（不能直接new对象），作用是给所有「能读写的设备」定一套统一的规则：不管你操作的是本地文件、内存数据、网络数据、串口数据，只要能读写，就必须支持我规定的这些方法。

它规定了所有IO设备都必须有的核心方法：

方法 作用

open(OpenMode) 打开设备，申请操作权限

close() 关闭设备，释放资源

readAll() 读取所有数据

write(data) 写入数据

isOpen() 判断设备是否已经打开

isReadable() 判断是否可读

为什么要设计这个？

因为Qt里不止能操作本地文件，以后你会遇到：
• 读内存里的数据：QBuffer（也是QIODevice子类）

• 读网络数据：QTcpSocket/QNetworkReply（也是QIODevice子类）

• 读串口数据：QSerialPort（也是QIODevice子类）

所有IO类的用法和QFile一模一样：都是open()→read()→close()，你学会了QFile，以后学网络、串口根本不用重新记API，这就是面向对象的抽象好处。

你代码里的QFile之所以能调用open()/close()，就是因为从QIODevice继承来的。

三、串一遍你刚才「打开文件」的完整流程（对应到你写的每一行代码）

1. 你点菜单栏「打开」→ 触发actionOpen的triggered信号
2. QFileDialog弹出窗口 → 你选了一个a.txt → 返回路径"C:/a.txt"
3. 用这个路径创建QFile对象：QFile file("C:/a.txt") → 绑定这个文件
4. file.open(ReadOnly | Text) → QFile向操作系统申请读这个文件的权限，成功返回true
5. QTextStream借助QFile（本质是QIODevice）的readAll()方法，把文件里的字节读出来，转成QString
6. 把QString塞给textEdit显示
7. file.close() → 告诉操作系统我不用这个文件了，释放资源

四、易错点提醒（你以后一定会遇到）

1. ❌ 不要给二进制文件（图片、视频、exe）加QIODevice::Text模式，会把二进制数据里的换行符篡改，文件直接损坏（你之前的轮播图读png时open()不能加Text）
2. ❌ QFileDialog返回的路径可能是空的（用户点了取消），一定要判断再操作QFile
3. ❌ open()一定要判断返回值！很多「文件打不开」的bug都是因为没判断，比如文件被占用、路径不存在，直接往下走就会崩溃

五、扩展：不用QTextStream能不能读文件？

完全可以，QTextStream只是个辅助类，帮你处理文本编码、换行符的，你也可以直接用QIODevice的原生方法：
QFile file(fileName);
if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
    QByteArray data = file.readAll();  // 直接读原始字节
    QString text = QString::fromUtf8(data);  // 自己转成字符串
    ui->textEdit->setText(text);
    file.close();
}

3.网络编程







4.sq1



