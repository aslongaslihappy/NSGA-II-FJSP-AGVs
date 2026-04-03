# NSGA-II-FJSP-AGVs

A lightweight Python implementation of a multi-objective NSGA-II solver for the Flexible Job Shop Scheduling Problem with Automated Guided Vehicles (FJSP-AGVs).

本项目实现了一个面向 `FJSP-AGVs` 的多目标优化求解器，使用 `NSGA-II` 同时优化：

- `Makespan`（最大完工时间）
- `Energy Consumption`（总能耗）

仓库中包含：

- 核心算法实现
- 数据解析与解码器
- 两套测试数据集
- 批量实验与 Pareto 前沿记录脚本
- 部分实验结果示例

## Features

- 基于 `NSGA-II` 的多目标进化求解框架
- 三段式染色体编码：工序顺序、机器选择、AGV 选择
- 支持 `POX` 与 `UX` 交叉算子
- 支持工序、机器、AGV 三类变异
- 基于快速非支配排序与拥挤距离的环境选择
- 同时考虑机器加工能耗、机器空闲能耗、AGV 空载与载货运输能耗
- 支持单次求解和多次重复实验

## Repository Structure

```text
NSGA-II-FJSP-AGVs/
├─ datasets/                 # FJSP-AGVs benchmark datasets
│  └─ FJSP_AGVs/
│     ├─ Bilge and Ulusoy/
│     └─ Brandimarte_Data/
├─ nsga_fjsp_agvs/           # Core algorithm modules
│  ├─ NSGA_II.py
│  ├─ decoder.py
│  ├─ environment_selection.py
│  ├─ operators.py
│  ├─ parser.py
│  └─ problem.py
├─ utils/
│  ├─ performance_test.py    # Batch experiment / Pareto statistics
│  └─ recorder.py            # Pareto front extraction and printing
├─ results/                  # Saved experiment results
└─ main.py                   # Default entry point
```

## Environment

- Python 3
- Required: `numpy`
- Optional: `tqdm`, `matplotlib`

安装依赖：

```bash
pip install numpy tqdm matplotlib
```

如果你只运行 `main.py`，核心依赖是 `numpy`；`tqdm` 和 `matplotlib` 主要用于 `utils/performance_test.py` 的批量实验与绘图。

## Quick Start

直接运行默认示例：

```bash
python main.py
```

当前默认配置位于 `main.py`：

- 数据集：`Bilge and Ulusoy`
- 算例：`Jobset01`
- 车间布局：`Layout1`
- 停止条件：`max_fe=10000`
- 种群规模：`100`
- 交叉概率：`0.9`
- 变异概率：`0.15`

一次实际运行的终端输出示例：

```text
Stopping criterion: 10000 function evaluations
Final Pareto front (makespan, energy):
Solution 1: makespan = 75.00, energy = 5667.00
```

## Batch Experiments

如果你想做重复实验、保存每次运行的 Pareto 前沿，并自动生成 CSV 和图像，可以运行：

```bash
python utils/performance_test.py
```

该脚本会：

- 重复运行指定数据集多次
- 保存每次实验的 Pareto 历史
- 汇总全部非支配解
- 导出 `csv` 文件
- 生成 Pareto 散点图

## Dataset Support

当前仓库内置了两类数据：

- `datasets/FJSP_AGVs/Bilge and Ulusoy`
- `datasets/FJSP_AGVs/Brandimarte_Data`

布局运输时间矩阵与作业数据分开存储，程序会在运行时自动读取：

- 作业实例文件：如 `Jobset01.txt`、`Mk01.txt`
- 布局文件：如 `Layout1.txt`、`Layout.txt`

## Objective Definition

当前实现返回两个优化目标：

1. `Makespan`
2. `Total Energy`

其中总能耗由以下部分组成：

- 机器加工能耗
- 机器空闲能耗
- AGV 空载运输能耗
- AGV 载货运输能耗

## Main Modules

- `nsga_fjsp_agvs/problem.py`：问题定义、个体表示、种群初始化、交叉与变异调度
- `nsga_fjsp_agvs/decoder.py`：根据染色体计算调度结果与目标值
- `nsga_fjsp_agvs/NSGA_II.py`：NSGA-II 主流程
- `nsga_fjsp_agvs/environment_selection.py`：非支配排序与拥挤距离选择
- `nsga_fjsp_agvs/operators.py`：初始化、交叉与变异算子
- `utils/performance_test.py`：批量测试、结果统计与绘图

## Example Result

仓库中已包含一组示例结果，位于：

`results/Brandimarte_Data/Mk01_Layout/`

示例图如下：

![Combined Pareto Front](results/Brandimarte_Data/Mk01_Layout/combined_pareto_front.png)

## How To Customize

你可以直接修改 `main.py` 或 `utils/performance_test.py` 中的参数，例如：

- 切换数据集与布局
- 修改 `max_fe`
- 修改种群规模 `pop_size`
- 修改交叉概率 `cr`
- 修改变异概率 `mu`
- 调整重复实验次数 `num_runs`

## Notes

- 当前仓库适合作为 FJSP-AGVs 与多目标进化算法的研究代码基础版本。
- 如果你准备公开到 GitHub，建议补充 `LICENSE`、论文引用信息和更系统的实验说明。

## Citation

如果这个项目对你的研究有帮助，建议在你的 GitHub 仓库或论文中注明项目来源与改进内容。
