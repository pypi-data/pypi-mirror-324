import argparse
import shutil
import os
from pathlib import Path

# Define the template files in the package
TEMPLATE_FILES = {
    "examples.py": "examples.py",
    ".env": ".example.env"  # The source filename inside the package
}

def copy_template(file_name, destination_dir):
    """Copies a template file from the package directory to the specified destination."""
    package_dir = Path(__file__).parent  # Get package directory
    source_file = package_dir / TEMPLATE_FILES.get(file_name)

    if not source_file.exists():
        print(f"Error: Template '{file_name}' does not exist in the package.")
        return

    destination_path = Path(destination_dir) / file_name

    try:
        shutil.copy(source_file, destination_path)
        print(f"Successfully copied '{file_name}' to '{destination_path}'.")
    except Exception as e:
        print(f"Error copying '{file_name}': {e}")

def main():
    parser = argparse.ArgumentParser(
        description="x_browser_client CLI - Manage templates for your project."
    )
    parser.add_argument(
        "template", 
        choices=TEMPLATE_FILES.keys(), 
        help="Specify the template file to copy (.env or examples.py)"
    )
    parser.add_argument(
        "destination", 
        nargs="?", 
        default=os.getcwd(), 
        help="Specify the destination directory (default: current directory)"
    )

    args = parser.parse_args()
    copy_template(args.template, args.destination)

if __name__ == "__main__":
    main()
