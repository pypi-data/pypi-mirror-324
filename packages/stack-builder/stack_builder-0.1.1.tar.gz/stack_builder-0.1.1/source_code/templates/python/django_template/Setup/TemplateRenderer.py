import os
from jinja2 import Template

class TemplateRenderer:
    @staticmethod
    def render_template(template_path: str, context: dict, output_path: str):
        """
        Generate a file based on a Jinja template and a given context.

        Args:
            template_path (str): Path to the Jinja template file.
            context (dict): Dictionary of variables to render the template with.
            output_path (str): Path to save the rendered file.

        Raises:
            FileNotFoundError: If the specified template file does not exist.
            Exception: For any other errors that occur during the rendering process.
        """
        try:
            # Check if the template file exists
            if not os.path.exists(template_path):
                raise FileNotFoundError(f"Template not found: {template_path}")

            # Read the template file content
            with open(template_path, "r") as template_file:
                template_content = template_file.read()

            # Render the template with the provided context
            template = Template(template_content)
            rendered_content = template.render(context)

            # Write the rendered content to the output file
            with open(output_path, "w") as output_file:
                output_file.write(rendered_content)

            print(f"File successfully generated: {output_path}")
        
        except FileNotFoundError as fnf_error:
            print(f"Error: {fnf_error}")
            raise

        except Exception as e:
            print(f"An error occurred while rendering the template: {e}")
            raise
