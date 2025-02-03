# dockerfile_generator/python.py
import os
from .base import DockerfileGenerator

class PythonGenerator(DockerfileGenerator):
    def __init__(self, app_path):
        super().__init__(app_path)
        self.python_version = self._detect_python_version()
        self.project_type = self._detect_project_type()
        self.use_poetry = self._check_poetry()

    def _detect_python_version(self):
        # Check runtime.txt
        if os.path.exists(os.path.join(self.app_path, "runtime.txt")):
            with open(os.path.join(self.app_path, "runtime.txt")) as f:
                version = f.read().strip().replace("python-", "")
                return version
        
        # Check .python-version
        if os.path.exists(os.path.join(self.app_path, ".python-version")):
            with open(os.path.join(self.app_path, ".python-version")) as f:
                return f.read().strip()
        
        return "3.11"  # Default to latest stable Python version

    def _detect_project_type(self):
        files = os.listdir(self.app_path)
        if "manage.py" in files:
            return "django"
        if any(f.endswith("fastapi.py") or "fastapi" in f.lower() for f in files):
            return "fastapi"
        if any(f.endswith("flask.py") or "flask" in f.lower() for f in files):
            return "flask"
        return "generic"

    def _check_poetry(self):
        return os.path.exists(os.path.join(self.app_path, "pyproject.toml"))

    def generate_dockerfile(self):
        # Base image
        self.add_from(f"python:{self.python_version}-slim")

        # System dependencies
        self.add_run("apt-get update && apt-get install -y --no-install-recommends \
            build-essential \
            curl \
            && rm -rf /var/lib/apt/lists/*")

        # Set environment variables
        self.add_env("PYTHONUNBUFFERED", "1")
        self.add_env("PYTHONDONTWRITEBYTECODE", "1")
        self.add_env("PIP_NO_CACHE_DIR", "off")
        self.add_env("PIP_DISABLE_PIP_VERSION_CHECK", "on")

        # Working directory
        self.add_workdir("/app")

        # Install dependencies
        if self.use_poetry:
            self.add_run("curl -sSL https://install.python-poetry.org | python -")
            self.add_copy("pyproject.toml poetry.lock* ./")
            self.add_run("poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi")
        else:
            self.add_copy("requirements.txt", ".")
            self.add_run("pip install --upgrade pip && pip install -r requirements.txt")

        # Copy application
        self.add_copy(".", ".")

        # Set default port
        self.add_expose(8000)

        # Set startup command based on project type using default development servers
        if self.project_type == "django":
            self.add_cmd("python manage.py runserver 0.0.0.0:8000")
        elif self.project_type == "flask":
            self.add_env("FLASK_APP", "app.py")
            self.add_env("FLASK_ENV", "production")
            self.add_cmd("flask run --host=0.0.0.0 --port=8000")
        elif self.project_type == "fastapi":
            self.add_cmd("uvicorn main:app --host 0.0.0.0 --port 8000")
        else:
            self.add_cmd("python app.py")
