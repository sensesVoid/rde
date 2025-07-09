import os
import subprocess
import sys
import csv
from datetime import datetime
import requests # Added for API calls
import json # Added for JSON handling

# --- CONFIGURATION ---
MAX_RETRIES = 3
PROJECT_DIR = "project"
GUIDELINES_DIR = "guidelines"
LOG_FILE = "engine_log.csv"

# --- AI MODEL CONFIGURATION ---
# Set your desired AI model provider here: "gemini", "openai", "claude", "openrouter"
AI_MODEL_PROVIDER = os.environ.get("AI_MODEL_PROVIDER", "gemini").lower()

# API Keys (read from environment variables for security)
# Ensure these environment variables are set before running the engine
API_KEYS = {
    "gemini": os.environ.get("GEMINI_API_KEY"),
    "openai": os.environ.get("OPENAI_API_KEY"),
    "claude": os.environ.get("CLAUDE_API_KEY"),
    "openrouter": os.environ.get("OPENROUTER_API_KEY"),
}

# --- GENERIC AI API CALLER ---
def call_ai_api(provider, prompt, model_name=None, temperature=0.7):
    """Makes a generic API call to the specified AI provider."""
    api_key = API_KEYS.get(provider)
    if not api_key:
        raise ValueError(f"API key for {provider} not found. Please set the corresponding environment variable.")

    headers = {
        "Content-Type": "application/json",
    }
    payload = {}
    url = ""
    text_extraction_path = [] # Path to extract text from JSON response

    if provider == "gemini":
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name or 'gemini-pro'}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature
            }
        }
        text_extraction_path = ["candidates", 0, "content", "parts", 0, "text"]
    elif provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        payload = {
            "model": model_name or "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        text_extraction_path = ["choices", 0, "message", "content"]
    elif provider == "claude":
        # Anthropic (Claude) API
        url = "https://api.anthropic.com/v1/messages"
        headers["x-api-key"] = api_key
        headers["anthropic-version"] = "2023-06-01" # Required for Anthropic
        headers["Content-Type"] = "application/json"
        payload = {
            "model": model_name or "claude-3-opus-20240229",
            "max_tokens": 4000, # Claude requires max_tokens
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        text_extraction_path = ["content", 0, "text"]
    elif provider == "openrouter":
        # OpenRouter API (can route to many models)
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers["Authorization"] = f"Bearer {api_key}"
        headers["HTTP-Referer"] = "https://your-app-url.com" # Replace with your app URL
        headers["X-Title"] = "Your App Name" # Replace with your app name
        payload = {
            "model": model_name or "mistralai/mistral-7b-instruct", # Example OpenRouter model
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        text_extraction_path = ["choices", 0, "message", "content"]
    else:
        raise ValueError(f"Unsupported AI model provider: {provider}")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        
        response_json = response.json()
        
        # Extract text based on provider-specific path
        text = response_json
        for key in text_extraction_path:
            if isinstance(text, list) and isinstance(key, int):
                text = text[key]
            elif isinstance(text, dict) and isinstance(key, str):
                text = text.get(key)
            else:
                raise KeyError(f"Invalid path for text extraction: {key} in {text_extraction_path}")
        
        return text

    except requests.exceptions.RequestException as e:
        print(f"Network or HTTP error during API call to {provider}: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"JSON decoding error from {provider} response: {e}")
        print(f"Response content: {response.text}")
        raise
    except KeyError as e:
        print(f"Could not extract text from {provider} response. Path error: {e}")
        print(f"Response JSON: {response_json}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during API call to {provider}: {e}")
        raise

def get_file_content(filepath):
    """Helper function to read file content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at {filepath}"

def log_failure(task, attempt, error_output):
    """Logs a verification failure to the CSV log file."""
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "task", "attempt", "error_output"])
    
    with open(LOG_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), task, attempt, error_output])

def call_ai(prompt):
    """
    Calls the configured AI model to generate a response.
    """
    print(f"--- Calling AI ({AI_MODEL_PROVIDER}) ---")
    print(f"Prompt (truncated): {prompt[:500]}...")
    try:
        # You can specify model_name and temperature here if needed,
        # otherwise, defaults from call_ai_api will be used.
        response_text = call_ai_api(AI_MODEL_PROVIDER, prompt)
        print("--- AI Response Received ---")
        return response_text
    except Exception as e:
        print(f"Error in call_ai: {e}")
        # Return a default error message or re-raise, depending on desired behavior
        return "Error: AI model call failed. Check logs for details."


def run_verification():
    """
    Runs the verification command (pytest) and returns the result.
    """
    command = [sys.executable, "-m", "pytest", PROJECT_DIR]
    print(f"\n> Running verification: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    return result

def main_loop(task_description):
    """
    The main self-healing loop.
    """
    SYSTEM_PROMPT_FILE = "system_prompt.md"

    context = "You are an autonomous AI software engineer. Your task is to fix a bug in the following project.\n"

    # Load the system prompt first
    system_prompt_path = os.path.join(os.getcwd(), SYSTEM_PROMPT_FILE)
    context += f"\n--- System Prompt: {SYSTEM_PROMPT_FILE} ---\n"
    context += get_file_content(system_prompt_path)

    # Then load other guidelines
    for guideline_file in os.listdir(GUIDELINES_DIR):
        # Ensure we don't try to load system_prompt.md again if it was somehow left in guidelines
        if guideline_file == SYSTEM_PROMPT_FILE:
            continue
        context += f"\n--- Guideline: {guideline_file} ---\n"
        context += get_file_content(os.path.join(GUIDELINES_DIR, guideline_file))
    
    file_to_fix_path = os.path.join(PROJECT_DIR, "main.py")
    code_to_fix = get_file_content(file_to_fix_path)

    initial_verification = run_verification()
    error_output = initial_verification.stdout + "\n" + initial_verification.stderr
    if initial_verification.returncode != 0:
        log_failure(task_description, 0, error_output)

    for i in range(MAX_RETRIES):
        verification_result = run_verification()
        if verification_result.returncode == 0:
            print("\n--- Verification Succeeded! ---")
            print("The code has been successfully fixed by the AI.")
            return

        print(f"\n--- Attempt {i + 1} of {MAX_RETRIES} ---")
        
        prompt = (
            f"{context}\n"
            f"The task is: {task_description}\n\n"
            f"The file `{file_to_fix_path}` currently contains this code:\n"
            f"```python\n{code_to_fix}\n```\n\n"
            f"When I run the tests, I get this error:\n"
            f"```\n{error_output}\n```\n\n"
            "Please analyze the error and provide the complete, corrected code for the file. "
            "Do not add any commentary or apologies, just the full code."
        )

        corrected_code = call_ai(prompt)
        
        print(f"\n> AI provided a fix. Writing to {file_to_fix_path}")
        with open(file_to_fix_path, 'w', encoding='utf-8') as f:
            if corrected_code.strip().startswith("```python"):
                corrected_code = corrected_code.strip()[9:-3].strip()
            f.write(corrected_code)

        error_output = verification_result.stdout + "\n" + verification_result.stderr
        log_failure(task_description, i + 1, error_output)
        code_to_fix = corrected_code

    print(f"\n--- Max Retries Reached ({MAX_RETRIES}) ---")
    print("The AI was unable to fix the code within the maximum number of attempts.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        task = sys.argv[1]
    else:
        task = "Fix the bug in the `add` function in `project/main.py`." # Default task
    main_loop(task)