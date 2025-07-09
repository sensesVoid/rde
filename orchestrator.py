import subprocess
import sys
import os
import time
import shutil

def clear_project_folder():
    """Clears the contents of the PROJECT_DIR."""
    project_path = os.path.join(PROJECT_ROOT, PROJECT_DIR)
    if os.path.exists(project_path):
        print(f"\n--- Clearing project folder: {project_path} ---")
        try:
            # Remove all contents but keep the folder itself
            for item in os.listdir(project_path):
                item_path = os.path.join(project_path, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            # Recreate .gitkeep if it was removed
            gitkeep_path = os.path.join(project_path, ".gitkeep")
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write("")
            print("Project folder cleared successfully.")
        except Exception as e:
            print(f"Error clearing project folder: {e}")
    else:
        print(f"Project folder not found at {project_path}. Nothing to clear.")


def has_log_data(log_file_path):
    """Checks if the log file exists and contains data (more than just headers)."""
    if not os.path.exists(log_file_path):
        return False
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            # Read header line
            header = f.readline()
            # Check if there's a second line (data)
            if f.readline():
                return True
            else:
                return False # Only header or empty file
    except Exception:
        return False # Handle potential file reading errors

# --- CONFIGURATION ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MCP_SCRIPT = os.path.join(PROJECT_ROOT, "mcp.py")
META_MCP_SCRIPT = os.path.join(PROJECT_ROOT, "meta_mcp.py")
EXPORT_SCRIPT = os.path.join(PROJECT_ROOT, "export_project.py")
LOG_FILE = os.path.join(PROJECT_ROOT, "engine_log.csv")

def run_script(script_path, args=None, description=""):
    """Helper to run a Python script and capture its output."""
    command = [sys.executable, script_path]
    if args:
        command.extend(args)
    
    print(f"\n--- Running {description}: {' '.join(command)} ---")
    process = subprocess.run(command, capture_output=True, text=True, cwd=PROJECT_ROOT)
    
    print(f"Stdout:\n{process.stdout}")
    print(f"Stderr:\n{process.stderr}")
    
    if process.returncode != 0:
        print(f"Error: {description} failed with exit code {process.returncode}")
        return False, process.stdout + process.stderr
    print(f"{description} completed successfully.")
    return True, process.stdout + process.stderr

def import_project_to_engine(source_path):
    """Imports an existing project into the PROJECT_DIR."""
    project_path = os.path.join(PROJECT_ROOT, PROJECT_DIR)
    
    # Clear existing project folder first to ensure a clean import
    clear_project_folder() # Reuse the clear function

    print(f"\n--- Importing project from {source_path} to {project_path} ---")
    
    if source_path.startswith("http://") or source_path.startswith("https://") or source_path.endswith(".git"):
        # Assume it's a Git repository
        try:
            print(f"Cloning Git repository: {source_path}")
            subprocess.run(["git", "clone", source_path, project_path], check=True, capture_output=True)
            print("Git clone successful.")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning Git repository: {e.stderr.decode()}")
            return
    elif os.path.isdir(source_path):
        # Assume it's a local directory
        try:
            print(f"Copying local directory: {source_path}")
            # Copy contents, not the folder itself
            for item in os.path.listdir(source_path):
                s = os.path.join(source_path, item)
                d = os.path.join(project_path, item)
                if os.path.isfile(s):
                    shutil.copy2(s, d)
                elif os.path.isdir(s):
                    shutil.copytree(s, d)
            print("Local directory copied successfully.")
        except Exception as e:
            print(f"Error copying local directory: {e}")
            return
    else:
        print(f"Error: Source path '{source_path}' is not a valid Git URL or local directory.")
        return

    print("Project import complete.")
    print("You can now use the engine to analyze or improve this project.")

def orchestrate_development(prd_path, export_destination):
    """Orchestrates the full development process."""
    print(f"--- Starting Reflexive Development Engine Orchestration ---")
    print(f"PRD Path: {prd_path}")
    print(f"Export Destination: {export_destination}")

    # Phase 1: Initialization (AI generates PRP and initial code)
    # This part is implicitly handled by mcp.py's initial prompt if it's designed to take a PRD.
    # For now, mcp.py is designed to fix a bug, so we'll simulate the initial development.
    # A more advanced mcp.py would take the PRD and generate the initial project.
    print("\n--- Phase 1: Initial Development (via mcp.py) ---")
    # Assuming mcp.py's main_loop is called with a task that leads to initial code generation
    # For this example, we'll just run mcp.py which tries to fix a bug.
    # In a real scenario, mcp.py would be prompted with the PRD to start building.
    
    # Clear previous logs for a fresh run
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    mcp_success = False
    mcp_attempts = 0
    MAX_MCP_ATTEMPTS = 5 # Max attempts for mcp.py to succeed

    while not mcp_success and mcp_attempts < MAX_MCP_ATTEMPTS:
        mcp_attempts += 1
        print(f"\nAttempt {mcp_attempts} to run mcp.py...")
        # mcp.py currently has a hardcoded task. In a real system, this would be dynamic.
        task_to_perform = "Fix the bug in the `add` function in `project/main.py`." # This could be dynamic based on PRP
        success, output = run_script(MCP_SCRIPT, args=[task_to_perform], description="MCP (Main Control Program)")
        
        if success:
            mcp_success = True
            print("MCP completed successfully. Project should be ready.")
        else:
            print("MCP failed. Checking logs for self-improvement opportunity.")
            # Phase 2: Reflexion & Self-Improvement
            if has_log_data(LOG_FILE):
                print("\n--- Phase 2: Triggering Meta-MCP for Self-Improvement ---")
                meta_mcp_success, meta_mcp_output = run_script(META_MCP_SCRIPT, description="Meta-MCP (Guideline Improvement)")
                if meta_mcp_success:
                    print("Meta-MCP ran successfully. Retrying MCP.")
                else:
                    print("Meta-MCP failed. Continuing to retry MCP without guideline improvement.")
            else:
                print("No logs found for Meta-MCP. Retrying MCP directly.")
        
        time.sleep(2) # Small delay before retrying

    if not mcp_success:
        print("\n--- Orchestration Failed: MCP could not complete successfully after multiple attempts. ---")
        return False

    # Phase 3: Finalization (Export Project)
    print("\n--- Phase 3: Exporting Final Project ---")
    export_success, export_output = run_script(EXPORT_SCRIPT, args=[export_destination, "--force"], description="Project Export")
    
    if export_success:
        print("\n--- Reflexive Development Engine Orchestration Completed Successfully! ---")
        print(f"Project exported to: {export_destination}")
        return True
    else:
        print("\n--- Orchestration Failed: Project export failed. ---")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <command> [args...]")
        print("Commands:")
        print("  develop <path_to_prd.md> <export_destination_path>")
        print("  clear")
        sys.exit(1)

    command = sys.argv[1]

    if command == "develop":
        if len(sys.argv) != 3: # Changed from 4 to 3
            print("Usage: python orchestrator.py develop <export_destination_path>") # Removed <path_to_prd.md>
            sys.exit(1)
        
        # Hardcode prd_template.md as the PRD file
        prd_file = os.path.join(PROJECT_ROOT, "user_input", "prd_template.md")
        
        export_dest = sys.argv[2] # Changed from sys.argv[3] to sys.argv[2]
        
        if not os.path.exists(prd_file):
            print(f"Error: Default PRD file not found at {prd_file}") # Changed error message
            sys.exit(1)
        orchestrate_development(prd_file, export_dest)
    elif command == "clear":
        clear_project_folder()
    elif command == "import":
        if len(sys.argv) != 3:
            print("Usage: python orchestrator.py import <source_path>")
            print("  <source_path> can be a Git repository URL or a local directory path.")
            sys.exit(1)
        source_path = sys.argv[2]
        import_project_to_engine(source_path)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
