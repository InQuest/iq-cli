import yaml

config = {}

try:
    with open('config.yml') as _config_file:
        config = yaml.safe_load(_config_file)
except IOError:
    pass
