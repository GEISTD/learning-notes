用qt creator开发

QT  +=core gui 引用库

配置文件一般不修改，引入网络的库（sq1数据库）要修改配置文件（.pro文件）

.exe应用程序 TEMPLATE = app

greaterThan适用于兼容QT大于4则加上widgets。

.h头文件定义类里的函数和变量没有具体的实现。

widget.cpp源文件是具体实现，main.cpp是程序入口创建了一个widget对象，一个window窗体对象。

return a.exec();让项目一直运行。

widget窗体对象最外层

layout布局对象

控件对象（文字控件，图片对象，输入框对象，按钮对象）

widget w随着作用域（函数）的消亡而消亡。

widget *w = new widget；要用delete。

假设对象都是new出来的，只delete了窗体对象其他对象依旧存在，在创建布局对象的时候会告诉他你爹是窗体对象，而机制是父亲死亡儿子一起死，所以在delete了窗体对象之后所有都消亡

因为窗体对象是最老的对象。（对象树机制）

可以通过查文档知道QT的具体操作，比如重命名，改大小，新增控件。

设置空间的宽和高和布局move（）；设置坐标。setGeometry（）；设置坐标和宽高。

1.信号发送者 哪个控件发出的信号。

2.信号   点击按钮信号  回车键的信号   鼠标移动到上面的信号

需要点击函数的地址   QPushButton地址（对象）里面的+

具体的信号地址。

3.信号的接收者。

4.槽函数：具体要完成的动作，也是用地址调用。

connect（btn1，&QPushButton：：clicked，this，&widget：：close）；

如果是很漂亮的界面是炫耀自定义控件的，可以直接用ui。

在ui文件里实现，所有的对象都在ui中，可以用ui-> btn2之类的实现。

在自定义了ui后会自动生成代码，但需要自己补全具体的实现。

 







 

