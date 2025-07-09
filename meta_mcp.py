
import os
import csv
import requests # Added for API calls
import json # Added for JSON handling

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

def get_most_common_error(log_file_path):
    """Reads the log file and returns the most common error_output."""
    errors = []
    if not os.path.exists(log_file_path):
        return "No log file found."
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'error_output' in row:
                    errors.append(row['error_output'])
        
        if not errors:
            return "No errors recorded in log file."
        
        # Count occurrences of each error
        from collections import Counter
        error_counts = Counter(errors)
        
        # Return the most common error
        return error_counts.most_common(1)[0][0]
    except Exception as e:
        return f"Error reading log file: {e}"

# --- CONFIGURATION ---
LOG_FILE = "engine_log.csv"
GUIDELINES_DIR = "guidelines"

def get_file_content(filepath):
    """Helper function to read file content."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at {filepath}"

def call_ai_for_meta_task(prompt):
    """
    Calls the configured AI model for meta-tasks (e.g., improving guidelines).
    """
    print(f"--- Calling Meta-AI ({AI_MODEL_PROVIDER}) ---")
    print(f"Prompt (truncated): {prompt[:500]}...")
    try:
        # You can specify model_name and temperature here if needed,
        # otherwise, defaults from call_ai_api will be used.
        response_text = call_ai_api(AI_MODEL_PROVIDER, prompt)
        print("--- Meta-AI Response Received ---")
        return response_text
    except Exception as e:
        print(f"Error in call_ai_for_meta_task: {e}")
        # Return a default error message or re-raise, depending on desired behavior
        return "Error: Meta-AI model call failed. Check logs for details."


def analyze_and_improve():
    """Analyzes the log file and triggers a guideline improvement task."""
    if not os.path.exists(LOG_FILE):
        print(f"Error: Log file {LOG_FILE} not found. Run mcp.py first to generate logs.")
        return

    # 1. Read and analyze the log file to find the most common error
    # 1. Read and analyze the log file to find the most common error
    most_common_error = get_most_common_error(LOG_FILE)
    
    print(f"--- Analysis Complete ---")
    print("Found a recurring failure pattern.")

    # 2. Identify the relevant guideline to improve.
    # This is a simplified heuristic. A real system would need more complex logic.
    guideline_to_improve_path = os.path.join(GUIDELINES_DIR, "development_standards.md")
    print(f"Identified `{guideline_to_improve_path}` as the guideline to improve.")
    original_guideline = get_file_content(guideline_to_improve_path)

    # 3. Construct the meta-prompt
    prompt = (
        "You are a Meta-AI responsible for improving the performance of a developer AI. "
        "The developer AI is repeatedly failing on a task. Here is the most common error it produces:\n"
        f"```\n{most_common_error}\n```\n\n"
        f"This error seems related to the following guideline file: `{guideline_to_improve_path}`. "
        "Here is the current content of that guideline:\n"
        f"```markdown\n{original_guideline}\n```\n\n"
        "Please analyze the error and the guideline. Rewrite and provide the complete, improved guideline file. "
        "Your goal is to make the guideline clearer and more effective to prevent this error in the future. "
        "Do not add any commentary, just the full, updated markdown for the file."
    )

    # 4. Call the AI to get the improved guideline
    improved_guideline = call_ai_for_meta_task(prompt)

    # 5. Save the improved guideline
    print(f"\n> Meta-AI provided an improved guideline. Writing to {guideline_to_improve_path}")
    with open(guideline_to_improve_path, 'w', encoding='utf-8') as f:
        f.write(improved_guideline)
    
    print("\n--- Self-Improvement Complete ---")
    print(f"The guideline at {guideline_to_improve_path} has been updated.")
    print("Future runs of mcp.py will now use this improved rule.")

if __name__ == "__main__":
    analyze_and_improve()
