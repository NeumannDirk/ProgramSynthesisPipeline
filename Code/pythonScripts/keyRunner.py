import subprocess


def run_key(key_file, input_file, output_folder):
    java_command = [
        "java",
        "-jar",
        key_file,
        "--auto",
        "--openGoalsSmtPath",
        output_folder,
        input_file,
    ]
    print(" ".join(java_command))
    try:
        result = subprocess.run(java_command, shell=True, check=True)
        # Access result.returncode or other information if needed
        return result.returncode
    except subprocess.CalledProcessError as e:
        # Handle the case where the command returns a non-zero exit code
        print(f"Error: {e}")
        return e.returncode
