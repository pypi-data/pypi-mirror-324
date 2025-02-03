# dockerfile_generator/base.py
class DockerfileGenerator:
    def __init__(self, app_path):
        self.app_path = app_path
        self.lines = []
        self.port = None

    def add_line(self, line):
        self.lines.append(line)

    def add_from(self, base_image):
        self.add_line(f"FROM {base_image}")

    def add_workdir(self, path):
        self.add_line(f"WORKDIR {path}")

    def add_copy(self, src, dest):
        self.add_line(f"COPY {src} {dest}")

    def add_run(self, command):
        self.add_line(f"RUN {command}")

    def add_expose(self, port):
        self.port = port
        self.add_line(f"EXPOSE {port}")

    def add_cmd(self, command):
        self.add_line(f'CMD ["{command}"]')

    # Add the missing add_env method
    def add_env(self, key, value):
        self.add_line(f"ENV {key}={value}")

    # Add the missing add_healthcheck method
    def add_healthcheck(self, command):
        self.add_line(f"HEALTHCHECK {command}")

    def generate(self, output_path="Dockerfile"):
        with open(output_path, "w") as f:
            f.write("\n".join(self.lines))
