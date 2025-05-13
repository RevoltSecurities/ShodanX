import aiofiles
import yaml
from fake_useragent import UserAgent
import sys
import socket

class ShodanxUtils:
    @staticmethod
    async def load_yaml(filename: str):
        async with aiofiles.open(filename, "r") as file:
            contents = await file.read()
            data = yaml.safe_load(contents)
            return data.get('shodanx', {}).get('username'), data.get('shodanx', {}).get('password')
        
    @staticmethod
    async def load_key(filename: str):
        async with aiofiles.open(filename, "r") as file:
            contents = await file.read()
            data = yaml.safe_load(contents)
            return data.get('shodanx', {}).get('apikey')

    @staticmethod
    async def load_json(filename: str):
        async with aiofiles.open(filename, "r") as file:
            contents = await file.read()
            data = yaml.safe_load(contents)
            return data.get('cookies', None)
        
    
    @staticmethod
    async def set_cookie(filename: str, cookie: str):
        new_data = {"cookies": cookie}
        async with aiofiles.open(filename, "w") as file:
            await file.write(yaml.dump(new_data, indent=4))

    @staticmethod
    async def set_auth(filename: str, username: str, password:str, apikey:str):
        new_data = {
            'shodanx': {
                'username': username,
                'password': password,
                'apikey': apikey
            }
        }
        async with aiofiles.open(filename, "w") as file:
            await file.write(yaml.dump(new_data, default_flow_style=False))
            
    @staticmethod
    async def async_reader(filename: str):
        try:
            async with aiofiles.open(filename, "r") as file:
                content = await file.readlines()
                return [line.strip() for line in content if line.strip()]
        except Exception:
            return None
            
    @staticmethod        
    def get_service_name(port:int):
        try:
            return socket.getservbyport(port, 'tcp')
        except Exception:
            try:
                return socket.getservbyport(port, 'udp')
            except Exception:
                return "unknown service"
            
    @staticmethod
    def random_useragent()-> str:
        return UserAgent().random
    
    def Exit(val = 0) -> None:
        sys.exit(val)
        
    @staticmethod
    def get_port_style_and_service(port:int, default_service="unknow service"):
        port_styles = {
        21:     ("bold red",     "FTP (plain-text credentials)"),
        22:     ("bold green",   "SSH (remote access)"),
        23:     ("bold red",     "Telnet (insecure remote access)"),
        25:     ("bold yellow",  "SMTP (email/spam vector)"),
        53:     ("bold cyan",    "DNS (recon)"),
        80:     ("bold green",        "HTTP (web)"),
        110:    ("bold yellow",  "POP3 (email)"),
        123:    ("bold yellow",       "NTP (time sync leak)"),
        135:    ("bold red",          "MS RPC (pivot risk)"),
        137:    ("bold red",          "NetBIOS Name (SMB)"),
        138:    ("bold red",          "NetBIOS Datagram"),
        139:    ("bold red",          "SMB (NetBIOS)"),
        143:    ("bold yellow",       "IMAP (email)"),
        161:    ("bold red",     "SNMP (info leak)"),
        162:    ("bold red",     "SNMP Trap (info leak)"),
        179:    ("yellow",       "BGP (routing protocol)"),
        389:    ("bold yellow",  "LDAP (auth exposure)"),
        443:    ("bold green",   "HTTPS (secure web)"),
        445:    ("bold red",     "SMB (EternalBlue, RCE risk)"),
        465:    ("bold green",        "SMTPS (secure email)"),
        514:    ("bold yellow",       "Syslog (log leak)"),
        587:    ("bold green",        "SMTP (submission)"),
        593:    ("bold red",          "RPC over HTTP"),
        631:    ("bold yellow",       "IPP (printer exposure)"),
        636:    ("bold green",        "LDAPS (secure directory)"),
        873:    ("bold yellow",       "rsync (unauth file access)"),
        3389:   ("bold yellow",  "RDP (remote desktop)"),
        5900:   ("bold yellow",  "VNC (unauth screen access)"),
        5800:   ("bold yellow",  "VNC over Web"),
        9001:   ("bold yellow",  "Tor ORPort (relay)"),
        1433:   ("bold red",     "MSSQL (DB exposure)"),
        1521:   ("bold red",     "Oracle DB"),
        3306:   ("bold red",     "MySQL (DB exposure)"),
        5432:   ("bold red",     "PostgreSQL (DB exposure)"),
        5984:   ("bold red",     "CouchDB (unauth access)"),
        6379:   ("bold red",     "Redis (unauth memory access)"),
        9200:   ("bold red",     "Elasticsearch (data exposure)"),
        11211:  ("bold red",     "Memcached (info leak)"),
        27017:  ("bold red",     "MongoDB (unauth access)"),
        8000:   ("bold cyan",         "Dev HTTP"),
        8080:   ("bold cyan",         "Proxy / Web API"),
        8443:   ("bold green",        "HTTPS Alt (dev)"),
        8888:   ("bold cyan",         "HTTP Admin"),
        5000:   ("bold cyan",         "Flask / API"),
        5601:   ("bold yellow",       "Kibana UI"),
        7001:   ("bold cyan",         "WebLogic console"),
        8008:   ("bold cyan",         "Android HTTP"),
        8983:   ("bold yellow",       "Apache Solr"),
        1883:   ("bold yellow",  "MQTT (IoT messaging)"),
        8883:   ("bold yellow",  "MQTTS (secure IoT)"),
        20000:  ("bold red",          "DNP3 (SCADA)"),
        44818:  ("bold red",          "EtherNet/IP (ICS)"),
        2049:   ("bold red",          "NFS (file exposure)"),
        5000:   ("bold yellow",       "Flask / Docker API"),
        6000:   ("bold red",          "X11 (screen capture risk)"),
        6666:   ("bold yellow",       "IRC (unfiltered)"),
        6667:   ("bold yellow",       "IRC"),
        8081:   ("bold cyan",         "Alt Web UI"),
        8889:   ("bold yellow",       "Jupyter Notebook"),
        2375:   ("bold red",          "Docker API (unauth)"),
        2379:   ("bold red",          "etcd (K8s config leak)"),
        2380:   ("bold red",          "etcd peer port"),
        6443:   ("bold yellow",       "Kubernetes API"),
        10250:  ("bold red",          "Kubelet (RCE risk)"),
        10255:  ("bold red",          "Kubelet ReadOnly"),
        1194:   ("bold green",        "OpenVPN"),
        1701:   ("bold green",        "L2TP"),
        500:    ("bold green",        "IPSec"),
        4500:   ("bold green",        "IPSec NAT-T"),
        5222:   ("bold yellow",       "XMPP (chat)"),
        5269:   ("bold yellow",       "XMPP Server"),
        6665:   ("bold yellow",       "IRC"),
        7000:   ("bold yellow",       "IRC"),
        7071:   ("bold yellow",       "Zimbra Admin"),
    }
        style, label = port_styles.get(port, ("bold yellow", default_service))
        return style, label

