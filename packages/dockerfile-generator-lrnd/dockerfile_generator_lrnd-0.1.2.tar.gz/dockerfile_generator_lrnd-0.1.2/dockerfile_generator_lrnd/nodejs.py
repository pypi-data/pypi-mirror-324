# dockerfile_generator/nodejs.py
import json
import os
from pathlib import Path
from .base import DockerfileGenerator
from .exceptions import InvalidPackageJsonError

class NodeJSGenerator(DockerfileGenerator):
    def __init__(self, app_path):
        super().__init__(app_path)
        self.package_json = self._load_package_json()
        self.node_version = self._detect_node_version()

    def _load_package_json(self):
        path = Path(self.app_path) / "package.json"
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise InvalidPackageJsonError(f"Invalid package.json: {str(e)}")

    def _detect_node_version(self):
        # Simplified version detection (could be improved)
        return self.package_json.get("engines", {}).get("node", "18")

    def generate_dockerfile(self):
        self.add_from(f"node:{self.node_version}")
        self.add_workdir("/app")
        self.add_copy("package*.json", ".")
        self.add_run("npm install")
        self.add_copy(".", ".")
        self.add_expose(3000)
        self.add_cmd("npm start")
