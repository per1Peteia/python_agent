import os
import subprocess


def run_python_file(working_directory, file_path):
    abs_wd = os.path.abspath(working_directory)
    abs_target_path = os.path.abspath(
        os.path.join(working_directory, file_path))
    if not abs_target_path.startswith(abs_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_target_path):
        return f'Error: File "{file_path}" not found.'
    if not os.path.isfile(abs_target_path) or not abs_target_path.endswith(".py"):
        return f'Error: "{file_path}" is not a python file.'

    try:
        process = subprocess.run(
            ["python", os.path.join(working_directory, file_path)], timeout=30, capture_output=True
        )

        if process.returncode != 0:
            return f"STDOUT: {process.stdout} \nSTDERR: {process.stderr} \nProcess exited with code {process.returncode}"

        return f"STDOUT: {process.stdout} \nSTDERR: {process.stderr}\n"
    except Exception as e:
        f"Error: executing Python file: {e}"
