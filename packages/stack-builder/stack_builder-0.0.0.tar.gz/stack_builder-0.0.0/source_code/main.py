import click
import yaml
from source_code.yaml_reader  import yaml_reader
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
source_code_path = os.path.dirname(current_dir)
if source_code_path not in sys.path:
    sys.path.append(source_code_path)

from source_code.templates.python.django_template.Setup.DjangoProjectCreator import DjangoProjectCreator

from source_code.templates.python.flask_template.Setup.create_project_structure import FlaskProjectCreator

def process_database(database_config):
    """Process database configuration and return relevant information."""
    if not database_config:
        return None

    return {
        'type': database_config.get('type', 'sqlite'),
        'version': database_config.get('version', 'latest'),
        'user': database_config.get('user', 'admin'),
        'password': database_config.get('password', 'admin'),
        'name': database_config.get('name', 'default_db'),
        'port': database_config.get('port', 5432)
    }

@click.command()
@click.option('--config', type=click.Path(exists=True), help='Path to the config YAML file for configuration.')
def main(config):
    """
    Generate a project based on the CLI options and/or a YAML configuration file.

    This function checks if a configuration file is provided; if so, it overrides
    the CLI options with values from the configuration file.
    Then, it proceeds to create the project using the specified framework and database settings.
    """
    try:
        # Read configuration from YAML file
        yaml_config = yaml_reader.read(config)

        # Validate project-level configurations
        project = yaml_config.get('project', {})
        project_name = project.get('name', 'Unnamed Project')
        project_description = project.get('description', 'No description provided')
        project_version = project.get('version', 'latest')
        project_author = project.get('author', 'Unknown Author')

        print(f"Starting project setup: {project_name} ({project_description})")
        print(f"Version: {project_version}, Author: {project_author}\n")

        # Iterate through services
        services = yaml_config.get('services', [])
        if not services:
            raise ValueError("No services defined in the configuration file.")

        for service in services:
            service_name = service.get('name', 'Unnamed Service')
            service_description = service.get('description', 'No description provided')

            print(f"Configuring service: {service_name} ({service_description})")

            service_stack = service.get('stack', {})
            service_stack_type = service_stack.get('type', '').lower()
            service_stack_version = service_stack.get('version', 'latest')
            service_stack_port = service_stack.get('port', 5000)

            database_config = process_database(service.get('database'))

            # Create project based on selected framework
            if service_stack_type == 'flask':
                print(f"\nInitializing Flask project setup for service '{service_name}'...")
                creator = FlaskProjectCreator(
                    project_name=service_name,
                    port=service_stack_port,
                    image_version=service_stack_version
                )
                creator.create_project()
                print(f"Flask project '{service_name}' created successfully.\n")

            elif service_stack_type == 'django':
                print(f"\nInitializing Django project setup for service '{service_name}'...")
                creator = DjangoProjectCreator(
                    project_name=service_name,
                    port=service_stack_port,
                    image_version=service_stack_version,
                    db_type=database_config['type'] if database_config else 'none',
                    db_version=database_config['version'] if database_config else None,
                    db_name=database_config['name'] if database_config else None,
                    db_user=database_config['user'] if database_config else None,
                    db_password=database_config['password'] if database_config else None,
                    db_port=database_config['port'] if database_config else 5432
                )
                creator.create_project()
                print(f"Django project '{service_name}' created successfully.\n")

            else:
                print(f"Error: Framework '{service_stack_type}' is not supported yet.\n")

    except yaml.YAMLError as yaml_err:
        print(f"YAML Error: {yaml_err}")
    except FileNotFoundError as file_err:
        print(f"File Error: {file_err}")
    except ValueError as val_err:
        print(f"Configuration Error: {val_err}")
    except Exception as general_err:
        print(f"Unexpected Error: {general_err}")
        raise

if __name__ == '__main__':
    main()
