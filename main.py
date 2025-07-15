def main():
    import os
    from dotenv import load_dotenv
    import sys
    import argparse

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    from google import genai

    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt>")
        sys.exit(1)
    prompt = sys.argv[1]
    
    from google.genai import types

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]    
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    from functions.get_files_info import schema_get_files_info
    from functions.get_files_info import schema_get_file_content
    from functions.get_files_info import schema_run_python_file
    from functions.get_files_info import schema_write_file

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    from functions.get_files_info import get_files_info
    from functions.get_file_content import get_file_content
    from functions.run_python_file import run_python_file
    from functions.write_file import write_file

    def call_function(function_call_part, verbose=False):
        function_name = function_call_part.name
        args = dict(function_call_part.args)
        args["working_directory"] = "calculator"
        function_map = {
            "get_files_info": get_files_info,
            "get_file_content": get_file_content,
            "run_python_file": run_python_file,
            "write_file": write_file,
        }
        if verbose:
            print(f"Calling function: {function_name}({args})")
        else:
            print(f" - Calling function: {function_name}")
        if function_name not in function_map:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )
        try:
            function_result = function_map[function_name](**args)
        except Exception as e:
            function_result = f"Error: {e}"
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )

    res = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        )
    )
    
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
                
    # res = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
    # Print function call info if present, else print text
    if hasattr(res, "function_calls") and res.function_calls:
        for function_call_part in res.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            function_call_result = call_function(function_call_part, verbose=args.verbose)
            # Check for .parts[0].function_response.response
            try:
                response = function_call_result.parts[0].function_response.response
            except Exception:
                raise RuntimeError("Function call did not return a valid response.")
            if args.verbose:
                print(f"-> {response}")
    else:
        print(res.text)
    if args.verbose:
        print("User prompt: ", prompt)
        print("Prompt tokens: ", getattr(res.usage_metadata, 'prompt_token_count', 'N/A'))
        print("Response tokens: ", getattr(res.usage_metadata, 'candidates_token_count', 'N/A'))

if __name__ == "__main__":
    main()