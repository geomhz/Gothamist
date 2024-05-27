import yaml


def load_selectors(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


selectors = load_selectors('selectors.yaml')
