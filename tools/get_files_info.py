import os


def get_files_info(working_directory, directory=None):
    cwd_abs = os.path.abspath(working_directory)
    if directory:
        dir_abs = os.path.abspath(os.path.join(working_directory, directory))
    if not dir_abs.startswith(cwd_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(dir_abs):
        f'Error: "{directory}" is not a directory'

    try:
        result = []
        entries = os.listdir(dir_abs)
        for name in entries:
            path = os.path.join(dir_abs, name)
            result.append(
                f'{name}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}'
            )

        return '\n'.join(result)
    except Exception as e:
        return f'Error: {e}'
