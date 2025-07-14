def main():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    from google import genai

    client = genai.Client(api_key=api_key)
    
    res = client.models.generate_content(model="gemini-2.0-flash-001", contents="Does the rise of AI make it a bad idea to become developer? One paragraph.")
    print(res.text)
    print("Prompt tokens: ", res.usage_metadata.prompt_token_count)
    print("Response tokens: ", res.usage_metadata.candidates_token_count)

if __name__ == "__main__":
    main()