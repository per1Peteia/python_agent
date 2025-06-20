import os
from google.genai import types

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    abs_wd = os.path.abspath(working_directory)
    abs_target_file = os.path.abspath(
        os.path.join(working_directory, file_path))
    if not abs_target_file.startswith(abs_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:

        with open(abs_target_file, "r") as f:
            file_content = f.read(MAX_CHARS)
            if len(file_content) == MAX_CHARS:
                file_content += f'  [...File "{file_path}" truncated at 10000 characters]'
            return file_content
    except Exception as e:
        return f'Error reading file: {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)
