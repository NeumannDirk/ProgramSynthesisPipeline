import subprocess

def run_cvc5(input_file, output_file):    
    java_command = ["cvc5.exe", "--incremental", input_file, ">", output_file]
    subprocess.run(java_command, shell=True)