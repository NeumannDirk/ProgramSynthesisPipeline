import os
import numpy as np


def eval_timing(info):
    step_timings = {
        "setup": [],
        "split": [],
        "key_pre": [],
        "key_post": [],
        "smt_pre": [],
        "smt_post": [],
        "read_vars": [],
        "gen_sygus": [],
        "start_synth": [],
        "end_synth": [],
        "java": [],
        "total": [],
    }

    total_times = []

    projectFolder = info["src_dir"] + "prove" + info["project"]
    statement = info["statement_file"]

    for i in range(10):
        input_file_path = os.path.join(
            projectFolder, "temp_" + statement + f"_{i}\\times.txt"
        )

        with open(input_file_path, "r") as file:
            lines = file.readlines()
            relative_times = eval(lines[2])

            for step, timing in zip(step_timings.keys(), relative_times):
                step_timings[step].append(timing)
        total_time = sum(relative_times)
        total_times.append(total_time)
        step_timings["total"].append(total_time)

    step_statistics = {}
    for step, timings in step_timings.items():
        avg_time = np.mean(timings)
        stddev_time = np.std(timings)
        step_statistics[step] = (avg_time, stddev_time)

    mean_total_time = round(np.mean(total_times), 1)
    stddev_total_time = round(np.std(total_times), 1)

    output_file_path = os.path.join(projectFolder, f"timing_results_{statement}.txt")
    with open(output_file_path, "w") as output:
        for step, stats in step_statistics.items():
            avg_time, stddev_time = stats
            output.write(f"{step}: ${avg_time:.1f} \\pm {stddev_time:.1f}$ \n")
        output.write(f"total: ${mean_total_time:.1f} \\pm {stddev_total_time:.1f}$ \n")
