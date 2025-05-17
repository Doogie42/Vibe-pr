import os

from google import genai
from dotenv import load_dotenv

from get_commitgit import get_diff
from models import PromptResponse
from printer import pretty_print_gpt


load_dotenv()

GOOGLE_KEY = os.getenv("API_KEY")


def get_ai_response(prompt: str) -> any:
    client = genai.Client(api_key=GOOGLE_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": PromptResponse,
        },
    )
    return response.parsed


def load_prompt(prompt_name, params=None):
    prompt = None
    with open(f"./prompt/{prompt_name}.txt") as f:
        prompt = f.read()
    return inject_param(prompt, params)


def inject_param(prompt, params=None):
    for key, value in params.items():
        prompt = prompt.replace("{{" + key + "}}", value)
    return prompt


def get_prompt(prompt_name: str, **kwargs) -> str:
    return load_prompt(prompt_name, params=kwargs)


def main():
    diff = get_diff()
    prompt = get_prompt("gpt", diff=diff)
    response_parsed = get_ai_response(prompt)
    response_parsed.issues.sort(key=lambda x: x.confidence, reverse=True)
    pretty_print_gpt(response_parsed)


if __name__ == "__main__":
    main()
