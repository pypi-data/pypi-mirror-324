import os
import shutil
from source_code.templates.python.flask_template.Setup.generate_template import TemplateGenerator
from source_code.templates.python.flask_template.Setup.safe_copytree import SafeCopyTree


class FlaskProjectCreator:
    def __init__(self, project_name, port=5000, workdir="/app", image_version="3.9"):
        self.project_name = project_name
        self.port = port
        self.workdir = workdir
        self.image_version = image_version

        # Paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.abspath(os.path.join(self.script_dir, "../../.."))
        self.template_dir = os.path.join(self.project_root, "templates", "flask_template")

    def create_structure(self):
        os.makedirs(self.project_name, exist_ok=True)

        for item in os.listdir(self.template_dir):
            src_path = os.path.join(self.template_dir, item)
            dst_path = os.path.join(self.project_name, item)

            if item in ["run.py.j2", "Setup"]:
                continue

            if os.path.isdir(src_path):
                os.makedirs(dst_path, exist_ok=True)
                SafeCopyTree.copy(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)

    def generate_files(self):
        context = {
            "project_name": self.project_name,
            "port": self.port,
            "workdir": self.workdir,
            "image_version": self.image_version,
        }

        dockerfile_output = os.path.join(self.project_name, "Dockerfile")
        if os.path.isdir(dockerfile_output):
            shutil.rmtree(dockerfile_output) 

        TemplateGenerator.generate(
            os.path.join(self.template_dir, "Dockerfile", "Dockerfile.j2"),
            context,
            dockerfile_output,
        )

        runpy_output = os.path.join(self.project_name, "run.py")
        if os.path.isdir(runpy_output):
            shutil.rmtree(runpy_output) 

        TemplateGenerator.generate(
            os.path.join(self.template_dir, "run.py.j2"),
            context,
            runpy_output,
        )


    def create_project(self):
        print(f"Creating Flask project {self.project_name}...")
        self.create_structure()
        self.generate_files()
        print(f"The Flask project {self.project_name} has been successfully created!")
