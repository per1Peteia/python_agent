import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    try:
        user_message = sys.argv[1]
    except IndexError:
        print('Usage: python main.py <"user message">')
        sys.exit(1)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)

    conversation = [
        types.Content(role="user", parts=[types.Part(text=user_message)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=conversation
    )

    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
