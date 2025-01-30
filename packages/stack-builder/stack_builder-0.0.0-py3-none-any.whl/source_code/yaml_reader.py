import yaml
class yaml_reader:
    @staticmethod
    def read(config_path):
        with open(config_path, 'r') as file:
            return yaml.safe_load(file)