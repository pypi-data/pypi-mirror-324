# dockerfile_generator/cli.py
import click
import os
from pathlib import Path
from .utils import detect_application_type
from .exceptions import UnsupportedTechnologyError
from .nodejs import NodeJSGenerator  # Add this import
from .python import PythonGenerator  # Add this import
from .php import PHPGenerator        # Add this import
from .static import StaticGenerator  # Add this import

@click.command()
@click.argument("app_path", type=click.Path(exists=True))
@click.option("--output", "-o", default="Dockerfile", help="Output file path")
def generate_dockerfile(app_path, output):
    """Generate a Dockerfile for the application at APP_PATH"""
    app_type = detect_application_type(app_path)
    
    generators = {
        "nodejs": NodeJSGenerator,
        "python": PythonGenerator,
        "php": PHPGenerator,
        "static": StaticGenerator
    }
    
    if app_type not in generators:
        raise UnsupportedTechnologyError(f"Unsupported application type in {app_path}")
    
    generator = generators[app_type](app_path)
    generator.generate_dockerfile()
    generator.generate(output)
    
    click.echo(f"Successfully generated Dockerfile at {output}")
