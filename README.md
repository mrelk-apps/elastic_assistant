# Mr.Elk' Elastic Assistant
This webapp is made by experts to help you maintain and monitor your elasticsearch/opensearch clusters easily

Features:

its a simple wrapper over elasticsearch important apis, it will help you do the following:
- assign new shards
- check thread pools 
- monitor your cluster internal statistics (allocation, requests completed, requests rejected ..etc) 
- if you have elastic license, it will help you check the health of the watcher engine as well
- move shards between nodes

and all that with just few clicks, no need to search, write or memorize any apis



To run the app use the following command 
    `python webapp.py --conf.path="location\to\config.yml"`
    
and make sure to install the following libraries 
- elasticsearch=7.17.6
- flask=latest
