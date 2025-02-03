# dockerfile_generator/utils.py
import os
from pathlib import Path

def detect_application_type(app_path):
    path = Path(app_path)
    
    if (path / "package.json").exists():
        return "nodejs"
    elif (path / "requirements.txt").exists():
        return "python"
    elif (path / "composer.json").exists():
        return "php"
    elif any(path.glob("*.html")):
        return "static"
    return None
