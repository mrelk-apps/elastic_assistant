import requests

def establish_connection(urls: list,
    username: str = "", 
    password: str = "", 
    verify: bool = False, 
    certificate_path: str = "" ):
    """
    establish_connection is used to establish connection between python and server
    
    parameters:
        - urls = list of urls to establish connection with

    optional parameters : 
        - username = server username. 
        - password = server password.     
        - verify = ssl verification (in case you want to skip verification of certificate)
        - certificate_path = in case of using https add the path of the certificate.
    
    returns: 
        - session = session with all the parameters
        - connection_status = Connected or Not Conneted
    """
    for url in urls:
        scheme = str(url).split(':')[0]
        s = requests.Session()         
        if scheme == 'https':
            s.verify = verify
            s.auth = (username, password)
            if verify:
                s.cert=certificate_path
            else:
                requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)    
        try:      
            response = s.get(url)
            if response.ok:
                if url[-1] == "/":
                    s.url = str(url)
                else:
                    s.url = str(url) + "/"
            return s, "Connected"
        except:
            pass   
    return None, "Not Connected"

def check_connection(s):
    """
    check connection
    """
    try:
        response = s.get(s.url)
        if response.ok:
            return "Connected"
    except:
        return "Not Connected"