from __future__ import annotations

import re
from pathlib import Path


DATASET_ROOT = Path(__file__).resolve().parent.parent / "datasets" / "FJSP_AGVs"


def read_trans(dataset_name, layout_name):
    layout_path = DATASET_ROOT / dataset_name / f"{layout_name}.txt"
    if not layout_path.exists():
        raise FileNotFoundError(f"Transport matrix file not found: {layout_path}")

    with open(layout_path, "r", encoding="utf-8") as file:
        rows = file.read().splitlines()

    trans = []
    for row in rows[1:]:
        if not row:
            continue
        trans.append([int(value) for value in re.findall(r"[0-9]+", row)])

    return trans


def read_fjsp_agvs_instance(dataset_name, instance_name, layout_name):
    instance_path = DATASET_ROOT / dataset_name / f"{instance_name}.txt"
    if not instance_path.exists():
        raise FileNotFoundError(f"Data file not found: {instance_path}")

    with open(instance_path, "r", encoding="utf-8") as file:
        lines = [line.rstrip() for line in file.readlines() if line.strip()]

    work, machine_time, agv_num = _parse_jobset(lines)
    trans = read_trans(dataset_name, layout_name)
    return work, machine_time, agv_num, trans


def _parse_jobset(lines):
    header = [int(value) for value in re.findall(r"[0-9]+", lines[0])]
    if len(header) < 3:
        raise ValueError(f"Invalid AGVS header: {lines[0]}")

    job_count = header[0]
    agv_num = header[2]
    work = []
    machine_time = []

    for job_index, row in enumerate(lines[1 : 1 + job_count]):
        values = [int(value) for value in re.findall(r"[0-9]+", row)]
        if not values:
            continue

        operation_count = values[0]
        work.extend([job_index + 1] * operation_count)

        row_tail = values[1:]
        for _ in range(operation_count):
            if not row_tail:
                raise ValueError("Invalid job row: missing operation machine options")

            candidate_count = row_tail[0]
            operation_pairs = []
            for index in range(candidate_count):
                pair = row_tail[2 * index + 1 : 2 * index + 3]
                if len(pair) < 2:
                    raise ValueError("Invalid job row: missing machine-time pair")
                operation_pairs.extend(pair)
            machine_time.append(operation_pairs)
            row_tail = row_tail[2 * candidate_count + 1 :]

    return work, machine_time, agv_num
