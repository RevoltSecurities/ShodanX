import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from shodanx.modules.logger.logger import Logger
from typing import List,Dict
from rich import box


class ShodanFaviconMap():
    def __init__(self,session:httpx.AsyncClient,all:bool = False,top:int =50):
        self.logger = Logger()
        self.console = Console()
        self.session = session
        self.all = all
        self.top = top
        self._shodan_url = "https://faviconmap.shodan.io/data/favicons.json"
        
    async def search(self) -> list:
        try:
            response: httpx.Response = await self.session.request("GET", self._shodan_url, timeout=30)
            if response.status_code != 200:
                return []
            data = response.json()
            self.display_favicon_ranking(data)
            return data
        except Exception as e:
            self.logger.warn(f"Error occured in the favicon map search due to: {e}")
            return []
        
    def display_favicon_ranking(self, data: List[Dict]) -> None:

        sorted_data = sorted(data, key=lambda x: x["count"], reverse=True)
        display_data = sorted_data if self.all else sorted_data[:self.top]
        
        table = Table(
            title="🔍 [bold #00ff41]ShodanX Favicon Intelligence[/] [bold #ff00ff]::[/] [bold #00ffff]Hash Rankings[/]",
            box=box.DOUBLE_EDGE,
            border_style="bold #ff00ff",
            header_style="bold #00ffff",
            style="bold #00ff41 on #0a0a0a",
            show_lines=True
        )
        
        table.add_column("[bold #ff5555]Rank[/]", justify="right", style="bold #00ffff")
        table.add_column("[bold #ff5555]Favicon Hash[/]", style="bold #ff00ff")
        table.add_column("[bold #ff5555]Host Count[/]", justify="right", style="bold #00ff41")
        table.add_column("[bold #ff5555]Shodan Query[/]", style="bold #ffff00", overflow="fold")
        
        for rank, entry in enumerate(display_data, start=1):
            hash_val = str(entry["hash"])
            count = entry["count"]
            query_url = f"https://www.shodan.io/search?query=http.favicon.hash:{hash_val}"
            
            if count > 10000:
                count_style = "[blink bold red]"
                rank_style = "[bold red]"
            elif count > 5000:
                count_style = "[bold red]"
                rank_style = "[bold yellow]"
            elif count > 1000:
                count_style = "[bold yellow]"
                rank_style = "[bold #00ffff]"
            else:
                count_style = "[bold #00ff41]"
                rank_style = "[bold white]"
            
            formatted_count = f"{count_style}{count:,}[/]"
            
            table.add_row(
                f"{rank_style}{rank}[/]",
                f"[bold magenta]{hash_val}[/]",
                formatted_count,
                f"[link={query_url}][bold cyan]shodan search[/][/]"
            )
        
        total_hashes = len(data)
        total_hosts = sum(entry["count"] for entry in data)
        top_percentage = (sum(entry["count"] for entry in display_data) / total_hosts * 100)
        
        summary_table = Table(
            box=box.SIMPLE_HEAVY,
            show_header=False,
            style="bold #00ff41"
        )
        summary_table.add_column("Metric", style="bold #00ffff")
        summary_table.add_column("Value", style="bold #ff5555")
        
        summary_table.add_row("Total Unique Hashes", f"[bold white]{total_hashes:,}[/]")
        summary_table.add_row("Total Hosts Mapped", f"[bold white]{total_hosts:,}[/]")
        summary_table.add_row("Top Coverage", f"[bold white]{top_percentage:.1f}%[/]")
        
        self.console.print(Panel(
            table,
            title="[bold #ff00ff] FAVICON THREAT INTELLIGENCE [/]",
            border_style="bold #00ffff",
            padding=(0, 2)
        ))
        
        self.console.print(Panel(
            summary_table,
            title="[bold #ffff00] STATISTICS SUMMARY [/]",
            border_style="bold #ff5555",
            width=60
        ))
        
        self.console.print(
            Text.from_markup(
                "[bold #00ff41]Tip: [white]Click on Shodan query links to view hosts with matching favicon hashes[/]"
            ),
            justify="center"
        )