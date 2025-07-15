def get_file_content(working_directory, file_path):
    import os
    try:
        # Join and normalize paths
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if file_path is within working_directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if file_path is a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Import MAX_CHARS from config.py
        try:
            from functions.config import MAX_CHARS
        except ImportError:
            MAX_CHARS = 10000

        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS + 1)
        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return content
    except Exception as e:
        return f"Error: {e}"