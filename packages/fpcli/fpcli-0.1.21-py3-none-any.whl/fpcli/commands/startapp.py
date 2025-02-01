import os
from pathlib import Path
import typer

from ..function.startproject import create_file
from ..content.startproject import   get_helper_utilities_content,  get_urls_contant, get_welcome_controller_contant
from .basic import app

def create_folder_structure(base_dir: str):
    """Creates the folder and file structure."""
    folders = [
        "migrations",      
    ]

    files = {
        f"{base_dir}/config.py": "# Configuration file",
        f"{base_dir}/urls.py": "# all routes file\n"+get_urls_contant(),
        f"{base_dir}/utils.py": "# Utility functions \n\n"+get_helper_utilities_content(),
        f"{base_dir}/views.py": "#Welcome View  ",
        f"{base_dir}/schemas.py": "",
        f"{base_dir}/middleware.py": "",
        f"{base_dir}/models.py": "",

    }

    # Create folders
    for folder in folders:
        os.makedirs(f"{base_dir}/{folder}", exist_ok=True)

    # Create files
    for file, content in files.items():
        create_file(file, content)
    
@app.command("startapp")
def startapp(name: str):
    """Create a new project structure."""
    base_dir = Path(name).resolve()
    os.makedirs(base_dir, exist_ok=True)
    create_folder_structure(str(base_dir))
    typer.echo(f"Project '{name}' created successfully at {base_dir}!")

