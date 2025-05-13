import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils
from rich import box

class ShodanxCVEDB:
    def __init__(
        self,
        session: httpx.AsyncClient,
        product: str = None,
        cpe23: str = None,
        count: bool = False,
        is_kev: bool = False,
        sort_by_epss: bool = False,
        skip: int = 0,
        limit: int = 1000,
        start_date: str = None,
        end_date: str = None,
        verbose: bool = False,
    ):
        self.session = session
        self.product = product
        self.cpe23 = cpe23
        self.count = count
        self.is_kev = is_kev
        self.sort_by_epss = sort_by_epss
        self.skip = skip
        self.limit = limit
        self.start_date = start_date
        self.end_date = end_date
        self.verbose = verbose
        self.console = Console()
        self.logger = Logger()
        self.utils = ShodanxUtils
        self._shodan_url = "https://cvedb.shodan.io"

    async def search(self,cpe=None,product=None) -> dict:
        if self.product and self.cpe23:
            self.logger.error("You can only specify one of 'product' or 'cpe23'.")
            return {}
        params = {
            "is_kev": self.is_kev,
            "skip": self.skip,
            "limit": self.limit,
        }
        if self.start_date:
            params["start_date"] = self.start_date
        if self.end_date:
            params["end_date"] = self.end_date
        if cpe:
            params["cpe23"] = cpe
        if product:
            params["product"] = product
        try:
            url = f"{self._shodan_url}/cves"
            response: httpx.Response = await self.session.request("GET",url,params=params, timeout=30)
            if response.status_code != 200:
                return {}
            data = response.json()
            self._display_cve_all_table(data.get("cves", []))
            return data
        except Exception as e:
            self.logger.warn(f"Error occured in the cve search module due to: {e}, {type(e)}")
            return {}

    async def search_cve_by_id(self,cveid: str) -> dict:
        try:
            request_url = f"{self._shodan_url}/cve/{cveid}"
            response : httpx.Response = await self.session.request("GET", request_url, timeout=30)
            if response.status_code != 200:
                return {}
            data = response.json()
            self._display_cve_details(data)
            return data
        except Exception as e:
            self.logger.warn(f"Error occured in the id cve search module due to: {e}")
            return {}
        
    async def search_cve_by_cpe(self,cpe:str) -> dict:
        try:
            params = {
            "cpe23":cpe,
            "is_kev": self.is_kev,
            "skip": self.skip,
            "limit": self.limit,
            }
            if self.start_date:
                params["start_date"] = self.start_date
            if self.end_date:
                params["end_date"] = self.end_date
            request_url = f"{self._shodan_url}/cves"
            response: httpx.Response =  await self.session.request("GET", request_url, timeout=30, params=params)
            if response.status_code != 200:
                return {}
            data = response.json()
            self._display_cve_all_table(data)
            return data
        except Exception as e:
            self.logger.warn(f"Error occured in the cpe search module due to: {e}")
            return {}
    
    
        
    def _display_cve_all_table(self, cves: list):
        if not cves:
                self.console.print("[bold yellow]No CVEs found.[/bold yellow]")
                return
            
        table = Table(
                title="[bold white]Shodanx CVE Database Results[/bold white]",
                box=box.ROUNDED,
                style="bold white",
                show_lines=True, 
                header_style="bold cyan",
                row_styles=["none"]
                )
    
        table.add_column("CVE ID", style="bold cyan", no_wrap=True, min_width=12)
        table.add_column("Summary", style="bold white", min_width=40, overflow="fold")
        table.add_column("CVSS", style="bold red", justify="center", width=6)
        table.add_column("EPSS", style="bold green", justify="center", width=6)
        table.add_column("Exploited", style="bold magenta", justify="center", width=10)
        table.add_column("References", style="bold yellow", min_width=30, overflow="fold")
        table.add_column("Published", style="bold blue", no_wrap=True, width=20)

        for cve in cves:
            references = cve.get("references", [])
            if len(references) > 3:
                refs = "\n".join(references[:3]) + f"\n[...+{len(references)-3} more]"
            else:
                refs = "\n".join(references) if references else "N/A"

            summary = cve.get("summary", "N/A")
            

            table.add_row(
                cve.get("cve_id", "N/A"),
                summary,
                str(cve.get("cvss", "N/A")),
                str(cve.get("epss", "N/A")),
                "✅" if cve.get("kev") else "❌",
                refs,
                cve.get("published_time", "N/A")
            )
    
        self.console.print(Panel.fit(
            table,
            title="[bold]CVE Database Results[/bold]",
            border_style="blue",
            padding=(1, 2)
        ))
        
    def _display_cve_details(self, cve: dict):
        table = Table(title=f"CVE Details: {cve.get('cve_id', 'N/A')}", style="bold white",box=box.ROUNDED,show_lines=True, header_style="bold cyan",row_styles=["none"])
        table.add_column("Field", style="bold magenta", no_wrap=True)
        table.add_column("Data", style="bold cyan")
        table.add_row("CVE ID", cve.get("cve_id", "N/A"),style="bold white")
        table.add_row("Summary", cve.get("summary", "N/A"),style="bold cyan")
        table.add_row("CVSS (Overall)", str(cve.get("cvss", "N/A")),style="bold yellow")
        table.add_row("EPSS", str(cve.get("epss", "N/A")),style="bold cyan")
        table.add_row("Ranking EPSS", str(cve.get("ranking_epss", "N/A")),style="bold cyan")
        table.add_row("KEV (Exploited)", "✅ Yes" if cve.get("kev") else "❌ No",style="bold white")
        table.add_row("Proposed Action", cve.get("propose_action", "N/A"), style="bold magenta")
        table.add_row("Ransomware Campaign", cve.get("ransomware_campaign", "N/A"),style="bold white")
        table.add_row("Published Time", cve.get("published_time", "N/A"),style="bold green")
        
        references = "\n".join(cve.get("references", [])) or "N/A"
        table.add_row("References", references,style="bold cyan")
        cpes = "\n".join(cve.get("cpes", [])) or "N/A"
        table.add_row("CPEs", cpes,style="bold blue")

        self.console.print(table)
        