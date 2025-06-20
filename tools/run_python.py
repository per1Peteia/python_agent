import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path, args=None):
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
        commands = ["python", abs_target_path]
        if args:
            commands.extend(args)
        process = subprocess.run(
            commands, timeout=30, capture_output=True, text=True, cwd=abs_wd
        )

        if process.returncode != 0:
            return f"STDOUT:\n{process.stdout}\nSTDERR: {process.stderr} \nProcess exited with code {process.returncode}"

        return f"STDOUT:\n{process.stdout}\nSTDERR:\n{process.stderr}\n"
    except Exception as e:
        f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
