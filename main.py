import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from tools.tool_list import available_functions

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_message, options = parse_commandline()

    conversation = [
        types.Content(role="user", parts=[types.Part(text=user_message)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=conversation,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        ),
    )

    if options['verbose']:
        print("User prompt:", user_message)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(response.text)
        sys.exit(0)

    if not response. function_calls:
        print(response.text)
    for call in response.function_calls:
        print(f"Calling function: {call.name}({call.args})")
    sys.exit(0)


def parse_commandline():
    try:
        user_message = sys.argv[1]
        options = {"verbose": False}

        if len(sys.argv) == 2:
            return user_message, options

        flags = sys.argv[2:]
        if "--verbose" in flags:
            options['verbose'] = True

        return (user_message, options)
    except IndexError as e:
        print('Usage: python main.py <"user message">')
        print(f'{e}')
        sys.exit(1)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)


if __name__ == "__main__":
    main()
