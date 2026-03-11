"""AI tool entry point."""

from openai import OpenAI


def main():
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "What is AI"}],
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
