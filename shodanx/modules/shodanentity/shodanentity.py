import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List, Dict, Any
from shodanx.modules.logger.logger import Logger
from rich import box
from rich.text import Text
from rich.columns import Columns
from rich.align import Align

class ShodanxEntityDB:
    def __init__(self, session: httpx.AsyncClient):
        self._shodan_url = "https://entitydb.shodan.io/api"
        self.session = session
        self.console = Console()
        self.logger = Logger()

    async def list_all_entities(self) -> List[Dict[str, Any]]:
        url = f"{self._shodan_url}/entities/"
        try:
            response: httpx.Response = await self.session.get(url, timeout=30, follow_redirects=True)
            data = response.json()
            entities = data.get("entities", [])
            self.display_entities_table(entities=entities)
            return entities
        except Exception as e:
            self.logger.warn(f"Error occurred in the listing entity DB due to: {e}")
            return []
        
    def display_entities_table(self, entities: List[Dict[str, Any]]) -> None:
        table = Table(
            title="[bold white]ShodanX Entity DB - Companies List[/bold white]",
            box=box.DOUBLE_EDGE,
            border_style="bright_blue",
            header_style="bold bright_green",
            show_lines=True,
            expand=True
        )
    
        table.add_column("ID", style="bold green", justify="right", width=8)
        table.add_column("CIK", style="bold cyan", justify="right", width=12)
        table.add_column("Tickers", style="bold yellow", width=15)
        table.add_column("Entity Name", style="bold magenta", overflow="fold")

        for idx, ent in enumerate(entities):
            id = str(ent.get("id", "N/A"))
            cik = str(ent.get("cik", "N/A"))
            tickers = ", ".join(ent.get("tickers", [])) or "[dim]N/A[/dim]"
            name = ent.get("entity_name", "[dim]N/A[/dim]")
        
            row_style = "bold bright_white" if idx % 2 == 0 else "bold bright_cyan"
        
            if "N/A" not in cik:
                cik = f"[bold bright_green]{cik}[/bold bright_green]"
            if "N/A" not in tickers:
                tickers = f"[bold bright_yellow]{tickers}[/bold bright_yellow]"
        
            table.add_row(
                f"[green]{id}[/green]",
                cik,
                tickers,
                f"[bright_magenta]{name}[/bright_magenta]",
                style=row_style
            )

        panel = Panel.fit(
            table,
            title="[bold yellow]Corporate Entities Intelligence[/bold yellow]",
            subtitle="[dim]Data sourced from Shodan Entity Database[/dim]",
            border_style="bright_white",
            padding=(1, 2),
            style="on black"
        )
    
        self.console.print(panel)
        
    async def list_entity_by_id(self, id: int) -> dict:
        try:
            url = f"{self._shodan_url}/entities/{id}"
            response: httpx.Response = await self.session.request("GET", url, timeout=30, follow_redirects=True)
            if response.status_code != 200:
                return {}
            data = response.json()
            entity = data["entity"]
            self.display_entity_table(entity)
            return entity
        except Exception as e:
            self.logger.warn(f"Error occurred in the id entity db search module due to: {e}")
            return {}
            
    def display_entity_table(self, entity: Dict[str, Any]) -> None:
        header = Panel.fit(
            Text.from_markup(
            f"[bold bright_cyan]{entity.get('entity_name', 'N/A')}[/]\n"
            f"[bold yellow]{entity.get('entity_type', 'N/A')}[/]"
            ),
            border_style="bright_blue"
        )
        self.console.print(header)
    
        info_panel1 = Panel(
            Text.from_markup(
            f"🏛 [bold green]CIK:[/] [bright_white]{entity.get('cik', 'N/A')}[/]\n"
            f"📈 [bold green]Tickers:[/] [bright_yellow]{', '.join(entity.get('tickers', ['N/A']))}[/]\n"
            f"🏷 [bold green]SIC:[/] [white]{entity.get('sic', 'N/A')}[/] ([italic]{entity.get('sic_description', 'N/A')}[/])"
            ),
            title="[bold]Financial ID[/]",
            border_style="bright_green"
        )
    
        info_panel2 = Panel(
            Text.from_markup(
            f"🌐 [bold green]Website:[/] [bright_blue underline]{entity.get('hostname', 'N/A')}[/]\n"
            f"📞 [bold green]Phone:[/] [white]{entity.get('phone', 'N/A')}[/]\n"
            f"📅 [bold green]FY End:[/] [white]{entity.get('fiscal_year_end', 'N/A')}[/]"
            ),
            title="[bold]Contact Info[/]",
            border_style="bright_blue"
        )
    
        self.console.print(Columns([info_panel1, info_panel2]))
    
        address_panel = Panel(
            Text.from_markup(
            f"🏢 [bold green]Address:[/]\n[white]{entity.get('business_address', 'N/A')}[/]"
            ),
            border_style="bright_magenta"
        )
        self.console.print(address_panel)
    
        asn_table = Table(
            title="[bold yellow]NETWORK FOOTPRINT[/bold yellow]",
            box=box.DOUBLE_EDGE,
            border_style="bright_yellow",
            header_style="bold bright_cyan",
            show_lines=True,
            expand=True
        )
    
        asn_table.add_column("ASN", style="bold blue", justify="right")
        asn_table.add_column("CIDRs", style="bold white", justify="center")
        asn_table.add_column("Total IPs", style="bold magenta", justify="right")
        asn_table.add_column("Threat Profile", style="bold red", justify="center")
    
        ip_count = 0
        for asn_data in entity.get("asns", []):
            asn = str(asn_data.get("asn", "N/A"))
            prefixes = asn_data.get("route_views", [])
            cidr_count = len(prefixes)
        
            asn_ip_count = 0
            for p in prefixes:
                try:
                    asn_ip_count += int(p.get("number_ips", 0))
                except (ValueError, TypeError):
                    pass
        
            ip_count += asn_ip_count
        
            threat_level = "🟢 Low" if asn_ip_count < 1000 else \
                      "🟡 Medium" if asn_ip_count < 10000 else \
                      "🔴 High" if asn_ip_count < 50000 else \
                      "💀 Critical"
        
            asn_table.add_row(
            f"[bold bright_blue]{asn}[/]",
            f"[bold]{cidr_count:,}[/]",
            f"[bold bright_magenta]{asn_ip_count:,}[/]",
            f"[bold]{threat_level}[/]"
            )

        all_prefixes = [p.get('prefix', 'N/A') for asn in entity.get('asns', []) for p in asn.get('route_views', [])]
        if all_prefixes:
            largest_cidr = max(all_prefixes, key=lambda x: len(x) if x != 'N/A' else 0)
        else:
            largest_cidr = "N/A (No prefixes available)"

        network_panel = Panel(
            Text.from_markup(
            f"[bold]🌍 Total Network Exposure:[/] [bright_red]{ip_count:,}[/] IP addresses across [bright_yellow]{len(entity.get('asns', []))}[/] ASNs\n"
            f"[bold]🔥 Largest CIDR Block:[/] [bright_white]{largest_cidr}[/]"
            ),
            title="[bold]NETWORK THREAT ASSESSMENT[/bold]",
            border_style="yellow",
            style="on black"
            )
    
        self.console.print("\n")
        self.console.print(network_panel)
        self.console.print("\n")
        self.console.print(asn_table)
    
    # just a suggestion :)
        if ip_count > 10000:
            security_panel = Panel(
            Text.from_markup(
                "[bold bright_red]⚠️ HIGH RISK TARGET ⚠️[/]\n"
                "This organization has significant internet exposure\n"
                "Recommended recon techniques:\n"
                "• [bold]Masscan[/] for rapid port scanning\n"
                "• [bold]Shodan[/] queries for exposed services\n"
                "• [bold]ASN[/] mapping for network topology"
            ),
            border_style="bold red",
            style="on bright_black"
            )
            self.console.print("\n")
            self.console.print(security_panel)