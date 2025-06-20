from google.genai import types
from tools.get_files_info import schema_get_files_info
from tools.get_file_content import schema_get_file_content
from tools.write_file import schema_write_file
from tools.run_python import schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ]
)
