from __future__ import annotations

import numpy as np


class FJSPAGVSDecoder:
    def __init__(self, work, machine_time, agv_num, trans):
        self.work = work
        self.machine_time = machine_time
        self.agv_num = agv_num
        self.trans = trans

    def calculate(self, job_code, machine_code, agv_code):
        job_num = max(job_code)
        machine_num = max(machine_code)

        t_job = np.zeros((1, job_num), dtype=int)
        t_machine = np.zeros((1, machine_num), dtype=int)
        t_agv = np.zeros(self.agv_num, dtype=int)

        agv_position = np.zeros(self.agv_num, dtype=int)
        job_position = np.zeros(job_num, dtype=int)
        count = np.zeros((1, job_num), dtype=int)

        machine_processing_energy = np.zeros(machine_num)
        machine_processing_time = np.zeros(machine_num)
        agv_loaded_energy = 0.0
        agv_empty_energy = 0.0

        processing_power = 30.0
        idle_power = 1.0
        loaded_power = 10.0
        empty_power = 0.5

        for seq_idx in range(len(job_code)):
            job_idx = job_code[seq_idx] - 1
            op_idx = self.work.index(job_idx + 1) + count[0, job_idx]
            machine_id = machine_code[op_idx]

            start_pos = int(job_position[job_idx])
            end_pos = int(machine_id)
            need_transport = start_pos != end_pos

            if need_transport:
                agv_idx = int(agv_code[seq_idx]) - 1
                empty_time = self.trans[int(agv_position[agv_idx])][start_pos]
                loaded_time = self.trans[start_pos][end_pos]

                empty_end = int(t_agv[agv_idx]) + int(empty_time)
                pickup_time = max(empty_end, int(t_job[0, job_idx]))
                drop_time = pickup_time + int(loaded_time)

                t_agv[agv_idx] = drop_time
                agv_position[agv_idx] = end_pos

                agv_empty_energy += empty_power * float(empty_time)
                agv_loaded_energy += loaded_power * float(loaded_time)

                start_time = max(int(t_job[0, job_idx]), int(t_machine[0, machine_id - 1]), int(t_agv[agv_idx]))
            else:
                start_time = max(int(t_job[0, job_idx]), int(t_machine[0, machine_id - 1]))

            processing_time = self.get_processing_time(op_idx, machine_id)
            machine_processing_energy[machine_id - 1] += processing_time * processing_power
            machine_processing_time[machine_id - 1] += processing_time

            finish_time = start_time + processing_time
            t_machine[0, machine_id - 1] = finish_time
            t_job[0, job_idx] = finish_time
            job_position[job_idx] = end_pos
            count[0, job_idx] += 1

        c_max = max(t_job[0])

        machine_idle_energy = np.zeros(machine_num)
        for machine_idx in range(machine_num):
            idle_time = c_max - machine_processing_time[machine_idx]
            machine_idle_energy[machine_idx] = idle_power * idle_time

        total_energy = np.sum(machine_processing_energy)
        total_energy += np.sum(machine_idle_energy)
        total_energy += agv_loaded_energy + agv_empty_energy

        return [float(c_max), float(total_energy)]

    def decode_with_details(self, job_code, machine_code, agv_code):
        job_num = max(job_code)
        machine_num = max(machine_code)

        t_job = np.zeros(job_num, dtype=int)
        t_machine = np.zeros(machine_num, dtype=int)
        t_agv = np.zeros(self.agv_num, dtype=int)

        agv_position = np.zeros(self.agv_num, dtype=int)
        job_position = np.zeros(job_num, dtype=int)
        count = np.zeros(job_num, dtype=int)

        machine_processing_energy = np.zeros(machine_num)
        machine_processing_time = np.zeros(machine_num)
        agv_loaded_energy = 0.0
        agv_empty_energy = 0.0

        processing_power = 30.0
        idle_power = 1.0
        loaded_power = 10.0
        empty_power = 0.5

        operations = []
        agv_moves = []

        for seq_idx in range(len(job_code)):
            job_idx = job_code[seq_idx] - 1
            op_idx = self.work.index(job_idx + 1) + count[job_idx]
            op_id = int(count[job_idx]) + 1
            machine_id = int(machine_code[op_idx])

            start_pos = int(job_position[job_idx])
            end_pos = int(machine_id)
            need_transport = start_pos != end_pos

            agv_id = None
            transport_ready_time = int(t_job[job_idx])

            if need_transport:
                agv_idx = int(agv_code[seq_idx]) - 1
                agv_id = agv_idx + 1
                empty_time = int(self.trans[int(agv_position[agv_idx])][start_pos])
                loaded_time = int(self.trans[start_pos][end_pos])

                empty_start = int(t_agv[agv_idx])
                empty_finish = empty_start + empty_time
                loaded_start = max(empty_finish, int(t_job[job_idx]))
                loaded_finish = loaded_start + loaded_time

                t_agv[agv_idx] = loaded_finish
                agv_position[agv_idx] = end_pos
                transport_ready_time = loaded_finish

                agv_empty_energy += empty_power * float(empty_time)
                agv_loaded_energy += loaded_power * float(loaded_time)

                agv_moves.append(
                    {
                        "seq_id": seq_idx + 1,
                        "agv_id": agv_id,
                        "job_id": job_idx + 1,
                        "op_id": op_id,
                        "from_pos": start_pos,
                        "to_pos": end_pos,
                        "empty_start": empty_start,
                        "empty_finish": empty_finish,
                        "empty_duration": empty_time,
                        "loaded_start": loaded_start,
                        "loaded_finish": loaded_finish,
                        "loaded_duration": loaded_time,
                    }
                )

            start_time = max(
                int(t_job[job_idx]),
                int(t_machine[machine_id - 1]),
                transport_ready_time,
            )

            processing_time = self.get_processing_time(op_idx, machine_id)
            machine_processing_energy[machine_id - 1] += processing_time * processing_power
            machine_processing_time[machine_id - 1] += processing_time

            finish_time = start_time + processing_time
            t_machine[machine_id - 1] = finish_time
            t_job[job_idx] = finish_time
            job_position[job_idx] = end_pos
            count[job_idx] += 1

            operations.append(
                {
                    "seq_id": seq_idx + 1,
                    "job_id": job_idx + 1,
                    "op_id": op_id,
                    "machine_id": machine_id,
                    "agv_id": agv_id,
                    "from_pos": start_pos,
                    "to_pos": end_pos,
                    "start_time": start_time,
                    "finish_time": finish_time,
                    "process_time": processing_time,
                }
            )

        c_max = int(max(t_job)) if len(t_job) > 0 else 0

        machine_idle_energy = np.zeros(machine_num)
        for machine_idx in range(machine_num):
            idle_time = c_max - machine_processing_time[machine_idx]
            machine_idle_energy[machine_idx] = idle_power * idle_time

        total_energy = np.sum(machine_processing_energy)
        total_energy += np.sum(machine_idle_energy)
        total_energy += agv_loaded_energy + agv_empty_energy

        return {
            "objectives": {
                "makespan": float(c_max),
                "energy": float(total_energy),
            },
            "operations": operations,
            "agv_moves": agv_moves,
            "machine_num": machine_num,
            "agv_num": self.agv_num,
        }

    def get_processing_time(self, operation_idx, machine_id):
        if operation_idx < len(self.machine_time):
            pairs = self.machine_time[operation_idx]
            for index in range(0, len(pairs), 2):
                if index + 1 < len(pairs) and pairs[index] == machine_id:
                    return pairs[index + 1]
        return 1
