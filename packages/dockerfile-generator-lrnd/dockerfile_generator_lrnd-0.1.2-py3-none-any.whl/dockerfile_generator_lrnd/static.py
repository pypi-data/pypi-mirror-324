# dockerfile_generator/static.py
from .base import DockerfileGenerator

class StaticGenerator(DockerfileGenerator):
    def generate_dockerfile(self):
        self.add_from("nginx:alpine")
        self.add_copy(".", "/usr/share/nginx/html")
        self.add_expose(80)
        self.add_cmd("nginx -g 'daemon off;'")
