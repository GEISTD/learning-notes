# Quartus / FPGA 数电实验

数字电子技术实验（Quartus 18.1 Lite + Cyclone IV E）的完整流程、踩坑记录与实测数据。

## 目录内容

| 文件 | 内容 |
|---|---|
| `从零建工程手把手.md` | 以 4 位加法器为例的从零教程（建工程→写 .v→编译→仿真，附无 Quartus 时的 EDA Playground 路线） |
| `Quartus上手指南.md` | 以译码显示电路（实验 1）为例的实战流程，click-by-click，含 9 条报错对照表 |
| `真值表.md` | 译码显示电路真值表：逐位点亮版 + 0~F 七段版（两种功能表） |
| `实测记录.md` | 本机实测：驱动、JTAG、编译资源、引脚落位、上板观察表 |

## 七步流程

```
建工程(选对器件) → 写/加 .v → Ctrl+K 综合 → ModelSim 仿真验证
→ Pin Planner 锁脚 → Ctrl+L 全编译 → Programmer 下载
```

| # | 做什么 | 位置 | 产物 / 验收 |
|---|---|---|---|
| 1 | 建工程：Cyclone IV E → TQFP / 144 / speed 8 → `EP4CE6E22C8`，顶层实体名 = module 名 | File > New Project Wizard | `.qpf` + `.qsf` |
| 2 | 加/写设计文件 | Ctrl+N 新建 或 Add Files | Project Navigator → Files 里有它 |
| 3 | 综合 `Ctrl+K` | Processing | Error 0（此时才有信号名可锁脚） |
| 4 | 写 testbench → ModelSim 建 work 库 → 编译 → 仿真 | ModelSim（**testbench 不加进 Quartus 工程**） | 17 项 0 错误，波形对得上真值表 |
| 5 | 锁引脚 | Pin Planner（Ctrl+Shift+N） | Location 列填 `PIN_xx`，I/O 选 3.3-V LVTTL |
| 6 | 全编译 `Ctrl+L` | Processing | 0 error，生成 `.sof`（引脚在 Fitter 阶段才生效） |
| 7 | 插板 → Programmer → Start | Tools > Programmer | `Configuration succeeded`，板上现象正确 |

## 三个必须理解的"为什么"

1. **先综合再锁引脚**：Pin Planner 的信号名单来自综合结果，没综合过名单是空的。
2. **锁完引脚要重新全编译**：引脚信息由 Fitter 阶段消耗，不重编等于没改。
3. **仿真和引脚无关**：仿真只验证逻辑（在电脑里跑），引脚决定物理连接，最后在芯片里合流。

## 五个高频坑

1. 双击 `.v` 打开的是文本编辑器，**打开工程要双击 `.qpf`**（看左边有没有 Project Navigator）。
2. 顶层实体名必须等于 `module` 名，否则 `Top-level entity not found`。
3. testbench 不可综合（有 `#20`、`$display`），**不能加进 Quartus 工程**。
4. `.sof` 烧进 SRAM，**断电即丢**，每次上电都要重新下载（要断电保存得转 `.jic` 烧 EPCS）。
5. 波形默认十六进制显示，和二进制真值表"看着不一样"——右键 `Radix > Binary` 即可。

## 环境速查（本机）

| 项 | 值 |
|---|---|
| Quartus | 18.1.0 Build 625 Lite，`D:\Download\quartus\bin64\quartus.exe` |
| ModelSim | ModelSim-Intel FPGA Starter 10.5b，`D:\Download\modelsim_ase\win32aloem\modelsim.exe` |
| 器件 | `EP4CE6E22C8`，Cyclone IV E，TQFP-144，speed grade 8 |
| 下载线 | USB-Blaster，JTAG IDCODE `0x020F10DD` |
| 驱动注意 | Quartus 18.1 自带 `usbblstr.sys` 2.12.00（2014）在 Win11 下 **Code 39 / 0xc000007b 加载失败**，改用 Quartus 24.1 的 2.12.28（FTDI 签名）后正常 |
| 下载命令 | `quartus_pgm -c 1 -m jtag -o "p;<file>.sof"` |
