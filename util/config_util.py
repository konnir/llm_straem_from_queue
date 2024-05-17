import yaml


def read_yaml_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def read_text_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
