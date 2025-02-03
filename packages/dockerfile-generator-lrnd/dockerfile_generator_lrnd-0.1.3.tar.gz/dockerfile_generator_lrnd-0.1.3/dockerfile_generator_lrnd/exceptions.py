# dockerfile_generator/exceptions.py
class DockerfileGeneratorError(Exception):
    pass

class UnsupportedTechnologyError(DockerfileGeneratorError):
    pass

class InvalidPackageJsonError(DockerfileGeneratorError):
    pass
