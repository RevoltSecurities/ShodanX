import httpx
from bs4 import BeautifulSoup,XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning
import warnings
from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils

class ShodanXWebSearch():
    def __init__(self, query: str, facet:str,session: httpx.AsyncClient, verbose:bool = False) -> None:
        self.sesssion = session
        self.facet = facet
        self.verbose = verbose
        self.query = query
        self.results = []
        self._shodan_utils = ShodanxUtils()
        self._logger = Logger()
        self._shodan_url =f"https://www.shodan.io/search/facet?query={self.query}&facet={self.facet}"
        self.data = {"shodan_web_search": []}
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
    
    async def search(self) -> dict[str,str]:
        try:
            self.headers["User-Agent"] = self._shodan_utils.random_useragent()
            response = await self.sesssion.request("GET", self._shodan_url, headers=self.headers, timeout=30)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
                warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
                soup = BeautifulSoup(response.text, "lxml")
                results = soup.find_all('strong')
                for result in results:
                    self.results.append(result.get_text())
                self.data['shodan_web_search'] = self.results
        except Exception as e:
            if self.verbose:
                self._logger.warn(f"error occured in the shodan search module due to: {e}")
        finally:
            return self.data
    