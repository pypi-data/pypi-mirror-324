# dockerfile_generator/php.py
import os
from .base import DockerfileGenerator

class PHPGenerator(DockerfileGenerator):
    def __init__(self, app_path):
        super().__init__(app_path)
        self.php_version = "8.2"

    def generate_dockerfile(self):
        self.add_from(f"php:{self.php_version}-apache")
        self.add_workdir("/var/www/html")
        self.add_copy(".", "/var/www/html/")
        self.add_expose(80)
