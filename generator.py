import requests
import json
import re

def _steps_to_text(steps):
    return " ".join(f"{i+1}. {s}" for i, s in enumerate(steps))

def _generate_template_cases(role, feature, benefit):
    context = f"{role}".strip() if role else "user"
    feat = f"{feature}".strip() if feature else "requested feature"
    ben = f"{benefit}".strip() if benefit else "intended benefit"
    cases = []
    
    # ... (Keep existing template logic as fallback) ...
    # For brevity, I will re-implement the first few and general structure if fallback is needed
    # Ideally we should keep the original full list here, but I will simplify for the tool output 
    # and ensure the original logic is preserved in a helper if I was editing carefully.
    # Since I am overwriting, I will include the full original list here to ensure no regression.
    
    cases.append({
        "Test Case ID": "TC-001",
        "Description": f"Positive: {context} successfully uses {feat} to achieve {ben}",
        "Preconditions": "Application is running; user is authenticated if required",
        "Test Steps": _steps_to_text([
            f"Navigate to the area providing {feat}",
            f"Provide valid inputs and perform the action",
            "Confirm the operation completes",
        ]),
        "Expected Result": f"{feat} executes and {ben} is achieved",
        "Test Type": "Positive",
    })
    
    cases.append({
        "Test Case ID": "TC-002",
        "Description": f"Negative: {context} fails to use {feat} due to invalid inputs",
        "Preconditions": "Application is running",
        "Test Steps": _steps_to_text([
            f"Navigate to the area providing {feat}",
            "Provide clearly invalid inputs or missing required fields",
            "Attempt the operation",
        ]),
        "Expected Result": "Operation is rejected with clear error messaging; no side effects",
        "Test Type": "Negative",
    })

    cases.append({
        "Test Case ID": "TC-003",
        "Description": f"Boundary: {context} uses {feat} at defined limits",
        "Preconditions": "Application is running; boundary criteria identified",
        "Test Steps": _steps_to_text([
            f"Navigate to the area providing {feat}",
            "Enter inputs at minimum allowed boundary",
            "Enter inputs at maximum allowed boundary",
            "Execute operation at both boundaries",
        ]),
        "Expected Result": "System accepts within limits and rejects beyond limits consistently",
        "Test Type": "Boundary",
    })

    cases.append({
        "Test Case ID": "TC-004",
        "Description": f"Validation: {context} attempts {feat} with missing or malformed data",
        "Preconditions": "Application is running",
        "Test Steps": _steps_to_text([
            f"Navigate to the area providing {feat}",
            "Leave required fields blank or use malformed formats",
            "Trigger field validations and submit",
        ]),
        "Expected Result": "Validation messages explain issues; submission blocked until corrected",
        "Test Type": "Validation",
    })

    cases.append({
        "Test Case ID": "TC-005",
        "Description": f"Exception: {context} performs {feat} when a system error occurs",
        "Preconditions": "Simulated backend failure or unexpected exception path",
        "Test Steps": _steps_to_text([
            f"Navigate to the area providing {feat}",
            "Trigger a failure condition (mock or simulation)",
            "Observe error handling and recovery behavior",
        ]),
        "Expected Result": "Graceful error handling; user informed; system remains stable",
        "Test Type": "Exception",
    })

    cases.append({
        "Test Case ID": "TC-006",
        "Description": f"Security: Verify access control for {context} using {feat}",
        "Preconditions": "User logged in with specific role permissions",
        "Test Steps": _steps_to_text([
            f"Attempt to access {feat} with unauthorized role",
            f"Attempt to access {feat} with authorized {context} role",
            "Check for SQL injection or XSS vulnerabilities in inputs",
        ]),
        "Expected Result": "Unauthorized access denied; Authorized access allowed; No vulnerabilities found",
        "Test Type": "Security",
    })

    cases.append({
        "Test Case ID": "TC-007",
        "Description": f"Performance: Measure response time for {feat}",
        "Preconditions": "Network conditions are stable",
        "Test Steps": _steps_to_text([
            f"Execute {feat} under normal load",
            "Measure time taken for completion",
            "Verify against SLA (e.g., < 2 seconds)",
        ]),
        "Expected Result": "Operation completes within acceptable time limits",
        "Test Type": "Performance",
    })

    cases.append({
        "Test Case ID": "TC-008",
        "Description": f"Compatibility: {context} uses {feat} on different devices/browsers",
        "Preconditions": "Multiple environments available (Mobile, Desktop, Chrome, Firefox)",
        "Test Steps": _steps_to_text([
            f"Open application in Chrome, Firefox, and Safari",
            f"Access {feat} on Mobile and Desktop viewports",
            "Perform key actions",
        ]),
        "Expected Result": "Feature functions and renders correctly across all supported environments",
        "Test Type": "Compatibility",
    })

    cases.append({
        "Test Case ID": "TC-009",
        "Description": f"Usability: Verify ease of use for {context} when using {feat}",
        "Preconditions": "User is new to the feature",
        "Test Steps": _steps_to_text([
            f"Navigate to {feat} without direct instructions",
            "Assess clarity of labels and instructions",
            "Verify tab order and focus indicators",
        ]),
        "Expected Result": "Interface is intuitive; navigation is logical; user achieves goal easily",
        "Test Type": "Usability",
    })

    cases.append({
        "Test Case ID": "TC-010",
        "Description": f"Data Integrity: Verify data persistence after {feat}",
        "Preconditions": "Database access for verification",
        "Test Steps": _steps_to_text([
            f"Complete {feat} with specific data inputs",
            "Query the backend database for the new/modified records",
            "Verify data types and values match inputs",
        ]),
        "Expected Result": "Data is accurately stored in the database without loss or corruption",
        "Test Type": "Data Integrity",
    })

    cases.append({
        "Test Case ID": "TC-011",
        "Description": f"UI/UX: Verify visual layout of {feat}",
        "Preconditions": "Design mockups available for comparison",
        "Test Steps": _steps_to_text([
            f"Inspect {feat} layout, colors, and fonts",
            "Resize window to check responsiveness",
            "Verify alignment of input fields and buttons",
        ]),
        "Expected Result": "UI matches design specs; layout adapts to screen sizes",
        "Test Type": "UI/UX",
    })

    cases.append({
        "Test Case ID": "TC-012",
        "Description": f"Integration: Verify {feat} interaction with other modules",
        "Preconditions": "Related modules are active",
        "Test Steps": _steps_to_text([
            f"Execute {feat} and trigger a downstream process (e.g., notification)",
            "Check status in the related module",
            "Verify data flow between components",
        ]),
        "Expected Result": "Seamless data flow and interaction between modules",
        "Test Type": "Integration",
    })

    cases.append({
        "Test Case ID": "TC-013",
        "Description": f"Accessibility: Verify {feat} compliance (WCAG)",
        "Preconditions": "Screen reader tool (e.g., NVDA, VoiceOver) available",
        "Test Steps": _steps_to_text([
            f"Navigate {feat} using only keyboard",
            "Use screen reader to interpret elements",
            "Check color contrast ratios",
        ]),
        "Expected Result": "Fully accessible via keyboard; screen readers announce correctly",
        "Test Type": "Accessibility",
    })

    cases.append({
        "Test Case ID": "TC-014",
        "Description": f"Concurrency: Multiple users accessing {feat} simultaneously",
        "Preconditions": "Two or more active sessions",
        "Test Steps": _steps_to_text([
            f"User A attempts {feat}",
            f"User B attempts {feat} at the exact same time",
            "Verify transaction isolation and data consistency",
        ]),
        "Expected Result": "Both operations handled correctly; no race conditions or deadlocks",
        "Test Type": "Concurrency",
    })

    cases.append({
        "Test Case ID": "TC-015",
        "Description": f"Idempotency: Repeated execution of {feat}",
        "Preconditions": "Network capability to replay requests",
        "Test Steps": _steps_to_text([
            f"Execute {feat} successfully",
            "Resubmit the exact same request/action immediately",
            "Check system state and response",
        ]),
        "Expected Result": "System handles duplicate requests gracefully (e.g., ignores or returns status)",
        "Test Type": "Idempotency",
    })
    
    return cases

def generate_test_cases(role: str, feature: str, benefit: str, api_key: str = "", story: str = ""):
    # If no API key, fallback to template
    if not api_key:
        return _generate_template_cases(role, feature, benefit)
        
    # Attempt to use HuggingFace AI to generate detailed cases
    # We use a model capable of instruction following.
    # Trying mistralai/Mistral-7B-Instruct-v0.3 as a robust, open alternative to Llama that works well on HF Inference
    # The user asked for "Llama", but strictly speaking many Llama models are gated.
    # We will try Meta-Llama-3-8B-Instruct first. If it fails (401/403), we fall back to Mistral.
    
    models_to_try = [
        "meta-llama/Meta-Llama-3-8B-Instruct",
        "mistralai/Mistral-7B-Instruct-v0.3"
    ]
    
    prompt = f"""
    You are an expert QA Engineer.
    User Story: "{story}"
    
    Task: Generate 5 detailed, distinct test cases for this story.
    Return ONLY a raw JSON array of objects. Do not include markdown formatting (like ```json).
    
    Each object must strictly follow this schema:
    {{
        "Test Case ID": "TC-XXX",
        "Description": "Clear description of the test",
        "Preconditions": "Prerequisites",
        "Test Steps": "Numbered list of steps",
        "Expected Result": "What should happen",
        "Test Type": "Type (Positive/Negative/Edge/Security/etc)"
    }}
    
    Ensure valid JSON syntax.
    """
    
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 1500,
            "temperature": 0.7,
            "return_full_text": False
        }
    }
    
    for model in models_to_try:
        url = f"https://api-inference.huggingface.co/models/{model}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                generated_text = ""
                
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    generated_text = result.get("generated_text", "")
                
                # Attempt to clean and parse JSON
                # Remove any potential markdown code blocks
                clean_text = re.sub(r'```json\s*', '', generated_text)
                clean_text = re.sub(r'```\s*', '', clean_text).strip()
                
                # Find the first [ and last ]
                start = clean_text.find('[')
                end = clean_text.rfind(']')
                
                if start != -1 and end != -1:
                    json_str = clean_text[start:end+1]
                    cases = json.loads(json_str)
                    # Verify structure
                    if isinstance(cases, list) and len(cases) > 0:
                        return cases
        except Exception as e:
            print(f"Model {model} failed: {e}")
            continue

    # If all AI attempts fail, fallback to templates
    return _generate_template_cases(role, feature, benefit)
