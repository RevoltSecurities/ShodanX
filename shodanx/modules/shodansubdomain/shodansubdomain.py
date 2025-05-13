import httpx
from bs4 import BeautifulSoup,XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning
import warnings
from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils

class ShodanXSubdomainEnumerator():
    def __init__(self, domain:str, session:httpx.AsyncClient, verbose:bool =False):
        self.domain = domain
        self.session = session
        self._shodan_url = f"https://www.shodan.io/domain/{self.domain}"
        self.results = []
        self.verbose = verbose
        self.data = {"shodan_subdomains": self.results}
        self._logger = Logger()
        self._shodan_utils = ShodanxUtils
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Connection": "keep-alive",
            "Referer": "https://account.shodan.io/?language=en",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Priority": "u=0, i",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "TE": "trailers"
        }
        
    async def enumerate(self) -> dict[str,str]:
        try:
            self.headers["User-Agent"] = self._shodan_utils.random_useragent()
            response: httpx.Response = await self.session.request("GET", self._shodan_url, headers=self.headers, timeout=30)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
                warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
                soup = BeautifulSoup(response.text, "lxml")
                ul = soup.find('ul', id='subdomains')
                if ul:
                    results = ul.findAll("li")
                    for result in results:
                        self.results.append(result.text.strip()+f".{self.domain}")
                self.data["shodan_subdomains"] = self.results
        except Exception as e:
            self._logger.warn(f"error occured in shodanx subdomain enumeration due to: {e}")
        finally:
            return self.data