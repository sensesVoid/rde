# Reflexive Development Engine (RDE)

Welcome to the Reflexive Development Engine (RDE)! This framework is designed to help you collaborate with an AI assistant to build software projects efficiently. It provides a structured environment that ensures the AI is fully context-aware, autonomous, and aligned with your project's goals and constraints.

## How It Works

The Reflexive Development Engine (RDE) empowers an AI to act as a fully autonomous software engineer and orchestrator. Guided by the `system_prompt.md` (your primary directive), the AI interprets your **Product Requirements Document (PRD)** and drives the entire development lifecycle, from planning to code generation, testing, and self-improvement. This structured environment ensures the AI is context-aware, adheres to best practices, and continuously aligns with your project's goals.

A key aspect of the RDE's power is its ability to guide a single underlying AI model to adopt **multiple specialized roles or personas** throughout the development process. For instance, the AI acts as a "System Architect" when generating the initial plan, a "Developer AI" when writing code, and a "Meta-AI" when analyzing failures and improving its own guidelines. This specialization, driven by the engine's prompts and context, allows the AI to focus its capabilities for each specific task, leading to more effective and robust results.

The core automated workflow is:

1.  **Define**: You provide project requirements in `user_input/prd_template.md`.
2.  **Orchestrate**: The AI, following `system_prompt.md`, autonomously generates a **Prompt Engineering Plan (PRP)**, executes development tasks, and manages the project.
3.  **Develop**: The AI writes code, creates tests, and builds your application in the `project/` directory, adhering to all guidelines.
4.  **Persist**: The AI uses `persistency/` to maintain context, track tasks, and store learnings.

## Getting Started

1.  **Define Your Project**:
    -   Open `user_input/prd_template.md`.
    -   **Paste your Product Requirements Document (PRD) content directly into this file.**
    -   Save the file.

2.  **Initiate the Automated Process**:
    -   Use the `develop` command of `orchestrator.py` to start the development process. This script will autonomously manage the entire development lifecycle, guided by `system_prompt.md`. Your role shifts to oversight and feedback.

    ```bash
    python orchestrator.py develop C:/path/to/your/export/folder
    ```

## Folder Structure

-   **`orchestrator.py`**: The main entry point for initiating the fully automated development process.
-   **`system_prompt.md`**: The primary directive for the AI, outlining its role as orchestrator and the full automated workflow.
-   **`/examples/`**: Contains sample PRDs and the resulting code to show you what's possible.
-   **`/guidelines/`**: Supplementary rulebooks for the AI, providing specific coding standards, security practices, or communication styles. These are adhered to under the direction of `system_prompt.md`.
-   **`/initializer/`**: Holds the templates for generating the AI's master plan (the PRP).
-   **`/persistency/`**: The AI's memory.
    -   `task_list.md`: A checklist of tasks for the current project.
    -   `memory.md`: Stores long-term facts and decisions.
    -   `rag/`: A place to put documents for Retrieval-Augmented Generation, giving the AI deep knowledge on specific topics.
-   **`/project/`**: This is where your application's source code will be written by the AI.
-   **`/tools/`**: Defines how the AI can use external tools and orchestrate its own workflows (see `mcp_overview.md`).
-   **`/user_input/`**: Where you, the user, provide your primary input, most importantly the PRD.

This engine is a powerful tool for structured, AI-driven development. By investing a small amount of time in defining your requirements upfront, you can achieve a high degree of automation and quality in your projects.

## Orchestrator Commands

The `orchestrator.py` script provides the following commands to manage the development process:

### `python orchestrator.py develop <export_destination_path>`

-   **Purpose:** Initiates the full automated development lifecycle for a new project.
-   **Arguments:**
    -   `<export_destination_path>`: The desired path where the completed project will be exported.
-   **Note:** The Product Requirements Document (PRD) is automatically read from `user_input/prd_template.md`.

### `python orchestrator.py clear`

-   **Purpose:** Clears the contents of the `/project` directory. This is useful for starting a new development cycle or cleaning up after an export.

### `python orchestrator.py import <source_path>`

-   **Purpose:** Imports an existing project into the engine's `/project` directory for analysis, improvement, or further development.
-   **Arguments:**
    -   `<source_path>`: Can be a Git repository URL (e.g., `https://github.com/user/repo.git`) or a path to a local directory.
-   **Action:** This command will first clear the `/project` folder and then clone the Git repository or copy the local directory into it.

## AI Model Configuration

The Reflexive Development Engine can integrate with various AI models (Gemini, OpenAI, Claude, OpenRouter) via direct API calls. To configure which model the engine uses and to provide your API keys, you'll need to set **environment variables** before running the `orchestrator.py` script.

**1. Choose Your AI Model Provider:**

Set the `AI_MODEL_PROVIDER` environment variable to one of the following values (case-insensitive):

*   `gemini`
*   `openai`
*   `claude`
*   `openrouter`

**Example (before running `orchestrator.py`):**

*   **On Windows (Command Prompt):**
    ```cmd
    set AI_MODEL_PROVIDER=gemini
    ```
*   **On Windows (PowerShell):**
    ```powershell
    $env:AI_MODEL_PROVIDER="gemini"
    ```
*   **On macOS/Linux:**
    ```bash
    export AI_MODEL_PROVIDER="gemini"
    ```

**2. Set Your API Key(s):**

You need to set the API key for the provider you've chosen. Each provider has a specific environment variable name:

*   **Gemini:** `GEMINI_API_KEY`
*   **OpenAI:** `OPENAI_API_KEY`
*   **Claude:** `CLAUDE_API_KEY`
*   **OpenRouter:** `OPENROUTER_API_KEY`

**Example (setting a Gemini API key):**

*   **On Windows (Command Prompt):**
    ```cmd
    set GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
    ```
*   **On Windows (PowerShell):**
    ```powershell
    $env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```
*   **On macOS/Linux:**
    ```bash
    export GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
    ```

**Important Notes:**

*   **Security:** Always use environment variables for API keys. Never hardcode them directly into the Python scripts.
*   **Model Names:** Within the `call_ai_api` function in `mcp.py` and `meta_mcp.py`, there are default model names (e.g., `gemini-pro`, `gpt-3.5-turbo`). You can modify these defaults directly in the code if you wish to use a different model from a provider (e.g., `gpt-4o` for OpenAI).
*   **Temperature:** The `temperature` parameter (defaulting to 0.7) controls the randomness of the AI's output. You can adjust this in the `call_ai_api` function if you want more or less creative responses.
*   **OpenRouter Specifics:** If you use OpenRouter, remember to replace `"https://your-app-url.com"` and `"Your App Name"` in the `HTTP-Referer` and `X-Title` headers within the `call_ai_api` function with your actual application details.

## Exporting Your Project for Delivery

Once the AI has completed the project, you need a clean way to separate the final code from the engine itself. The `export_project.py` script is designed for this purpose.

### `python export_project.py <destination-path>`

-   **Purpose:** Exports the contents of the `/project` directory to a new, clean folder, ready for delivery to a client or for standalone version control.
-   **Action:**
    1.  Copies all files from the `/project` directory to the `<destination-path>`.
    2.  Initializes a new Git repository in the destination.
    3.  Creates an initial commit with all the project files.
-   **Example:**
    ```bash
    python export_project.py C:\Users\YourUser\Desktop\MyFinalApp
    ```
This command ensures your proprietary engine remains separate from the final, deliverable product.
