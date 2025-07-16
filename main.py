def main():
    import os
    from dotenv import load_dotenv
    import sys
    import argparse
    from google import genai
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    prompt = args.prompt

    from google.genai import types

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

    # Conversation loop
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    max_iterations = 20
    iteration = 0
    done = False
    while iteration < max_iterations and not done:
        try:
            res = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )
        except Exception as e:
            print(f"Error during LLM call: {e}")
            break

        # Add model response(s) to messages
        candidates = getattr(res, "candidates", None)
        if candidates:
            for candidate in candidates:
                if hasattr(candidate, "content"):
                    messages.append(candidate.content)

        # Handle function/tool calls
        function_calls = getattr(res, "function_calls", None)
        if function_calls:
            for function_call_part in function_calls:
                print(f" - Calling function: {function_call_part.name}")
                function_call_result = call_function(function_call_part, verbose=args.verbose)
                # Add tool response to messages
                messages.append(function_call_result)
                # Optionally print tool response if verbose
                if args.verbose:
                    try:
                        response = function_call_result.parts[0].function_response.response
                    except Exception:
                        response = None
                    if response is not None:
                        print(f"-> {response}")
        else:
            # No function calls - check if we have a final text response
            if hasattr(res, "text") and res.text:
                print("Final response:")
                print(res.text)
                done = True
                break
        iteration += 1
    if not done:
        print("Max iterations reached or no final response.")
    if args.verbose:
        print("User prompt: ", prompt)
        print("Prompt tokens: ", getattr(res.usage_metadata, 'prompt_token_count', 'N/A'))
        print("Response tokens: ", getattr(res.usage_metadata, 'candidates_token_count', 'N/A'))

if __name__ == "__main__":
    main()