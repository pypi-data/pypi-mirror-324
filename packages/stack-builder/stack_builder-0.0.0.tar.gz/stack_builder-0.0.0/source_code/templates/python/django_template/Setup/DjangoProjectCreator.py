import os
import subprocess
from .UpdateSetting  import UpdateSetting
from .TemplateRenderer import TemplateRenderer

class DjangoProjectCreator:
    def __init__(self, project_name: str, port: int, image_version: str, db_type: str, db_version: str, db_name: str, db_user: str, db_password: str,  db_port: str):
        """
        Initialize the DjangoProjectCreator class with project and database configurations.

        Args:
            project_name (str): Name of the Django project.
            port (int): Port for the Django application.
            image_version (str): Docker image version.
            db_type (str): Type of the database (e.g., MySQL, PostgreSQL).
            db_version (str): Version of the database.
            db_name (str): Database name.
            db_user (str): Database user.
            db_password (str): Database password.
            db_host (str): Host address for the database.
            db_port (str): Port for the database.
        """
        self.project_name = project_name
        self.port = port
        self.image_version = image_version
        self.db_type = db_type
        self.db_version = db_version
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port

        # Define directory paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.getcwd()
        self.project_dir = os.path.join(self.project_root, project_name)

    def create_project(self):
        """
        Create a new Django project with the specified configurations.
        """
        try:
            # Create the project directory
            os.makedirs(self.project_dir, exist_ok=True)
            print(f"Project directory created: {self.project_dir}")
        except OSError as err:
            print(f"Error while creating project directory: {err}")
            return

        # Build the Docker image for the Django engine
        self.build_docker_image()

        # Run the Docker container to initialize the Django project
        self.run_docker_container()

        # Generate project-specific files
        self.generate_project_files()

    def build_docker_image(self):
        """
        Build the Docker image for the Django engine.
        """
        build_command = (
            f"docker build -t django_engine -f {self.script_dir}/../Engine/engine.Dockerfile {self.script_dir}/../Engine/"
        )
        print(f"Executing Docker build command: {build_command}")
        subprocess.run(build_command, shell=True, check=True)

    def run_docker_container(self):
        """
        Run a Docker container to initialize the Django project.
        """
        startproject_command = (
            f"docker run --rm -v {self.project_dir}:/app django_engine django-admin startproject {self.project_name} /app/"
        )
        print(f"Executing startproject command: {startproject_command}")
        subprocess.run(startproject_command, shell=True, check=True)

    def generate_project_files(self):
        """
        Generate necessary project files such as Dockerfile, docker-compose.yaml, and settings.py.
        """
        context = {
            "image_version": self.image_version,
            "port": self.port,
            "project_name": self.project_name,
            "db_version": self.db_version,
            "db_image": self.db_name,
            "db_name": self.db_name,
            "db_user": self.db_user,
            "db_password": self.db_password,
            "db_port": self.db_port,
        }

        # Define template paths
        dockerfile_template = os.path.join(self.script_dir, "../Dockerfile/Dockerfile.j2")
        dockerfile_output = os.path.join(self.project_dir, "Dockerfile")
    
        compose_template = os.path.join(self.script_dir, f"../Databases/{self.db_type.lower()}/docker-compose.yaml.j2")
        compose_output = os.path.join(self.project_dir, "docker-compose.yaml")

        requirements_template = os.path.join(self.script_dir, "../requirements.txt")
        requirements_output = os.path.join(self.project_dir, "requirements.txt")

        env_template = os.path.join(self.script_dir, f"../Databases/{self.db_type.lower()}/.env.j2")
        env_output = os.path.join(self.project_dir, ".env")

        setting_template = os.path.join(self.script_dir, f"../Databases/{self.db_type.lower()}/settings.py.j2")
        setting_output = os.path.join(self.project_dir, f"{self.project_name}/settings.py")

        # Render templates
        TemplateRenderer.render_template(dockerfile_template, context, dockerfile_output)
        if self.db_type != 'none':
            TemplateRenderer.render_template(requirements_template, {}, requirements_output)
            TemplateRenderer.render_template(compose_template, context, compose_output)
            TemplateRenderer.render_template(env_template, context, env_output)

            # Update settings.py with database configuration
            UpdateSetting.update_database_config(setting_template, setting_output)

    def _generate_docker_compose(self):
        """
        Generate docker-compose.yaml based on the chosen database template.
        """
        raise NotImplementedError("This method is a placeholder and is not implemented.")
