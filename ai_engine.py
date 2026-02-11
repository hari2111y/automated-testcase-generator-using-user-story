import pandas as pd
from huggingface_hub import InferenceClient
from io import StringIO

HF_TOKEN = "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"
client = InferenceClient(api_key=HF_TOKEN)


def build_prompt(user_story):
    return [
        {
            "role": "user",
            "content": f"""
Act as a QA Engineer.

Generate 12-15 test cases for:
{user_story}

Rules:
- Output STRICT CSV format.
- Columns exactly in this order: ID, Type, Description, Preconditions, Steps, Expected Result
- ID format: TC-001, TC-002, etc.
- Type values: Positive, Negative, Boundary, Validation, Exception, Security, Performance
- CRITICAL: Do NOT use newlines inside any cell. 
- For multiple steps, use numbered list in one line (e.g., "1. Login 2. Click button").
- Quote ALL text fields to ensure commas don't break the CSV.
- Return ONLY the CSV content, no other text or markdown.
"""
        }
    ]

def generate_testcases(user_story):
    response = client.chat_completion(
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        messages=build_prompt(user_story),
        max_tokens=1800
    )
    return response.choices[0].message.content

def convert_to_dataframe(raw_text):
    cleaned = raw_text.replace("```csv", "").replace("```", "").strip()
    
    import re
    header_pattern = r"ID\s*,\s*Type\s*,\s*Description"
    match = re.search(header_pattern, cleaned, re.IGNORECASE)
    
    if match:
        
        csv_text = cleaned[match.start():]
    else:
       
        csv_text = cleaned

    df = pd.read_csv(StringIO(csv_text), on_bad_lines="skip")

    df.columns = df.columns.str.strip()

    df["ID"] = df["ID"].ffill()
    df["Type"] = df["Type"].ffill()
    df["Description"] = df["Description"].ffill()

    df = df[["ID", "Type", "Description", "Preconditions", "Steps", "Expected Result"]]


    return df

