import os
import shutil
import subprocess
import sys

# --- CONFIGURATION ---
PROJECT_SOURCE_DIR = "project"

def export_project(destination_path, force_overwrite=False):
    """Copies the project to a new directory and initializes a git repository."""
    # 1. Validate the source directory exists
    if not os.path.isdir(PROJECT_SOURCE_DIR):
        print(f"Error: Source directory '{PROJECT_SOURCE_DIR}' not found.")
        return

    # 2. Handle the destination directory
    if os.path.exists(destination_path):
        if force_overwrite:
            print(f"Warning: Destination '{destination_path}' already exists. Forcing overwrite.")
            shutil.rmtree(destination_path)
        else:
            response = input(f"Warning: Destination '{destination_path}' already exists. Overwrite? (y/n): ").lower()
            if response != 'y':
                print("Export cancelled.")
                return
            shutil.rmtree(destination_path)
    
    print(f"\n> Exporting project to {destination_path}...")
    
    # 3. Copy the project files, ignoring common temporary files
    # Define patterns for files to ignore during copy
    ignore_patterns = shutil.ignore_patterns(
        '__pycache__', '*.pyc',
        '.gitkeep', 'main.py', 'requirements.txt', 'test_main.py' # Add default project files to ignore
    )
    shutil.copytree(PROJECT_SOURCE_DIR, destination_path, ignore=ignore_patterns)

    print("> Project files copied successfully.")

    # 4. Initialize a new Git repository in the destination
    try:
        print(f"> Initializing new Git repository in {destination_path}...")
        subprocess.run(["git", "init"], cwd=destination_path, check=True, capture_output=True)
        
        # 5. Create the initial commit
        print("> Creating initial commit...")
        # It's important to configure user.name and user.email for this to work
        # We will stage all files and commit them
        subprocess.run(["git", "add", "."], cwd=destination_path, check=True, capture_output=True)
        commit_message = "Initial commit: Project exported from engine."
        subprocess.run(["git", "commit", "-m", commit_message], cwd=destination_path, check=True, capture_output=True)

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print("\n--- Git Initialization Failed ---")
        print("Could not initialize git. Please ensure git is installed and in your PATH.")
        print(f"Error: {e}")
        print("The project files were copied, but you will need to handle git manually.")
        return

    print("\n--- Export Complete! ---")
    print(f"Your clean project is ready at: {destination_path}")
    print("\nNext steps:")
    print(f"  1. cd {destination_path}")
    print("  2. git remote add origin <your-client-repo-url>")
    print("  3. git push -u origin master")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python export_project.py <path_to_clean_project_directory> [--force]")
        sys.exit(1)
    
    destination = sys.argv[1]
    force = False
    if len(sys.argv) == 3 and sys.argv[2] == "--force":
        force = True
    
    export_project(destination, force_overwrite=force)
