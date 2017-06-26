"""Simple resource system"""
import yaml


def res(path):
    """Return resource to which the path points
    
    examples:
    res('item')         get resource named 'item'
    res('dict\\item')   get resource from dict 'dict' on keyword 'item'
    res('list\\2)       get resource from list 'list' on index 2
    """
    with open('Agent/Resources/resources.yml', 'r') as resources_file:
        resource = yaml.load(resources_file)
        split = path.split('\\')
        for part in split:
            if type(resource) is list:
                part = int(part)
            resource = resource[part]
        return resource


def ares(path):
    """Return agent resource to which the path points"""
    # with open('Agent/Resources/agent.yml', 'r') as resources_file:
    with open('Resources/agent.yml', 'r') as resources_file:
        resource = yaml.load(resources_file)
        split = path.split('\\')
        for part in split:
            if type(resource) is list:
                part = int(part)
            resource = resource[part]
        return resource
