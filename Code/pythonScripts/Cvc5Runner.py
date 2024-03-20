import subprocess


def run_cvc5(input_file, output_file):
    java_command = ["cvc5.exe", "--incremental", input_file, ">", output_file]

    try:
        result = subprocess.run(java_command, shell=True, check=True)
        # Access result.returncode or other information if needed
        return result.returncode
    except subprocess.CalledProcessError as e:
        # Handle the case where the command returns a non-zero exit code
        print(f"Error: {e}")
        return e.returncode
