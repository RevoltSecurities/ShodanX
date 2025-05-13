import httpx
from bs4 import BeautifulSoup,XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning
import warnings
from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils
import getpass
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt


class ShodanAuth():
    def __init__(self,auth_yaml: str, cookie_json: str ,session: httpx.AsyncClient = None):
        self.session = session
        self.logger = Logger()
        self._auth_url = "https://account.shodan.io/login"
        self._shodan_utils = ShodanxUtils()
        self.auth_file = auth_yaml
        self.cookie_file = cookie_json
        self.console =  Console()
        self.cookie = None
        
    async def get_csrf_token(self) -> str | None:
        response : httpx.Response = await self.session.request(
            "GET", 
            self._auth_url, 
            headers={"User-Agent": self._shodan_utils.random_useragent()}, 
            timeout=30, 
            follow_redirects=True)
        
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
            warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
            soup = BeautifulSoup(response.text, "lxml")
            csrf_token_input = soup.find('input', {'name': 'csrf_token'})
            if csrf_token_input and csrf_token_input.get('value'):
                return csrf_token_input.get('value')
            else:
                return None
            
    async def login(self) -> str:
        username,password = await self._shodan_utils.load_yaml(self.auth_file)
        if  username is None or password is None:
            self.logger.warn("missing username or password of shodan, please update in the shodanx configuration file!")
            exit()
        csrf_token = await self.get_csrf_token()
        if not csrf_token:
            self.logger.warn("Unable to get CSRF Token!")
            csrf_token = "ef4d11775524c201f89e15aa7f489492264ad78c"
        body = {
            "username": username,
            "password": password,
            "grant_type":	password,
            "continue":	"https://account.shodan.io/",
            "csrf_token": csrf_token
        }
        headers = {
            'User-Agent': ShodanxUtils.random_useragent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://account.shodan.io',
            'Connection': 'keep-alive',
            'Referer': 'https://account.shodan.io/login',
            'Cookie': '_ga=GA1.2.477518759.1715975591; _ga_BNT9JE7KQX=GS2.2.s1746366123$o3$g0$t1746366123$j0$l0$h0; cf_clearance=3rC2dBEmiwC6hnNv1wMQmPQ1klLi2HM7f.Q.RVDLI4Q-1720690157-1.0.1.1-4NSsfAl.vKpLpYH.wSqyfInQTMTyYGoHkq4by9h6CR34d661r3jJRNT9bzhgs9qlp6DAIhEpRsz9vjnG2or2qQ; _gid=GA1.2.1420983711.1746355713; session=avmZ3iUoZP4PiU6Q6dhukKde2sDMT1C6cyJPW8_i-IWXExQzy_RL0ag4lNTmWIKfSgVF_w4W14blHN_cyiRrx4AFlXYAAAAAAAAASpqWF2hHQdoF4NNPMpl9lCiMDGNvbnRpbnVlX3VybJSMGmh0dHBzOi8vYWNjb3VudC5zaG9kYW4uaW8vlIwHX2NzcmZ0X5SMKGRjZjFkNzM1NDYyZmU2ZmJmMDNhZjU3MGIwMjhkMTNiNDcwYjliZDCUdYeULg',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }
        response : httpx.Response = await self.session.request(
            "POST", 
            self._auth_url, 
            headers=headers, 
            timeout=30,
            data=body,
            follow_redirects=True
        )
        
        if response.status_code != 302 and "Invalid username or password" in response.text:
            self.logger.warn("invalid credentials detected, please config the valid credentials! or set cookie manually!")
            return None
                
        cookies = response.cookies
        if "polito" in cookies and "session" in cookies:
            cookie = f"polito={cookies['polito']}; session={cookies['session']}"
            return cookie
        else:
            self.logger.warn("invalid cookie, please set the cookie manually and restart!")
            return None
        
    async def valid_session(self) -> bool:
        cookies = await self._shodan_utils.load_json(self.cookie_file)
        if cookies is None:
            return False
        
        headers = {
            'User-Agent': ShodanxUtils.random_useragent(),
            'Cookie': str(cookies),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://account.shodan.io',
            'Connection': 'keep-alive',
            'Referer': 'https://account.shodan.io/login',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'trailers'
        }
        response: httpx.Response = await self.session.request("GET", "https://account.shodan.io/", timeout=30, headers=headers)
        if response.status_code != 200:
            return False
        return True
    
    async def shell_login(self):
        console = Console()
        welcome_panel = Panel.fit(
            Text("Welcome to Shodanx Login Mode", 
                 style="bold green"),
            title="[bold blue]ShodanX Login Setup[/]",
            border_style="bright_blue",
            padding=(1, 4),
            style="bold white"
        )
        console.print(welcome_panel)
        try:
            ask = Prompt()
            console.print(f"[bold green]Please make sure paste cookies without spaces[/]")
            cookie = ask.ask("Enter your active sesson cookie (hidden) ", password=True)
            if len(cookie) == 0:
                console.print(f"[bold red]Please enter a valid session cookies![/]")
                return None
            return cookie
        except Exception as e:
            console.print(f"[bold red]Error during input: {e}[/]")
            return None