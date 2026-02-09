import re
import requests
import json

def _parse_fallback(story: str):
    """
    Attempts to parse the story using regex for standard format.
    If that fails, uses heuristics to infer components from unstructured text.
    """
    story = story.strip()
    
    # 1. Try standard "As a... I want... So that..." format
    pattern = re.compile(
        r"As a\s+(?P<role>.*?),\s*I want\s+(?:to\s+)?(?P<feature>.*?)\s+so that\s+(?P<benefit>.*?)[\.\n]*$",
        re.IGNORECASE | re.DOTALL,
    )
    match = pattern.search(story)
    if match:
        return {
            "role": match.group("role").strip(),
            "feature": match.group("feature").strip(),
            "benefit": match.group("benefit").strip()
        }

    # 2. Heuristic fallback for unstructured input
    # If the input is short (likely just a feature name), assume generic role/benefit
    role = "User"
    feature = story
    benefit = "achieve the desired goal"
    
    # Simple heuristic: "I want to <feature>"
    want_pattern = re.search(r"I want (?:to )?(.*)", story, re.IGNORECASE)
    if want_pattern:
        feature = want_pattern.group(1).strip()
    
    return {"role": role, "feature": feature, "benefit": benefit}


def extract_story_components(story: str, api_key: str):
    if not api_key:
        return _parse_fallback(story)
        
    # Use a smarter model capable of inference (consistent with generator.py)
    models_to_try = [
        "mistralai/Mistral-7B-Instruct-v0.3",
        "google/flan-t5-base" # Fallback to faster/smaller model
    ]
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Prompt optimized for inference
    prompt = (
        f"Analyze this user requirement: \"{story}\"\n"
        "Extract or infer the Role, Feature, and Benefit.\n"
        "If they are not explicitly stated, make a logical guess.\n"
        "Return ONLY a JSON object with keys: 'role', 'feature', 'benefit'.\n"
        "Example output: {\"role\": \"User\", \"feature\": \"Login\", \"benefit\": \"Access account\"}"
    )
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 200,
            "return_full_text": False,
            "temperature": 0.1 # Low temperature for consistent formatting
        }
    }

    for model in models_to_try:
        url = f"https://api-inference.huggingface.co/models/{model}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
            if resp.status_code != 200:
                continue
                
            data = resp.json()
            text = ""
            
            # Handle different response formats from HF Inference API
            if isinstance(data, list) and data and "generated_text" in data[0]:
                text = data[0]["generated_text"]
            elif isinstance(data, dict) and "generated_text" in data:
                text = data["generated_text"]
            else:
                continue
                
            # Attempt to find and parse JSON in the response
            # Mistral might wrap in ```json ... ```
            json_match = re.search(r"\{.*\}", text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                components = json.loads(json_str)
                
                # Validate keys exist
                if all(k in components for k in ["role", "feature", "benefit"]):
                    return {
                        "role": components["role"],
                        "feature": components["feature"],
                        "benefit": components["benefit"]
                    }
            
            # If JSON parsing failed, try simple line parsing (backup for Flan-T5)
            # Flan-T5 often returns plain text like "Role: ... Feature: ..."
            role = ""
            feature = ""
            benefit = ""
            
            lines = text.split('\n')
            for line in lines:
                if "role" in line.lower() and ":" in line:
                    role = line.split(":", 1)[1].strip().strip('",')
                elif "feature" in line.lower() and ":" in line:
                    feature = line.split(":", 1)[1].strip().strip('",')
                elif "benefit" in line.lower() and ":" in line:
                    benefit = line.split(":", 1)[1].strip().strip('",')
            
            if role and feature: # Benefit is optional-ish
                 return {"role": role, "feature": feature, "benefit": benefit or "unknown benefit"}

        except Exception as e:
            print(f"Extraction model {model} failed: {e}")
            continue

    # If all AI attempts fail, fallback to heuristic regex
    return _parse_fallback(story)
