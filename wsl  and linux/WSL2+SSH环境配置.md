# WSL2 + SSH 远程连接记录

环境：Windows 11 + WSL2(Ubuntu 22.04) + FinalShell
目的：在 Windows 上写代码，在 Linux 里跑，用 SSH 工具连过去。

## 一、装环境

```powershell
wsl --install
wsl -l -v          # 确认是 VERSION 2
```

首次启动设置用户名密码。

`/etc/wsl.conf` 我改成了这样：

```ini
[boot]
systemd=true

[user]
default=geist

[automount]
mountFsTab=false

[interop]
enabled=true
appendWindowsPath=true
```

Windows 磁盘挂在 `/mnt/host`，不是默认的 `/mnt/c`。改完要 `wsl --shutdown` 再进才生效。

## 二、开 SSH

```bash
sudo apt update
sudo apt install openssh-server -y
sudo systemctl enable --now ssh
ss -tlnp | grep ssh        # 看实际监听端口
```

## 三、四个坑

### 1. 端口不是 22

按教程填 22 连不上。查配置：

```bash
grep -E '^(Port|PasswordAuthentication|PermitRootLogin)' /etc/ssh/sshd_config
```

实际是 `Port 2222`。FinalShell 改成 2222 就连上了。

**结论**：先确认服务真实监听的端口，`ss -tlnp` 比猜默认值可靠。

### 2. WSL 的 IP 每次重启都变

第一次能连，重启后失效，`ip addr show eth0` 一看网段都变了。

先试了在 WSL 里手动加固定 IP（`ip addr add 192.168.50.10/24 dev eth0`）并写 systemd 服务自启。WSL 内部 ping 得通，但 Windows 端 `Test-NetConnection 192.168.50.10 -Port 2222` 失败——WSL2 是 NAT，不会把请求转发到我自己加的地址上。

改用 `127.0.0.1`：

```powershell
Test-NetConnection 127.0.0.1 -Port 2222     # TcpTestSucceeded = True
```

WSL2 自带 localhost 转发，跟 WSL 的实际 IP 无关，重启也不用改配置。FinalShell 主机就固定填 `127.0.0.1`。

**结论**：Windows 访问 WSL 内部服务走 localhost，不要依赖 WSL 的 IP。排查按层来：ping → 端口连通 → SSH 认证。

### 3. 重启后 SSH 没自启

`systemctl status ssh` 显示 inactive。原因是 `/etc/wsl.conf` 里没开 systemd，服务全靠手动 `service ssh start`。

在 `[boot]` 下加 `systemd=true`，`wsl --shutdown` 重进，再 `systemctl enable ssh`。

### 4. 密码要交互输入，脚本跑不了

`ssh geist@127.0.0.1` 会卡在输密码。两种做法：

```bash
sudo apt install sshpass
sshpass -p '密码' ssh -p 2222 geist@127.0.0.1 'whoami'
```

或者用密钥（更稳，也不用在脚本里写密码）：

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ''
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
ssh -p 2222 -i ~/.ssh/id_rsa geist@127.0.0.1
```

## 四、最终配置

| 项 | 值 |
|---|---|
| 主机 | `127.0.0.1` |
| 端口 | `2222` |
| 用户 | `geist` |
| 认证 | 密码 / 公钥 |
| SSH 配置 | `Port 2222`、`PasswordAuthentication yes`、`PermitRootLogin no` |

日常：开机 → `wsl` → SSH 已随 systemd 启动 → FinalShell 连 `127.0.0.1:2222`。

## 五、常用命令

| 操作 | 命令 |
|---|---|
| 列出发行版 | `wsl -l -v` |
| 关掉 WSL | `wsl --shutdown` |
| 以 root 进 | `wsl -u root` |
| 看监听端口 | `ss -tlnp` |
| 测端口 | `Test-NetConnection 127.0.0.1 -Port 2222` |
| 防火墙 | `sudo ufw status` |

## 待做

- WSL 网络改 mirrored 模式（Win11 22H2+）对比一下和 localhost 转发的差别
- Docker 跑在 WSL 里
- VS Code Remote-WSL 替代 FinalShell
