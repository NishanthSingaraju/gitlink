import os
from jinja2 import Template

from gitstore.constants import PLUGINS_DIR

def create_dockerfile(config: dict, target_directory: str):
    env_vars = config.get('env_variables', {})
    env_var_definitions = "\n".join([f"ENV {key} {value}" for key, value in env_vars.items()])

    # Get the dependencies for each plugin
    plugins = config.get("plugins", [])
    plugin_dependencies = []
    for plugin in plugins:
        plugin_path = os.path.join(PLUGINS_DIR, plugin)
        requirements_file = os.path.join(plugin_path, "requirements.txt")
        with open(requirements_file) as f:
            plugin_dependencies += f.read().strip().split("\n")

    # Combine the dependencies from plugins and the main project
    dependencies = plugin_dependencies + config.get("dependencies", [])
    dependencies_str = "\n".join(["RUN pip install " + dependency for dependency in dependencies])

    template = Template(
        """
        # Use an official Python runtime as the base image
        FROM python:3.9

        # Set the working directory in the container
        WORKDIR /app

        # Install dependencies
        {{ dependencies }}

        # Copy the application code to the container
        COPY . .

        RUN pip install -r requirements.txt

        {{ env_var_definitions }}

        # Run the application
        ENV PORT 8000

        CMD uvicorn api:app --host 0.0.0.0 --port ${PORT}
        """
    )

    with open(os.path.join(target_directory,'Dockerfile'), 'w') as f:
        f.write(template.render(dependencies=dependencies_str, env_var_definitions=env_var_definitions))