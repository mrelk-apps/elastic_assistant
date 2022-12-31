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
                if arguments[i].split('=')[0] not in ['--conf.path','--server.host','--server.port','--elasticsearch.url','--elasticsearch.username','--elasticsearch.password','--elasticsearch.ssl.certificateAuthorities','--elasticsearch.ssl.verificationMode']:
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
    return validate_config_cli(config)

def validate_config_cli(config :dict):
    """
    this function will take the cli configurations and validate it in case of using cli not config.yml
    """
    if 'elasticsearch.username' not in config:
        config['elasticsearch.username'] = ""
    if 'elasticsearch.password' not in config:
        config['elasticsearch.password'] = ""
    if 'elasticsearch.ssl.certificateAuthorities' not in config:
        config['elasticsearch.ssl.certificateAuthorities'] = ""
    if 'elasticsearch.ssl.verificationMode' not in config:
        config['elasticsearch.ssl.verificationMode'] = False
    if 'logging.verbose' not in config:
        config['logging.verbose'] = False
    if 'logging.dest' not in config:
        config['logging.dest'] = ""
    if dict(config).get('server.host') != None:
        if dict(config).get('server.port') != None:
            if dict(config).get('elasticsearch.url') != None:
                config['elasticsearch.url'] = str(config['elasticsearch.url']).split(',') 
                return config, "Valid"
            else:
                return None, "Missing elasticsearch.url!"
        else:
            return None, "Missing server.port!"
    else:
        return None, "Missing server.host!"