from __future__ import annotations

from nsga_fjsp_agvs.NSGA_II import NSGA_II
from nsga_fjsp_agvs.problem import FJSPAGVSProblem
from utils.recorder import get_final_pareto_front, print_pareto_front, record_best_makespan_gantt


def main():
    problem = FJSPAGVSProblem("Bilge and Ulusoy", "Jobset01", "Layout1", max_fe=10000)
    problem.enable_local_search = True

    algorithm = NSGA_II(problem)
    algorithm.pop_size = 100
    algorithm.cr = 0.9
    algorithm.mu = 0.15

    print(f"Stopping criterion: {problem.max_fe} function evaluations")
    population = algorithm.run()
    pareto_front = get_final_pareto_front(population)
    print_pareto_front("Final Pareto front (makespan, energy):", pareto_front)
    _, _, gantt_path = record_best_makespan_gantt(problem, population)
    print(f"Gantt chart saved to: {gantt_path}")


if __name__ == "__main__":
    main()
