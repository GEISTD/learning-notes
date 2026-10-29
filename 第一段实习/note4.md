# 04 网络编程：TCP 客户端与服务器

任务：做一个最小可用的 TCP 通信 demo，为后面两台机器联调做准备。

## 基础

- **IP**：定位主机，`ipconfig` 看本机地址；分公网和局域网。
- **端口**：定位进程，同一台机器上不同程序占不同端口。
- **协议**：双方约定的规则。TCP 面向连接、可靠、按序到达。
- **回环地址** `127.0.0.1`：先在本机把逻辑跑通，再去联两台机器。

通信的前提是网络可达，先 `ping` 通。同一个局域网里如果开了隔离或防火墙拦截，也 ping 不通，可以先用手机热点验证是不是网络环境的问题。

架构分 B/S 和 C/S，这个项目用的是 C/S：一端 `listen` 等连接，一端 `connectToHost` 发起。

## Qt 里的写法

`.pro` 里先加：

```
QT += network
```

服务器端：

```cpp
m_server = new QTcpServer(this);
m_server->listen(QHostAddress::Any, 8888);
connect(m_server, &QTcpServer::newConnection, this, &Widget::onNewConnection);

void Widget::onNewConnection()
{
    QTcpSocket *s = m_server->nextPendingConnection();
    connect(s, &QTcpSocket::readyRead, this, &Widget::onReadyRead);
}
```

客户端：

```cpp
m_socket = new QTcpSocket(this);
m_socket->connectToHost("127.0.0.1", 8888);
connect(m_socket, &QTcpSocket::readyRead, this, &Widget::onReadyRead);
```

收到数据的槽：

```cpp
void Widget::onReadyRead()
{
    QByteArray data = m_socket->readAll();
    ui->textEdit->append(QString::fromUtf8(data));
}
```

## 一个理解上的偏差

一开始以为 `write()` 就是把数据送到对方，所以客户端发完就等服务器回显。

实际流程是：`write()` 把数据拷进**本地发送缓冲区**，然后由 Qt 的事件循环交给操作系统的 TCP 协议栈发出去；对方网卡收到后放进**对方的接收缓冲区**，Qt 检测到有新数据才发 `readyRead`，这时 `readAll()` 才能读到。

所以客户端发完消息要自己先 append 到消息框，不然自己看不到自己发的内容——这是本地显示，不是服务器回显。

## 遇到的问题

- 只写了 `#include <QTcpSocket>`，没在 `.pro` 里加 `QT += network`，编译过、链接失败。
- 端口被别的程序占用，`listen()` 返回 false。要检查返回值，不能默认监听成功。
- 两台机器 ping 不通，先排查防火墙和网络隔离，不是代码问题。

## 结论

TCP 只提供一条可靠的字节流，**消息边界要自己定**。现在只做了收发字符串，长消息或连续发送会粘在一起，下一步在每条消息前加长度字段。
