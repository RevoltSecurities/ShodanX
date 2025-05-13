import httpx
from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils
from rich.panel import Panel
from rich.console import Console
from rich.rule import Rule
from rich.tree import Tree
from collections import defaultdict
from typing import Dict, Any


class ShodanxTrendsDB:
    def __init__(self, yaml_file: str, query: str, session: httpx.AsyncClient, facet: str = "ip") -> None:
        self.yaml_auth = yaml_file
        self.query = query
        self.session = session
        self.facet = facet
        self.logger = Logger()
        self._shodan_utils = ShodanxUtils()
        self._shodan_url = f"https://trends.shodan.io/api/v1/search?query={self.query}&facets={self.facet}"
        self.console = Console()

    def _generate_bar(self, count, max_count, length=30):
        filled_len = int(length * count // max_count) if max_count else 0
        bar = "█" * filled_len + "░" * (length - filled_len)
        return f"[green]{bar}[/green]"

    async def search_trends(self) -> dict:
        try:
            apikey = await self._shodan_utils.load_key(self.yaml_auth)
            if not apikey:
                self.logger.warn("No Shodan API key found for Shodan Trends search, please configure a valid API key")
                return {}
            url = f"{self._shodan_url}&key={apikey}"
            response: httpx.Response = await self.session.request("GET", url, timeout=30)
            if response.status_code != 200:
                self.logger.warn(f"Shodan Trends returned non-200 status code: {response.status_code}")
                return {}
            data = response.json()
            self.display_trends(data)
            return data
        except Exception as e:
            self.logger.warn(f"Error occurred in the trends search module: {e}")

    def display_trends(self, data: Dict[str, Any]) -> None:
        matches = data.get("matches", [])
        facet_data = data.get("facets", {}).get(self.facet, [])

        if not matches and not facet_data:
            self.console.print(f"[bold red]❌ No trend data available for facet: {self.facet}[/bold red]")
            return

        total_count = data.get("total", 0)
        max_count = max((m["count"] for m in matches), default=1)

        overview = Panel.fit(
            f"[bold bright_white]🔍 Query:[/bold bright_white] {self.query}\n"
            f"[bold bright_white]📊 Total Records:[/bold bright_white] {total_count:,}\n"
            f"[bold bright_white]🗓️ Time Range:[/bold bright_white] {matches[0]['month']} → {matches[-1]['month']} ({len(matches)} months)\n"
            f"[bold bright_white]🎯 Facet:[/bold bright_white] [cyan]{self.facet.upper()}[/cyan]",
            title="[bold blue]Shodan Trends Overview[/bold blue]",
            border_style="bright_magenta",
            padding=(1, 2)
        )
        self.console.print(overview)

        if matches:
            self.console.print(Rule("[bold cyan]📈 Monthly Activity Overview[/bold cyan]"))
            prev_count = None
            for match in matches:
                month = match["month"]
                count = match["count"]

                change_text = ""
                if prev_count is not None and prev_count != 0:
                    change = ((count - prev_count) / prev_count) * 100
                    if change > 0:
                        change_text = f"[green]🟢 +{change:.1f}%[/green]"
                    elif change < 0:
                        change_text = f"[red]🔻 {change:.1f}%[/red]"
                    else:
                        change_text = f"[yellow]⚪ 0.0%[/yellow]"

                bar = self._generate_bar(count, max_count)
                self.console.print(
                    f"[bold white]{month}[/bold white] ─ {count:,} {change_text}\n{bar}"
                )
                prev_count = count
            self.console.print()

        if facet_data:
            self.console.print(Rule(f"[bold magenta]📊 {self.facet.upper()} Distribution[/bold magenta]"))
            yearly_facet_data = defaultdict(list)
            for entry in facet_data:
                year = entry["key"][:4]
                yearly_facet_data[year].append(entry)

            distribution_tree = Tree(f"[bold underline]📊 {self.facet.upper()} Distribution[/bold underline]")
            for year, entries in sorted(yearly_facet_data.items()):
                year_branch = distribution_tree.add(f"[bold magenta]{year}[/bold magenta]")

                months = defaultdict(list)
                for entry in entries:
                    month = entry["key"][5:]  
                    months[month].append(entry)
                for month, month_entries in sorted(months.items()):
                    month_branch = year_branch.add(f"[bold yellow]{month}[/bold yellow]")

                    for entry in month_entries:

                        total_month_count = next(
                            (m["count"] for m in matches if m["month"] == entry["key"]),
                            sum(v["count"] for v in entry["values"])
                        )
                        for val in entry["values"]:
                            domain = str(val["value"])
                            count = val["count"]
                            percentage = (count / total_month_count * 100) if total_month_count > 0 else 0
                            month_branch.add(
                                f"[green]{domain}[/green] ─ [yellow]{count:,}[/yellow] ([cyan]{percentage:.1f}%[/cyan])"
                            )
            self.console.print(distribution_tree)
            self.console.print()

        info_panel = Panel.fit(
            f"[bold white]🧾 Displayed {len(matches)} monthly totals and {sum(len(m['values']) for m in facet_data)} {self.facet.upper()} values[/bold white]\n"
            f"[bold white]Available facets:[/bold white] [italic cyan]{', '.join(data.get('facets', {}).keys())}[/italic cyan]",
            title="[green]Data Summary[/green]",
            border_style="green"
        )
        self.console.print(info_panel)
