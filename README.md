# NSGA-II-FJSP-AGVs

A Python implementation of NSGA-II for multi-objective flexible job shop scheduling with AGVs, optimizing makespan and energy consumption.

This repository provides a lightweight research-oriented solver for the Flexible Job Shop Scheduling Problem with Automated Guided Vehicles (FJSP-AGVs). The current implementation uses NSGA-II to optimize two objectives simultaneously:

- `Makespan`
- `Total energy consumption`

The repository includes:

- Core algorithm modules
- Instance parsers and a schedule decoder
- Built-in benchmark datasets
- A batch experiment script for repeated runs
- Example result files and Pareto plots

## Features

- Multi-objective optimization based on `NSGA-II`
- Three-part chromosome representation:
  operation sequence, machine assignment, and AGV assignment
- `POX` crossover for operation sequencing
- `UX` crossover for machine and AGV genes
- Mutation operators for operation, machine, and AGV decisions
- Fast non-dominated sorting and crowding-distance-based environmental selection
- Energy modeling for:
  machine processing, machine idle time, AGV loaded travel, and AGV empty travel
- Support for both single-run testing and repeated batch experiments

## Repository Structure

```text
NSGA-II-FJSP-AGVs/
├─ datasets/
│  └─ FJSP_AGVs/
│     ├─ Bilge and Ulusoy/
│     └─ Brandimarte_Data/
├─ nsga_fjsp_agvs/
│  ├─ NSGA_II.py
│  ├─ decoder.py
│  ├─ environment_selection.py
│  ├─ operators.py
│  ├─ parser.py
│  └─ problem.py
├─ utils/
│  ├─ performance_test.py
│  └─ recorder.py
├─ results/
└─ main.py
```

## Requirements

- Python 3
- Required package: `numpy`
- Optional packages: `tqdm`, `matplotlib`

Install dependencies with:

```bash
pip install numpy tqdm matplotlib
```

If you only want to run `main.py`, `numpy` is the only required package. `tqdm` and `matplotlib` are mainly used by `utils/performance_test.py` for progress display and plotting.

## Quick Start

Run the default example:

```bash
python main.py
```

The current default configuration in `main.py` is:

- Dataset: `Bilge and Ulusoy`
- Instance: `Jobset01`
- Layout: `Layout1`
- Stopping criterion: `max_fe = 10000`
- Population size: `100`
- Crossover probability: `0.9`
- Mutation probability: `0.15`

Example console output from a real run:

```text
Stopping criterion: 10000 function evaluations
Final Pareto front (makespan, energy):
Solution 1: makespan = 75.00, energy = 5667.00
```

## Batch Experiments

To perform repeated runs, save Pareto history, export CSV files, and generate Pareto plots, run:

```bash
python utils/performance_test.py
```

This script can:

- Run a selected dataset multiple times
- Save Pareto-front history for each run
- Merge Pareto points across runs
- Export result tables as CSV files
- Generate scatter plots for Pareto fronts

## Supported Datasets

The repository currently includes two dataset groups:

- `datasets/FJSP_AGVs/Bilge and Ulusoy`
- `datasets/FJSP_AGVs/Brandimarte_Data`

Job data and transport-layout data are stored separately and loaded automatically at runtime:

- Instance files such as `Jobset01.txt` and `Mk01.txt`
- Layout files such as `Layout1.txt` and `Layout.txt`

## Objective Definition

The solver optimizes two objectives:

1. `Makespan`
2. `Total Energy`

The total energy value currently includes:

- Machine processing energy
- Machine idle energy
- AGV empty-travel energy
- AGV loaded-travel energy

## Main Modules

- `nsga_fjsp_agvs/problem.py`: problem definition, individual creation, initialization, crossover, and mutation flow
- `nsga_fjsp_agvs/decoder.py`: schedule decoding and objective evaluation
- `nsga_fjsp_agvs/NSGA_II.py`: NSGA-II main loop
- `nsga_fjsp_agvs/environment_selection.py`: non-dominated sorting and crowding-distance selection
- `nsga_fjsp_agvs/operators.py`: initialization, crossover, and mutation operators
- `utils/performance_test.py`: repeated experiments, statistics, CSV export, and plotting

## Example Result

An example result folder is included at:

`results/Brandimarte_Data/Mk01_Layout/`

Example plot:

![Combined Pareto Front](results/Brandimarte_Data/Mk01_Layout/combined_pareto_front.png)

## Customization

You can directly modify parameters in `main.py` or `utils/performance_test.py`, for example:

- Dataset and layout selection
- `max_fe`
- Population size `pop_size`
- Crossover probability `cr`
- Mutation probability `mu`
- Number of repeated runs `num_runs`

## Notes

- This repository is suitable as a baseline implementation for research on FJSP-AGVs and multi-objective evolutionary optimization.
- If you plan to publish this project on GitHub, it is recommended to also add a `LICENSE`, citation information, and a more formal experiment description.

## Citation

If this repository helps your research, please cite the related paper or mention the project source and your modifications in your publication or repository.
