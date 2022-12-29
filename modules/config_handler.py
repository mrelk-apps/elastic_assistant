import yaml
import sys

def validate_arugments(arguments: sys.argv):
    """
    this function validates the webapp and the arguments sent to it
    """
    options = {}
    if len(arguments) > 1:  
        for i in range(1, len(arguments)):
            if len(arguments[i].split('=')) == 2:
                if arguments[i].split('=')[0] not in ['--conf.path']:
                    return None, "Unrecognized argument "+arguments[i]
                else:
                    options[str(arguments[i]).split('=')[0].split('--')[1]] = str(arguments[i]).split('=')[1]
            else:
                return None, "Unrecognized argument "+arguments[i]
        return options, "Valid"
    return None, "--conf.path is missing!"


def validate_config_yaml(file_path: str):
    """
    this function will take the config.yml file validate it and return it as dictionary if valid
    """
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    if dict(config).get('server.host') != None:
        if dict(config).get('server.port') != None:
            if dict(config).get('elasticsearch.url') != None:
                return config, "Valid"
            else:
                return None, "Missing elasticsearch.url!"
        else:
            return None, "Missing server.port!"
    else:
        return None, "Missing server.host"