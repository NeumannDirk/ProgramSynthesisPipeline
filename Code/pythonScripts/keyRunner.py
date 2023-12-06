import subprocess

def run_key(key_file, input_file, output_folder):
    java_command = [
        "java",
        "-jar",
        key_file,
        "--auto",
        "--openGoalsSmtPath",
        output_folder,
        input_file
    ]
    result = subprocess.run(java_command, stdout=subprocess.PIPE, text=True, shell=True)