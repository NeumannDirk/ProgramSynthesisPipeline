import os
import re
from pprint import pprint
from tqdm import tqdm
from exeSygusPipeLine import execute_sygus_pipeline


def main():
    src_dir = "D:\\evalData_noPredicates\\diagrams\\"
    projectsToEvaluate = [
        # "maxElement",
        # "LinearSearch",
        "DutchFlag",
        # "Exponentation",
        # "FactorialGraphical",
        # "Logarithm",
    ]
    task_dict = collect_files_for_evaluation(
        src_dir=src_dir, projectsToEvaluate=projectsToEvaluate
    )
    for id, val in task_dict.items():
        # print("id: ", id)
        # print("file: ", val["statement_path"])
        # print("modi: ", val["modifiable"])
        # print("")
        # pprint(val)
        execute_sygus_pipeline(val)
        pass

    pass
    # print("Task-Dict:")
    # pprint(task_dict)


def collect_files_for_evaluation(src_dir, projectsToEvaluate):
    task_dict = {}
    task_id = 1
    for s in projectsToEvaluate:
        folder_path = src_dir + "prove" + s + "\\"
        cbcmodel_full_path = src_dir + s + ".cbcmodel"
        if not os.path.isfile(cbcmodel_full_path):
            print("Error: ", cbcmodel_full_path)

        for statement_filename in os.listdir(folder_path):
            statement_full_path = os.path.join(folder_path, statement_filename)
            if os.path.isfile(statement_full_path) and isStatementFile(
                statement_filename
            ):
                cbc_id = get_id_from_key_file(full_path=statement_full_path)
                modifiable_list = get_modifiable_from_key_file(
                    full_path=statement_full_path
                )
                if cbc_id is None:
                    print("Error: No cbc_id for file ", statement_full_path)
                if modifiable_list is None:
                    print("Error: No modifiable for file ", statement_full_path)

                task_dict[task_id] = {
                    "src_dir": src_dir,
                    "project": s,
                    "statement_file": statement_filename.split(".")[0],
                    "statement_path": statement_full_path,
                    "cbcmodel_path": cbcmodel_full_path,
                    "cbc_id": cbc_id,
                    "modifiable": modifiable_list,
                    "result": None,
                    "timestamps": [],
                }
                task_id += 1

            else:
                # print("No Statement: ", f)
                pass
    # print("Task-Dict:")
    # pprint(task_dict)
    return task_dict


def get_id_from_key_file(full_path: str) -> str:
    with open(full_path, "r") as file:
        file_content = file.read()
        pattern = r"//statementid:\{([0-9a-fA-F-]+)\}"
        match = re.search(pattern, file_content)
        if match:
            # print("Found Statement ID:", statement_id)
            return match.group(1)
        else:
            # print("Statement ID not found in the file.")
            pass


def get_modifiable_from_key_file(full_path: str) -> str:
    with open(full_path, "r") as file:
        file_content = file.read()
        pattern = r"//modifiable:\{([0-9a-zA-Z-,]+)\}"
        pattern = r"\/\/modifiable:\s*\{([^}]*)\}"
        match = re.search(pattern, file_content)
        if match:
            # print("Found Statement ID:", statement_id)
            return [x.strip() for x in match.group(1).split(",")]
        else:
            # print("Statement ID not found in the file.")
            pass


def isStatementFile(filename: str) -> bool:
    pattern = r"^Statement\d+\.key$"
    return re.match(pattern, filename) is not None


if __name__ == "__main__":
    # print(os.getcwd())
    main()
