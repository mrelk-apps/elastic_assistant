### Elasticsearch 7.X 
import requests
from typing import Any
from ssl import create_default_context
from elasticsearch import Elasticsearch, ElasticsearchException


def multi_url_connection(urls:list, username:str, password:str, certificate_path:str, verify:bool):
    """
    this function uses establish_connection function to connect to multi nodes
    it will round robin over all the urls until all urls are failed or until one is connected
    """
    for url in urls:
        es,connection_status = establish_connection(url, username, password, certificate_path, verify)
        #print(url,"-->",connection_status)
        if connection_status == "Connected":
            return es, connection_status
    return es, connection_status


def establish_connection(url: str, username: str, password: str, certificate_path: str, verify: bool):
    """
    establish_connection is used to establish connection between python and elastic server
    
    parameters : 
    - ip_list = list of ips to establish connection with. default is '[localhost]'
    - port = elasticsearch port. default is 9200
    - username = elasticsearch username. default is "elastic"
    - password = elasticsearch password. default is "elastic"
    - scheme = type of connection (http or https). default is "http"
    - certificate_path = in case of using https add the path of the certificate.
    - verify = ssl verification (in case you want to skip verification of certificate)

    returns : Elasticsearch connected instance or None in case of failure
    """
    scheme = str(url).split(':')[0]
    
    # connection variables
    connection_limit = 5

    # establish connection over http
    if scheme == 'http':
        es = Elasticsearch(
            url,
            http_auth=(username, password),
            maxsize=connection_limit,
            http_compress=True,
            ssl_show_warn=False)
    
    # establish connection over https
    elif scheme == 'https':
        if verify == True:
            certificate = create_default_context(cafile=certificate_path)
            es = Elasticsearch(
                url,
                http_auth=(username, password),
                ssl_context=certificate,
                maxsize=connection_limit,
                http_compress=True)
        elif verify == False:
            es = Elasticsearch(
                url,
                http_auth=(username, password),
                maxsize=connection_limit,
                http_compress=True,
                verify_certs=False,
                ssl_show_warn=False)

    # test connection and return the result
    if es.ping():
        return es, "Connected"
    else:
        return None, "Not Connected"

def check_connection(url: str, username: str, password: str, certificate_path: str, verify: bool):
    url = "http://10.0.0.12:9200/"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        response.close()
        return "Connected"
    else:
        return "Not Connected"

