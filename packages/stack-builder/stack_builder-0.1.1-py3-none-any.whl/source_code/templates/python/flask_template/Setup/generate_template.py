from jinja2 import Template
import os


class TemplateGenerator:
    @staticmethod
    def generate(template_path, context, output_path):
        """
        Generate a file from a Jinja2 template with the given context.
        """
        with open(template_path, "r") as template_file:
            template = Template(template_file.read())

        with open(output_path, "w") as output_file:
            output_file.write(template.render(context))
