
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY missing in .env")

# Initialize Gemini
client = genai.Client(api_key=api_key)

# Read invoice file
invoice_text = Path("sample_invoice.txt").read_text(
    encoding="utf-8"
)

# Ask Gemini to extract structured JSON
prompt = f"""
Extract invoice information from the text below.

Return only valid JSON with these fields:
- invoice_number (string)
- customer (string)
- total_amount (number)
- currency (string)

Do not invent missing information.
Use null if a field is missing.

Invoice text:
{invoice_text}
"""

try:
    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=prompt
    )

    result = json.loads(response.output_text)

    print("\nExtracted Invoice JSON:")
    print(json.dumps(result, indent=4))

except json.JSONDecodeError:
    print("Gemini did not return valid JSON.")
    print(response.output_text)

except Exception as e:
    print(f"Error: {e}")
