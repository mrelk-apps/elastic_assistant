import json
import yaml
import sys
from elasticsearch import Elasticsearch, ElasticsearchException


def validate_arugments(arguments: sys.argv):
    """
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


def read_config_yaml(file_path: str):
    """
    this function will take the config.yml file and return it as dictionary
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

def pretty(data: dict, sort_keys: bool = False, indent: int = 4) -> json:
    """
    print dictionary in pretty mode
    
    parameters : 
    - data = dictionary that needed to be printted in pretty mode
    - sort_keys = boolean that allow you to sort keys of the dictionary
    - indent = integer that increase the indentation of the json

    returns : json formatted dictionary
    """
    return json.dumps(data, sort_keys=sort_keys, indent=indent)


def calculate_nodes(data_type: str, data_size: float, retention: int, mem_per_node: int, replicas: int = 1, low_watermark: float = 0.15) -> int:
    """
    
    """    
    if data_type == "hot":
        ratio = 30
    elif data_type == "warm":
        ratio = 160
    elif data_type == "cold":
        ratio = 500
    elif data_type == "frozen":
        ratio = 1000
    else:
        return "please choose valid data type [hot, warm, cold, frozen]"
    total_data = data_size * retention * (replicas+1)
    total_storage = total_data * (1+low_watermark+0.1)
    total_nodes = round(total_storage/mem_per_node/ratio)
    return total_nodes, total_storage, data_type


def get_watcher_engine_status(es: Elasticsearch):
    """
    collects data about watchers and the watching engine
    """
    if es is None:
        return None
    else:
        try:
            es.cat.indices(index = ".watches")
            unassigned_watches = 0
            data = []
            watchers_data = es.cat.shards(index=".watches", format="json", h="id,node,prirep,state")
            engines_count = len(watchers_data)
            for i in range(engines_count):
                if watchers_data[i]['state'] == "UNASSIGNED":
                    unassigned_watches += 1
                watcher_stats = es.watcher.stats(filter_path="stats",format="json")["stats"]
                for j in range(len(watcher_stats)):
                    if watchers_data[i]["id"] == watcher_stats[j]["node_id"]:
                        data.append([watchers_data[i]["node"], watcher_stats[j]])
            active_engines =  engines_count - unassigned_watches
            return active_engines, unassigned_watches, data 
        except ElasticsearchException:
            return 0, 0, None


def get_nodes_stats(es: Elasticsearch):
    """
    """
    if es is None:
        return None
    else:
        try:
            es.nodes.stats()
            
        except ElasticsearchException:
            return None
        