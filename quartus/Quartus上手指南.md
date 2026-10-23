# Quartus 18.1 上手指南（配合 W4C4 实验1）

> 目标：能独立从"老师给的一个 .v 文件"走到"板子上看到结果"。
> 本机路径：Quartus `D:\Download\quartus\bin64\quartus.exe`，ModelSim `D:\Download\modelsim_ase\win32aloem\modelsim.exe`

---

## 0. 先分清三个东西（新手 90% 的困惑都在这）

| 东西 | 长什么样 | 作用 |
|---|---|---|
| 源文件 | `W4C4_2025112470_exp1.v` | 老师给的 Verilog 代码，纯文本 |
| 工程文件 | `code1_decoder.qpf` + `code1_decoder.qsf` | `.qpf`="这是个工程"，`.qsf`=所有设置（器件、文件、引脚） |
| 顶层实体 | `.v` 里的 `module code1_decoder` | Quartus 从这个 module 开始往下综合 |

**最容易犯的错：双击 `.v` 打开的是"文本编辑器"，不是工程。**
判断自己开的是不是工程 → 看窗口左边有没有 **Project Navigator** 面板、标题栏有没有工程名。

- 打开工程：双击 `.qpf`，或 `File > Open Project`
- 打开文件：`File > Open`（只能看代码，不能编译下载）

---

## 1. 新建工程：File > New Project Wizard

| 步骤 | 填什么 | 为什么 |
|---|---|---|
| 1 Introduction | Next | — |
| 2 Directory / Name / Top-Level | 目录 `D:\fpga_lab\exp1`（**全英文、无空格**）<br>工程名 `code1_decoder`<br>顶层实体 `code1_decoder` | 工程名随便起，但**顶层实体名必须和 `module` 名一字不差**（大小写敏感） |
| 3 Project Type | Empty project | 空工程，文件自己加 |
| 4 Add Files | 选 `W4C4_2025112470_exp1.v` → Add | **只加设计文件，不要加 `_test.v`**（原因见第 7 节） |
| 5 Family & Device | Family 选 `Cyclone IV E`<br>过滤 Package=TQFP、Pin count=144、Speed grade=8<br>选 `EP4CE6E22C8` | 板上丝印常写 `EP4CE6E22C8N`，N 只表示无铅，Quartus 里**选不带 N 的** |
| 6 EDA Tool Settings | Simulation = `ModelSim-Altera`，Format = `Verilog HDL` | 后面调仿真用 |
| 7 Summary | Finish | — |

验收：Project Navigator → Hierarchy 里 `code1_decoder` 在顶层；Files 里有那个 `.v`。

> 中文路径本次实测能编过，但换实验室电脑/换 Quartus 版本经常炸（路径被截断、生成文件乱码），**养成英文目录的习惯**。

---

## 2. 第一次编译：Processing > Start Analysis & Synthesis（Ctrl+K）

**做什么**：把 Verilog 翻译成门级网表，检查语法、端口、位宽、悬空信号。

**为什么先做这一步**：两个原因
1. 语法错了后面全部白做，先花 5 秒排掉；
2. **Pin Planner 里的信号列表来自综合结果**——没综合过，Pin Planner 里可能是空的，你连 `din[0]` 都找不到。

**看哪**：下方 Messages 窗口，`Error` 必须为 0（红色）；`Warning` 一般可忽略（黄色，如"没有时钟"对本实验是正常的）。

---

## 3. 引脚锁定：Assignments > Pin Planner（Ctrl+Shift+N）

这是 FPGA 实验里**最容易出错、也最能体现"你在用 Quartus"**的一步。

概念：FPGA 的引脚是"通用"的，代码里 `din[0]` 只是个名字，**Quartus 不知道它该接板上哪个物理脚**。不锁引脚，Fitter 会自己乱分配，下到板子上现象就是随机的。

操作：
1. 表格里 **Node Name** 列是代码里的端口名，一行一个：`din[0]`、`din[1]`…`dout[7]`、`seg`
2. 在 **Location** 列填 `PIN_24` 这样的值，必须带 `PIN_` 前缀
3. **I/O Standard** 选 `3.3-V LVTTL`
4. 关掉窗口（自动存进 `.qsf`），然后**必须重新全编译**

三个必错点：
- 位宽写成 `din0` / `din` —— 不行，总线必须带下标
- 大小写：`PIN_24` 和 `pin_24` 都能认，但信号名 `din[0]` 必须和代码完全一致
- 锁完引脚**不重新编译** —— 引脚信息是 Fitter 阶段用的，不重编等于没改

验证：`Compilation Report → Fitter → Pin-Out Files`，或直接看工程目录里的 `.pin` 文件。

---

## 4. 全编译：Processing > Start Compilation（Ctrl+L）

四个阶段各自干什么：

| 阶段 | 干什么 | 出错时说明 |
|---|---|---|
| Analysis & Synthesis | Verilog → 网表 | 代码语法/位宽错 |
| Fitter | 网表 → 具体放哪个 LE、哪个引脚 | 引脚冲突、器件资源不够、引脚号不存在 |
| Assembler | 生成 `.sof` 比特流 | — |
| Timing Analyzer | 时序检查 | 组合逻辑无时钟，本实验必然是 5 个 warning，正常 |

产物：`code1_decoder.sof`（工程根目录，或 `output_files\`）。

---

## 5. 抄实验报告的数据在哪

`Compilation Report → Flow Summary`（或 `Fitter → Summary`）：

| 报告栏目 | 本实验实测值 |
|---|---|
| Top-level Entity name | code1_decoder |
| Family | Cyclone IV E |
| Device | EP4CE6E22C8 |
| Total logic elements | **8** / 6,272 |
| Total registers | 0 |
| Total pins | **13** / 92 |
| Total memory bits | 0 |
| Embedded Multiplier 9-bit elements | 0 |
| Total PLLs | 0 |

> 报告里写"16（预估）"是不对的，真实值是 8：4→8 译码每个输出位就是一个 4 输入 LUT，正好 8 个 LE。

---

## 6. 仿真：ModelSim 六步

**为什么 testbench 不能加进 Quartus 工程**：它没有端口、里面有 `#20` 延时和 `$display`，这些**不可综合**。加进工程会让综合报错或生成一堆垃圾逻辑。Testbench 只给仿真器看。

手工流程（GUI）：

1. 启动 `modelsim.exe`
2. `File > Change Directory` → 切到 `...\exp1\sim`
3. `File > New > Library` → 库名 `work` → OK
4. `Compile > Compile` → 两个 `.v` 一起选上 → Compile → Done
5. `Simulate > Start Simulation` → 展开 `work` → 选 `W4C4_2025112470_exp1_test` → OK
6. `View > Wave`；在 Objects 窗口里展开 `uut`，选 `din`、`dout`、`seg` → 右键 `Add to > Wave > Selected Signals`；然后 `run 340 ns`（或 `run -all`）
7. 选 `dout` → 右键 `Radix > Unsigned`，波形就变成十进制；`File > Save Format` 存成 `.do` 下次直接用

命令行等价（本次实际跑过的）：

```
vlib work
vlog ..\src\W4C4_2025112470_exp1.v ..\src\W4C4_2025112470_exp1_test.v
vsim -c -do "run -all; quit -f" work.W4C4_2025112470_exp1_test
```

看老师给的 `.wlf` 波形库：`vsim -view W4C4_2025112470_exp1_test.wlf`
（`.wlf` 是二进制波形库，不能"双击打开"，必须由 vsim 载入）

---

## 7. 下载：Tools > Programmer

1. `Tools > Programmer`
2. `Hardware Setup...` → 选 `USB-Blaster [USB-0]`（列表空 → 驱动/线的问题）
3. `Mode` 选 `JTAG`
4. `Add File...` → `code1_decoder.sof` → 勾上 `Program/Configure`
5. `Start` → 进度 100% + `Configuration succeeded`

**断电即失效**：`.sof` 烧的是 FPGA 内部 SRAM，掉电就没了。
需要上电自动加载：`File > Convert Programming Files` 生成 `.jic`，烧到板上的 EPCS 配置芯片（Mode 选 Active Serial）。这是进阶项，实验一般不要求。

---

## 8. 高频报错对照表

| 现象 | 原因 | 解决 |
|---|---|---|
| `Top-level entity "xxx" not found` | 顶层实体名 ≠ module 名 | 改成一致，或右键文件 `Set as Top-Level Entity` |
| 综合报错说找不到模块 | `.v` 没加进工程 | Project Navigator 右键 `Add/Remove Files` |
| `Error: Cannot assign pin PIN_xx to node` | 信号名写错/位宽不符 | 必须写 `din[0]` |
| `PIN_xx is not a valid location` | 器件或封装选错 | 重选 `EP4CE6E22C8`（TQFP144） |
| Programmer 报 `Device does not match` | `.sof` 与板上芯片不是同一颗 | 换对的器件重新编译 |
| 仿真 `Failed to access library "work"` | 没建库 / 不在对的目录 | `File > New > Library` 建 `work` |
| 波形是直线/全 X | 没加 testbench 或没例化 DUT | 仿真顶层必须选 `*_test` |
| 编译巨慢 / 莫名错误 | 中文路径、空格、网盘同步目录 | 换 `D:\fpga_lab\xxx` |
| 板子毫无反应 | 上电后没重新下载（SRAM 掉电丢失） | 重新 Program |

---

## 9. 本实验参数速查

- 器件：`EP4CE6E22C8`，Cyclone IV E，TQFP144
- 顶层：`code1_decoder`
- 13 个引脚：

| 信号 | PIN | | 信号 | PIN |
|---|---|---|---|---|
| din[0] | 24 | | dout[2] | 104 |
| din[1] | 31 | | dout[3] | 111 |
| din[2] | 30 | | dout[4] | 106 |
| din[3] | 33 | | dout[5] | 110 |
| dout[0] | 112 | | dout[6] | 103 |
| dout[1] | 100 | | dout[7] | 105 |
| seg | 119 | | | |

- 实测极性/段序：`dout[0]=a … dout[7]=dp`，**高电平点亮**，`din=0` 全灭
- 资源：8 LE、0 寄存器、13 引脚

