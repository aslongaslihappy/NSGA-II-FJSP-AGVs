from __future__ import annotations

import random

import numpy as np


class FJSPAGVSInitialization:
    def __init__(self, work, machine_time, agv_num):
        self.work = work
        self.machine_time = machine_time
        self.agv_num = agv_num

    def create_chromosome_random(self):
        job_code = np.copy(self.work)
        np.random.shuffle(job_code)
        job_code = job_code.tolist()

        machine_code = []
        agv_code = []
        for operation_index in range(len(job_code)):
            operation_machine_time = self.machine_time[operation_index]
            candidate_machines = [operation_machine_time[index] for index in range(0, len(operation_machine_time), 2)]
            machine_code.append(candidate_machines[np.random.randint(0, len(candidate_machines), 1)[0]])
            agv_code.append(np.random.randint(1, self.agv_num + 1, 1)[0])

        return job_code, machine_code, agv_code


class FJSPAGVSCrossover:
    def pox(self, parent1, parent2):
        job_list = list(set(parent1))
        split_index = np.random.randint(0, len(job_list), 1)[0]
        job_set1 = job_list[: split_index + 1]

        offspring1 = []
        offspring2 = []
        genes_to_fill1 = []
        genes_to_fill2 = []

        for index in range(len(parent1)):
            gene1 = parent1[index]
            gene2 = parent2[index]

            if gene1 in job_set1:
                offspring1.append(gene1)
            else:
                genes_to_fill2.append(gene1)
                offspring1.append(-1)

            if gene2 in job_set1:
                offspring2.append(gene2)
            else:
                genes_to_fill1.append(gene2)
                offspring2.append(-1)

        for index in range(len(parent1)):
            if offspring1[index] == -1:
                offspring1[index] = genes_to_fill1.pop(0)
            if offspring2[index] == -1:
                offspring2[index] = genes_to_fill2.pop(0)

        return offspring1, offspring2

    def ux(self, parent1_code, parent2_code):
        child1_code = parent1_code.copy()
        child2_code = parent2_code.copy()
        mask = [random.randint(0, 1) for _ in range(len(parent1_code))]

        for index in range(len(parent1_code)):
            if mask[index] == 1:
                child1_code[index], child2_code[index] = child2_code[index], child1_code[index]

        return child1_code, child2_code


class FJSPAGVSMutation:
    def __init__(self, machine_time, agv_num):
        self.machine_time = machine_time
        self.agv_num = agv_num

    def mutate_operation_sequence(self, job_code):
        if len(job_code) <= 1:
            return job_code.copy()

        index1, index2 = random.sample(range(len(job_code)), 2)
        if index1 > index2:
            index1, index2 = index2, index1

        mutated = job_code.copy()
        value = mutated[index2]
        del mutated[index2]
        mutated.insert(index1, value)
        return mutated

    def mutate_machine_selection(self, machine_code):
        if len(machine_code) == 0:
            return machine_code.copy()

        operation_index = random.randint(0, len(machine_code) - 1)
        operation_machine_time = self.machine_time[operation_index]
        candidate_machines = [operation_machine_time[index] for index in range(0, len(operation_machine_time), 2)]

        if candidate_machines:
            mutated = machine_code.copy()
            mutated[operation_index] = random.choice(candidate_machines)
            return mutated

        return machine_code.copy()

    def mutate_agv_selection(self, agv_code):
        if len(agv_code) == 0:
            return agv_code.copy()

        operation_index = random.randint(0, len(agv_code) - 1)
        mutated = agv_code.copy()
        mutated[operation_index] = random.randint(1, self.agv_num)
        return mutated
