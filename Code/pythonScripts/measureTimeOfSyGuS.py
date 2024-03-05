import time
from Cvc5Runner import run_cvc5
import threading
import json
import pathlib

in_dir = ".\\..\\SyGuS-IF-Examples\\sequences\\"
out_dir = "pythonScripts\\temp\\measuringTiming\\"

# jobs = ["alter_array_content_only_at.sy", "alter_array_content_only_nth.sy"]
jobs = [
    "alter_array_index_only_at.sy",
    "alter_array_index_only_nth.sy",
    "alter_array_index_only_at_SLIA.sy",
    "alter_array_index_only_nth_SLIA.sy",
]
threads = []
measured_times = {}


def start_cvc5(input_file, outpuf_file):
    # print("start: ", input_file)
    start = time.time()
    run_cvc5(input_file, outpuf_file)
    end = time.time()
    # print("end: ", input_file)
    measured_times[input_file] = end - start


if __name__ == "__main__":

    json_file_path = out_dir + "measuredTimes.json"
    try:
        with open(json_file_path, "r") as json_file:
            measured_times = json.load(json_file)
    except FileNotFoundError:
        measured_times = {}

    print(pathlib.Path().resolve())
    for job in jobs:
        input_file = in_dir + job
        output_file = out_dir + "output_of_" + str(job) + ".log"
        thread = threading.Thread(target=start_cvc5, args=(input_file, output_file))
        threads.append(thread)

    # Start the threads (i.e. calculate the random number lists)
    for t in threads:
        t.start()

    # Ensure all of the threads have finished
    for t in threads:
        t.join()

    with open(json_file_path, "w") as json_file:
        json.dump(measured_times, json_file, indent=4)
