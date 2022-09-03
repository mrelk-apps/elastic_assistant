from flask import Flask, render_template, request
from modules.elastic_connector import *
from modules.mrelk import *

app = Flask(__name__)


@app.route('/')
def home():
    if connection_status == "Connected":
        cluster_status = es.cluster.health()
        active_engines, inactive_engines, watchers_status = get_watcher_engine_status(es)
    else:
        cluster_status = ""
        active_engines = ""
        watchers_status = ""
        inactive_engines = ""
    return render_template('index.html', 
                connection_status=connection_status, 
                cluster_status=cluster_status,
                active_engines=active_engines,
                inactive_engines=inactive_engines,
                watchers_status=watchers_status)

if __name__ == '__main__':
    arguments, arg_valid = validate_arugments(sys.argv)
    if arg_valid == "Valid":
        config, conf_valid = read_config_yaml(arguments['conf.path'])
        if conf_valid == "Valid":
            app.config['DEBUG'] = config['logging.verbose']
            es,connection_status = multi_url_connection(config['elasticsearch.url'], 
                                        config['elasticsearch.username'], 
                                        config['elasticsearch.password'], 
                                        config['elasticsearch.ssl.certificateAuthorities'], 
                                        config['elasticsearch.ssl.verificationMode'])
            app.run(host=config['server.host'], port=config['server.port'])
        else:
            print("Mr.Elk is not happy!")
            print("you messed up the config file.")
            print(conf_valid)
    else:
        print("Mr.Elk is not happy! ")
        print("you are trying to use invalid arguments.")
        print(arg_valid)