def main():
    import os
    from dotenv import load_dotenv

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    from google import genai

    client = genai.Client(api_key=api_key)
    
    res = client.models.generate_content(model="gemini-2.0-flash-001", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    print(res.text)

if __name__ == "__main__":
    main()