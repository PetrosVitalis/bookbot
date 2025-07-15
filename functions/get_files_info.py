def get_files_info(working_directory, directory=None):
    import os

    try:
        # Use working_directory if directory is None
        if directory is None:
            full_path = working_directory
            rel_dir = "."
        else:
            full_path = os.path.join(working_directory, directory)
            rel_dir = directory

        # Normalize and check if full_path is within working_directory
        working_directory = os.path.abspath(working_directory)
        full_path = os.path.abspath(full_path)
        if not full_path.startswith(working_directory):
            return f'Error: Cannot list "{rel_dir}" as it is outside the permitted working directory'

        # Check if full_path is a directory
        if not os.path.isdir(full_path):
            return f'Error: "{rel_dir}" is not a directory'

        entries = []
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)
            is_dir = os.path.isdir(entry_path)
            try:
                file_size = os.path.getsize(entry_path)
            except Exception as e:
                return f"Error: Could not get size for '{entry}': {e}"
            entries.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(entries)
    except Exception as e:
        return f"Error: {e}" 
    
from google.genai import types
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a file, constrained to the working directory. Truncates if file is too large.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the working directory and returns its output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites a file with the given content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)