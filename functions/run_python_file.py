def run_python_file(working_directory, file_path):
    import os
    import subprocess
    try:
        # Join and normalize paths
        abs_working_directory = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Check if file_path is within working_directory
        if not abs_file_path.startswith(abs_working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        # Check if file exists
        if not os.path.exists(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        # Check if file is a Python file
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        try:
            result = subprocess.run(
                ["python", abs_file_path],
                cwd=abs_working_directory,
                capture_output=True,
                text=True,
                timeout=30
            )
        except subprocess.TimeoutExpired:
            return f"Error: executing Python file: Timed out after 30 seconds"
        except Exception as e:
            return f"Error: executing Python file: {e}"

        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout.strip()}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr.strip()}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not output:
            return "No output produced."
        return "\n".join(output)
    except Exception as e:
        return f"Error: {e}"