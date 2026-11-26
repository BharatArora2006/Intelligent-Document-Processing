import os
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq


# Load environment variables from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GROQ_API_KEY")

model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env file.")

client = Groq(api_key=api_key)

try:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: Groq connection successful."
            }
        ]
    )

    print("Groq connection successful!")
    print("Model:", model)
    print("Response:", response.choices[0].message.content)

except Exception as error:
    print("Groq connection failed.")
    print("Error:", error)