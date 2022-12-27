# Mr.Elk' Elastic Assistant
Mr.Elk is a project made to help engineers in their day to day work with ease and flexability, it's a bot that will do actions, maintain your services, and all in a cute gamified view.

the first of Mr.Elk's apps will be "Elastic Assistant"

This webapp is made by experts to help you maintain and monitor your elasticsearch/opensearch clusters easily

Features:

its a simple wrapper over elasticsearch important apis, it will help you do the following and it will refresh automatically every few seconds to get fresh stats:
- assign new shards
- check thread pools 
- monitor your cluster internal statistics (allocation, requests completed, requests rejected ..etc) 
- if you have elastic license, it will help you check the health of the watcher engine as well
- move shards between nodes

and all that with just few clicks, no need to search, write or memorize any apis 
WAIT, there is way more coming soon
- integration with slack for automatic cluster monitoring
- more monitoring view
- analyze your cluster settings and give you recommendations
- help you build a cluster by giving you recommendations
and more and more and more.

and if you have any ideas, we will be happy to work on it if they are upvoted and people need it :D


To run the app use the following command 
    `python webapp.py --conf.path="location\to\config.yml"`
    
and make sure to install the following libraries 
- elasticsearch==7.17.5
- Flask==2.2.2
- PyYAML==6.0
- requests==2.28.1

SCREENSHOTS:

Home Page:

<img width="878" alt="image" src="https://user-images.githubusercontent.com/33005145/208752199-ebe1bf1c-6b2c-4347-adf5-42ea9bc67291.png">

Node Thread Pool:

<img width="847" alt="image" src="https://user-images.githubusercontent.com/33005145/208752415-e2ccfd94-abe4-4dd9-9c65-f309f1795fab.png">
