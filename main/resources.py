"""Simple resource system"""
import yaml


def res(path):
    """Return resource to which the path points"""
    with open('Resources\\resources.yml', 'r') as resources_file:
        resource = yaml.load(resources_file)
        split = path.split('\\')
        for part in split:
            if type(resource) is list:
                part = int(part)
            resource = resource[part]
        return resource
