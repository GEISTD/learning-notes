# WSL + Git 开发环境搭建记录

## 日期
2026-09-17

## 一、WSL2 环境配置

- 使用 `wsl --import` 方式部署 Ubuntu 发行版
- 理解 WSL 与 Windows 文件系统映射关系：
  - Windows 路径：`C:\Users\29681\Desktop`
  - WSL 路径：`/mnt/host/c/Users/29681/Desktop`
- 配置 `/etc/wsl.conf` 实现以下目标：
  - Windows 磁盘挂载至 `/mnt/host`
  - 启用 `metadata` 选项以支持 Linux 文件权限
  - 启用 `interop` 以支持在 WSL 中运行 Windows 程序
  - 设置默认登录用户为 `geist`

## 二、用户与权限管理

- 确认系统中存在 `geist` 用户
- 理解 WSL 启动机制：
  - 默认用户由 `/etc/wsl.conf` 中 `[user] default=geist` 控制
  - 启动路径继承自 Windows 当前目录（如在 Desktop 启动则路径为 Desktop）
  - 使用 `cd ~` 可切换至用户家目录 `/home/geist`
- 区分 root（`#`）与普通用户（`$`）权限差异

## 三、Git 前置认知

- 明确 Git 是“代码级快照”，类比 VMware 快照与 WSL 导出备份
- 理解本地仓库、远程仓库（origin / github）、分支（master / main）的关系
- 为后续 GitHub 每日贡献（30 天计划）完成基础环境准备

## 四、关键命令与实践

- `wsl --shutdown`：彻底重启 WSL 虚拟机
- `wsl -u root`：以 root 身份进入 WSL
- `cat > /etc/wsl.conf <<'EOF' ... EOF`：干净覆盖配置文件，避免重复与冲突
- `cd ~` / `pwd` / `whoami`：验证当前路径与用户身份

## 五、当前状态

- ✅ 默认用户：`geist`
- ✅ 家目录：`/home/geist`
- ✅ WSL 配置干净，无报错
- ✅ 已具备 Git 操作的基础环境

## 下一步计划

- 在 WSL 中初始化 Git 仓库
- 配置 Git 用户名与邮箱
- 完成首次 commit 并推送至 GitHub