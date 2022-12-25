from flask import Flask, render_template, request
from modules.elastic_connector import *
from modules.mrelk import *

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def home():
    es,connection_status = multi_url_connection(config['elasticsearch.url'], 
                                        config['elasticsearch.username'], 
                                        config['elasticsearch.password'], 
                                        config['elasticsearch.ssl.certificateAuthorities'], 
                                        config['elasticsearch.ssl.verificationMode'])
    if connection_status == "Connected":
        cluster_status = es.cluster.health()
        active_engines, inactive_engines, watchers_status = get_watcher_engine_status(es)
        es.close()
    else:
        cluster_status = ""
        active_engines = ""
        watchers_status = ""
        inactive_engines = ""
    return render_template('home.html', 
                connection_status=connection_status, 
                cluster_status=cluster_status,
                active_engines=active_engines,
                inactive_engines=inactive_engines,
                watchers_status=watchers_status)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    config, _ = read_config_yaml(arguments['conf.path'])
    _,connection_status = multi_url_connection(config['elasticsearch.url'], 
                                        config['elasticsearch.username'], 
                                        config['elasticsearch.password'], 
                                        config['elasticsearch.ssl.certificateAuthorities'], 
                                        config['elasticsearch.ssl.verificationMode'])
    return render_template('settings.html', 
                connection_status=connection_status,config=config)


@app.route('/nodes_view')
def nodes_view():
    config, _ = read_config_yaml(arguments['conf.path'])
    es,connection_status = multi_url_connection(config['elasticsearch.url'], 
                                        config['elasticsearch.username'], 
                                        config['elasticsearch.password'], 
                                        config['elasticsearch.ssl.certificateAuthorities'], 
                                        config['elasticsearch.ssl.verificationMode'])
    if connection_status == "Connected":
        node_stats_headers, node_stats_data, master_id = get_node_stats(es)
        allocation_headers, allocation_data = get_allocation(es)
        thread_pool_headers, thread_pool_data = get_thread_pool(es)
        return render_template('nodes.html', 
                    connection_status=connection_status,
                    node_stats_headers=node_stats_headers,
                    node_stats_data=node_stats_data,
                    master_id=master_id,
                    allocation_headers=allocation_headers,
                    allocation_data=allocation_data,
                    thread_pool_headers=thread_pool_headers,
                    thread_pool_data=thread_pool_data)
    else:
        cluster_status = ""
        active_engines = ""
        watchers_status = ""
        inactive_engines = ""
        return render_template('home.html', 
                connection_status=connection_status, 
                cluster_status=cluster_status,
                active_engines=active_engines,
                inactive_engines=inactive_engines,
                watchers_status=watchers_status)

@app.route('/index_view')
def index_view():
    config, _ = read_config_yaml(arguments['conf.path'])
    es,connection_status = multi_url_connection(config['elasticsearch.url'], 
                                        config['elasticsearch.username'], 
                                        config['elasticsearch.password'], 
                                        config['elasticsearch.ssl.certificateAuthorities'], 
                                        config['elasticsearch.ssl.verificationMode'])
    if connection_status == "Connected":
        index_stats_headers, index_stats_data = get_index_stats(es)
        return render_template('index.html', 
                    connection_status=connection_status,
                    index_stats_headers=index_stats_headers,
                    index_stats_data=index_stats_data
                 )
    else:
        cluster_status = ""
        active_engines = ""
        watchers_status = ""
        inactive_engines = ""
        return render_template('home.html', 
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
            app.run(host=config['server.host'], port=config['server.port'])
        else:
            print("Mr.Elk is not happy!")
            print("you messed up the config file.")
            print(conf_valid)
    else:
        print("Mr.Elk is not happy! ")
        print("you are trying to use invalid arguments.")
        print(arg_valid)