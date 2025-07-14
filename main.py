def main():
    import os
    from dotenv import load_dotenv
    import sys

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    from google import genai

    client = genai.Client(api_key=api_key)
    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt>")
        sys.exit(1)
    prompt = sys.argv[1]
    
    
    res = client.models.generate_content(model="gemini-2.0-flash-001", contents=prompt)
    print(res.text)
    print("Prompt tokens: ", res.usage_metadata.prompt_token_count)
    print("Response tokens: ", res.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()