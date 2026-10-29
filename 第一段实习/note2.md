# 02 Qt 工程结构

任务：接手项目用的 Qt 5.8 + MinGW 32bit 工程，先搞清楚一个窗口程序由哪几部分组成，能自己从零建一个。

## .pro 文件

```
QT       += core gui
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets
TEMPLATE = app
```

- 用到数据库加 `QT += sql`，用到网络加 `QT += network`，少了这两行，头文件能包含但链接会失败。
- `TEMPLATE = app` 表示生成 exe。
- 这个文件一般不动，加模块时才改。

## 四个文件的职责

| 文件 | 作用 |
|---|---|
| `main.cpp` | 程序入口，创建 Widget 对象，`return a.exec()` 进入事件循环，窗口才会一直显示 |
| `widget.h` | 类声明，成员变量、槽函数的原型 |
| `widget.cpp` | 具体实现 |
| `widget.ui` | 界面文件，构建时生成 `ui_widget.h` |

头文件里只声明不实现，实现在 cpp，这是 C++ 的基本规矩。

## 对象树

Qt 用父子关系管理内存：父对象析构时，挂在它下面的子对象一并销毁。

- 栈上 `Widget w;`，函数结束就销毁；
- 堆上 `new Widget`，要自己 `delete`；
- 子控件和布局在创建时指定父对象（或者加进布局），父窗口关掉时自动释放。

所以 `new` 出来的按钮只要指定了 parent，就不用逐个 delete。

## 信号与槽

四要素：谁发信号、发什么信号、谁接收、接收后执行哪个函数。

```cpp
connect(btn1, &QPushButton::clicked, this, &Widget::close);
```

- 信号是控件提供的，比如 `clicked`、`returnPressed`；
- 槽就是普通成员函数，在头文件里写在 `slots:` 下面；
- **连接只写一次，放在构造函数里**。

## 布局和坐标

- `move(x, y)` 只改位置；
- `setGeometry(x, y, w, h)` 位置和大小一起改；
- 用了布局管理器之后，手动坐标会被布局覆盖。

## 结论

界面可以用 Designer 拖，但业务逻辑必须手写；`.pro` 管模块，头文件管声明，cpp 管实现，对象树管内存。
