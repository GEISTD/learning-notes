# WSL + FinalShell SSH 远程连接踩坑记录与成长笔记

> 记录时间：2026-09-18  
> 环境：Windows 11 + WSL2 Ubuntu 22.04 + FinalShell  
> 用途：个人成长记录，面试技术沉淀

---

## 一、背景与目标

在 Windows 11 环境下，通过 WSL2 搭建 Ubuntu 22.04 Linux 子系统，并使用 FinalShell 作为 SSH 客户端进行远程连接，实现 Windows 本地开发 + Linux 环境运行的工作流。

**核心目标：**
1. WSL2 中安装并配置 Ubuntu
2. 在 Ubuntu 中启用 SSH 服务
3. 使用 FinalShell 远程连接 WSL 中的 Linux
4. 解决 WSL2 IP 地址动态变化导致连接失效的问题

---

## 二、完整实施流程

### 2.1 WSL2 安装 Ubuntu

```powershell
# PowerShell（管理员）中执行
wsl --install
```

安装完成后重启电脑，首次启动 Ubuntu 设置用户名和密码。

**已安装的 WSL 发行版：**
- Ubuntu (WSL2)
- Ubuntu-22.04 (WSL2)
- docker-desktop (WSL2)

### 2.2 安装并启动 SSH 服务

```bash
# 在 WSL Ubuntu 中执行
sudo apt update
sudo apt install openssh-server -y
sudo service ssh start
```

### 2.3 查看 WSL IP 地址

```bash
hostname -I
# 或
ip addr show eth0 | grep 'inet '
```

### 2.4 FinalShell 连接配置

| 字段 | 值 |
|------|-----|
| 主机 | WSL 的 IP 地址 |
| 端口 | 22（默认）或自定义 |
| 用户名 | Linux 用户名 |
| 密码 | Linux 密码 |

---

## 三、踩坑记录（核心部分）

### 坑 1：SSH 端口不是默认的 22

**现象：**  
按照网上教程配置 FinalShell 连接端口 22，结果连接超时。

**排查过程：**
```bash
# 检查 SSH 配置文件
cat /etc/ssh/sshd_config | grep -E '^(Port|PasswordAuthentication|PermitRootLogin)'
```

**发现：**  
SSH 服务监听的是 **2222** 端口，不是默认的 22。

**原因：**  
WSL2 的 Ubuntu 22.04 默认配置中，SSH 端口被设为 2222（可能是为了避免与 Windows 端口冲突）。

**解决方案：**  
FinalShell 连接端口改为 `2222`。

**收获：**  
> 排查网络连接问题时，第一步永远是确认服务实际监听的端口。不要想当然地认为默认值就是实际值。用 `cat /etc/ssh/sshd_config | grep Port` 或 `ss -tlnp | grep ssh` 确认。

---

### 坑 2：WSL2 IP 地址每次重启都会变化

**现象：**  
第一次配好 FinalShell 能连上，重启电脑后就连不上了，因为 WSL 的 IP 变了。

**排查过程：**
```bash
# 每次重启后 IP 都不同
ip addr show eth0 | grep 'inet '
# 第一次：172.22.174.41
# 重启后可能变成：172.x.x.x（不同网段）
```

**原因：**  
WSL2 使用 NAT 网络模式，每次启动时 DHCP 会分配新的 IP 地址，这是 WSL2 的设计机制，不是 bug。

**尝试的方案 A：设置固定 IP（失败）**

在 WSL 中添加固定 IP：
```bash
# 创建脚本
sudo bash -c 'cat > /usr/local/bin/set-static-ip.sh << EOF
#!/bin/bash
ip addr add 192.168.50.10/24 dev eth0 2>/dev/null || true
EOF'
sudo chmod +x /usr/local/bin/set-static-ip.sh

# 创建 systemd 服务自启
sudo bash -c 'cat > /etc/systemd/system/wsl-static-ip.service << EOF
[Unit]
Description=Set Static IP for WSL
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/set-static-ip.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
EOF'
sudo systemctl daemon-reload
sudo systemctl enable wsl-static-ip.service
sudo systemctl start wsl-static-ip.service
```

**结果：**  
- WSL 内部 `192.168.50.10` 生效，ping 通
- 但从 Windows 端 `Test-NetConnection 192.168.50.10 -Port 2222` **连接失败**
- 原因：WSL2 的 NAT 网络不会把 Windows 请求转发到 WSL 内部手动添加的 IP 上

**尝试的方案 B：使用 localhost 127.0.0.1（成功！✅）**

```powershell
# 从 Windows 端测试
Test-NetConnection -ComputerName 127.0.0.1 -Port 2222
# 结果：TcpTestSucceeded = True
```

**原因：**  
WSL2 内置了 **localhost 自动转发机制**。Windows 访问 `127.0.0.1:2222` 时，WSL2 会自动将请求转发到 WSL 内部的 SSH 服务。这个机制不依赖 WSL 的具体 IP 地址，所以不管 IP 怎么变，`127.0.0.1` 永远能连上。

**最终解决方案：**  
FinalShell 主机填 `127.0.0.1`，端口 `2222`，永不需要修改。

**收获：**  
> 1. WSL2 的网络是 NAT 模式，IP 动态分配是设计如此，不要和它对着干
> 2. Windows → WSL 的通信，localhost 转发是最可靠的方案
> 3. 排查网络问题时要分层测试：ping（网络层）→ Test-NetConnection（传输层）→ SSH 连接（应用层）

---

### 坑 3：WSL 重启后 SSH 服务未自动启动

**现象：**  
重启电脑后，FinalShell 连接被拒绝。

**排查过程：**
```bash
# 检查 SSH 服务状态
sudo service ssh status
# 或
sudo systemctl status ssh
```

**发现：**  
SSH 服务没有随 WSL 启动而自动运行。

**原因：**  
WSL2 默认不启用 systemd，需要手动配置。

**解决方案：**

1. 确认 `/etc/wsl.conf` 中已启用 systemd：
```ini
[boot]
systemd=true

[user]
default=geist
```

2. 确认 SSH 服务设为开机自启：
```bash
sudo systemctl enable ssh
sudo systemctl status ssh
# 确认 enabled + active (running)
```

**收获：**  
> WSL2 的 systemd 支持是后来才加的功能，默认不一定开启。检查 `/etc/wsl.conf` 中 `systemd=true` 是确保服务自启的前提。修改后需要 `wsl --shutdown` 再重新启动才生效。

---

### 坑 4：SSH 密码连接需要交互输入，脚本无法自动化

**现象：**  
尝试用 `ssh geist@127.0.0.1` 测试连接时，命令行卡住等待输入密码，无法在脚本中自动化。

**尝试的方案：**

方案 A：安装 sshpass
```bash
sudo apt install sshpass
sshpass -p '密码' ssh -p 2222 geist@127.0.0.1 'command'
```

方案 B：SSH 密钥认证（更安全）
```bash
# 生成密钥对
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ''

# 将公钥添加到 authorized_keys
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys

# 免密连接
ssh -p 2222 -i ~/.ssh/id_rsa geist@127.0.0.1
```

**收获：**  
> 密码认证适合人工操作，密钥认证适合自动化脚本。生产环境推荐密钥认证 + 禁用密码登录。

---

## 四、最终配置汇总

### FinalShell 连接信息（永久有效）

| 字段 | 值 |
|------|-----|
| 主机 | `127.0.0.1` |
| 端口 | `2222` |
| 用户名 | `geist` |
| 密码 | （个人密码） |
| 认证方式 | 密码 / 公钥（可选） |

### WSL 关键配置文件

**`/etc/wsl.conf`：**
```ini
[boot]
systemd=true

[user]
default=geist
```

**`/etc/ssh/sshd_config` 关键项：**
```
Port 2222
PasswordAuthentication yes
PermitRootLogin no
```

### 日常使用流程

```
开机 → 打开 PowerShell → 输入 wsl → SSH 服务自动启动 → FinalShell 连接 127.0.0.1:2222
```

---

## 五、技术知识点总结

### 5.1 WSL2 网络架构

```
Windows 主机
├── 127.0.0.1（localhost）──自动转发──→ WSL2 内部服务
├── WSL NAT 网关（172.x.x.x，动态变化）
│   └── Ubuntu 22.04
│       ├── eth0: 172.x.x.x（DHCP 动态分配）
│       ├── SSH 服务（端口 2222）
│       └── systemd 管理服务
```

**关键理解：**
- WSL2 使用 NAT 网络，不是桥接
- Windows → WSL：通过 localhost 自动转发（最可靠）
- WSL → 外网：通过 NAT 网关出去
- WSL IP 每次启动可能变化，不要依赖固定 IP

### 5.2 SSH 服务管理

```bash
# 安装
sudo apt install openssh-server

# 启动/停止/重启
sudo systemctl start/stop/restart ssh

# 查看状态
sudo systemctl status ssh

# 开机自启
sudo systemctl enable ssh

# 查看监听端口
ss -tlnp | grep ssh
# 或
grep '^Port' /etc/ssh/sshd_config
```

### 5.3 排查 SSH 连接问题的标准流程

```
1. 服务是否运行？ → systemctl status ssh
2. 端口是多少？ → grep Port /etc/ssh/sshd_config
3. 网络是否通？ → ping / Test-NetConnection
4. 端口是否可达？ → Test-NetConnection -Port 2222
5. 认证是否正确？ → 检查用户名/密码/密钥
6. 防火墙是否放行？ → sudo ufw status
```

---

## 六、面试可用的话术

### 问：你在开发中遇到过什么网络问题？怎么解决的？

> 在使用 WSL2 + FinalShell 做 Linux 远程开发时，遇到了三个主要问题：
> 
> 第一，SSH 端口不是默认的 22 而是 2222，通过检查 sshd_config 确认了实际监听端口。
> 
> 第二，WSL2 每次重启 IP 都会变化，导致 FinalShell 连接失效。我先尝试了在 WSL 内部用 `ip addr add` 设置固定 IP 并配置 systemd 自启，但发现 Windows 端无法通过这个 IP 访问到 WSL 的端口，因为 WSL2 的 NAT 网络不会转发到手动添加的 IP。最终改用 `127.0.0.1` 连接，利用 WSL2 内置的 localhost 自动转发机制，完美解决了 IP 变化问题。
> 
> 第三，SSH 服务没有随 WSL 启动自动运行，通过在 `/etc/wsl.conf` 中启用 systemd 并 `systemctl enable ssh` 解决。
> 
> 这个过程让我深入理解了 WSL2 的 NAT 网络架构、SSH 服务配置和 systemd 服务管理。

### 问：你对 WSL2 的网络了解多少？

> WSL2 使用的是 NAT 网络模式，和 WSL1 的桥接模式不同。每次启动 WSL2 时，Hyper-V 会创建一个虚拟网卡并分配一个 NAT 网关，WSL 内部的 Ubuntu 通过 DHCP 获取动态 IP。这意味着 WSL 的 IP 不固定。
> 
> 但 Windows 到 WSL 的通信可以通过 localhost 自动转发，这是 WSL2 的一个重要特性。当 Windows 访问 127.0.0.1 的某个端口时，WSL2 会自动将请求转发到 WSL 内部对应端口的服务上。这个机制让我们不需要关心 WSL 的实际 IP，直接用 127.0.0.1 就能访问 WSL 内部的服务。

---

## 七、后续学习方向

- [ ] WSL2 网络模式切换（NAT → Mirrored Mode，Windows 11 22H2+ 支持）
- [ ] Docker 在 WSL2 中的部署和使用
- [ ] VS Code Remote - WSL 开发工作流
- [ ] Linux 防火墙（ufw）配置
- [ ] SSH 密钥管理与安全加固
- [ ] Shell 脚本自动化部署

---

## 八、常用命令速查

| 操作 | 命令 |
|------|------|
| 启动 WSL | `wsl -d Ubuntu-22.04` |
| 查看所有 WSL | `wsl -l -v` |
| 关闭 WSL | `wsl --shutdown` |
| 启动 SSH | `sudo systemctl start ssh` |
| 查看 SSH 状态 | `sudo systemctl status ssh` |
| 查看 WSL IP | `ip addr show eth0 \| grep inet` |
| 测试端口连通 | `Test-NetConnection 127.0.0.1 -Port 2222` |
| 查看监听端口 | `ss -tlnp` |
| 查看防火墙 | `sudo ufw status` |

---

> **记录者：Geist**  
> **每一次踩坑都是成长，每一次解决都是进步。**
