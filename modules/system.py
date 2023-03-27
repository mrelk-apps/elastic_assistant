def calculate_nodes(data_type: str, data_size: float, retention: int, mem_per_node: int, replicas: int = 1, low_watermark: float = 0.15) -> int:
    """
    calculate needed nodes for each index
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


def get_watcher_engine_status(session):
    """
    collects data about watchers and the watching engine
    """
    if session is None:
        return None
    else:
        try:
            unassigned_watches = 0
            data = []
            watchers_data = session.get(session.url+"_cat/indices?index=.watches&format=json&h=id,node,prirep,state").json()
            engines_count = len(watchers_data)
            for i in range(engines_count):
                if watchers_data[i]['state'] == "UNASSIGNED":
                    unassigned_watches += 1
                watcher_stats = session.get(session.url+"_watcher/stats&filter_path=stats&format=json").json()["stats"]
                for j in range(len(watcher_stats)):
                    if watchers_data[i]["id"] == watcher_stats[j]["node_id"]:
                        data.append([watchers_data[i]["node"], watcher_stats[j]])
            active_engines =  engines_count - unassigned_watches
            return active_engines, unassigned_watches, data 
        except:
            return 0, 0, None



def get_thread_pool(session):
    """
    get thread pool for nodes
    """  
    if session is None:
        return None
    else:
        try:
            table_data = session.get(session.url+"_cat/thread_pool?format=json&h=node_name,ip,name,queue_size,queue,active,rejected,completed&s=nn,ip,c").json()
            table_headers = ["node.name","node.ip","action","queue.size","queued","active","rejected","completed"]
            return table_headers, table_data
        except:
            return None, None

def get_node_stats(session):
    """
    get nodes stats
    """  
    if session is None:
        return None
    else:
        try:
            table_data = session.get(session.url+"_nodes/stats?format=json&metric=os,jvm&filter_path=nodes.*.name,nodes.*.ip,nodes.*.version,nodes.*.roles,nodes.*.os.cpu.percent,nodes.*.os.mem.used_percent,nodes.*.jvm.mem.heap_used_percent").json()
            table_headers = [" ","node.name","node.ip","node.id","node.roles","os.cpu.used","os.mem.used","jvm.mem.used"]
            master_id = session.get(session.url+"_cat/master?format=json&filter_path=id").json()[0]["id"]
            return table_headers, table_data, master_id
        except:
            return None, None, None

def get_allocation(session):
    """
    get allocation of nodes
    """  
    if session is None:
        return None
    else:
        try:
            table_data = session.get(session.url+"_cat/allocation?format=json&s=n,ip").json()
            table_headers=["node.name","node.ip","shards","disk.used","disk.available","disk.total","disk.percent"]
            return table_headers, table_data
        except:
            return None, None

def get_index_stats(session):
    """
    get index stats
    """  
    if session is None:
        return None
    else:
        try:
            table_data = session.get(session.url+"_cat/indices?format=json&expand_wildcards=all").json()
            table_headers=["index.name","index.uuid","index.health","index.status","primaries","replicas","documents","store.size"]
            return table_headers, table_data
        except:
            return None, None

def get_shards(session):
    """
    get shards
    """  
    if session is None:
        return None
    else:
        try:
            table_data = session.get(session.url+"_cat/shards?format=json&h=i,s,p,st,d,sto,gmto,gto,n,ip&s=node,ip,index,store").json()
            table_headers=["index.name","shard","pri/rep","shard.state","documents","store.size","failed.get.request","total.get.requests","node.name","node.ip"]
            return table_headers, table_data
        except:
            return None, None


