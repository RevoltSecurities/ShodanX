import httpx
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.rule import Rule
from rich.align import Align

from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils


class ShodanxMapsOSINT:
    def __init__(self, session: httpx.AsyncClient) -> None:
        self.session = session
        self.console = Console()
        self.logger = Logger()
        self._shodan_utils = ShodanxUtils()
        self._shodan_url = "https://maps.shodan.io/_search"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Alt-Used": "maps.shodan.io",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Priority": "u=0, i",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache"
        }

    def _generate_maps_link(self, latitude, longitude):
        return f"https://www.google.com/maps?q={latitude},{longitude}"

    async def search(self, cookies_file: str, place: str) -> dict:
        try:
            cookies = await self._shodan_utils.load_json(cookies_file)
            if not cookies:
                self.logger.warn("No cookies found. Please configure your Shodan keys.")
                return {}

            self.headers["Cookie"] = cookies
            self.headers["User-Agent"] = self._shodan_utils.random_useragent()
            params = {"q": place}

            response: httpx.Response = await self.session.request("GET", self._shodan_url, timeout=30, headers=self.headers, params=params)
            if response.status_code != 200:
                self.logger.warn(f"Received non-200 status: {response.status_code}")
                return {}

            data = response.json()
            self.display_maps_osint_results(data)
            return data

        except Exception as e:
            self.logger.warn(f"Error occurred in Shodan Maps OSINT: {e}")
            return {}

    def display_maps_osint_results(self, data):
        self.console.print(
            Panel(
                Align.center(
                    Text.from_markup(
                        f"[bold magenta]:satellite: ShodanX:zap: Advanced Recon[/bold magenta]\n"
                        f"[bold cyan]🧠 Total Matches:[/bold cyan] [bold white]{data['total']:,}[/bold white] | "
                        f"[bold green]Displayed:[/bold green] {len(data['matches'])}\n"
                        f"[dim]🚀 Think like an attacker. Visualize like a hacker.[/dim]"
                    ),
                    vertical="middle"
                ),
                title="🛰️ [bright_white]MAPS INTELLIGENCE[/bright_white]",
                border_style="bold bright_magenta",
            )
        )

        for idx, match in enumerate(data['matches'], 1):
            ip = match['ip_str']
            port = match['port']
            loc = match['location']

            base_service = self._shodan_utils.get_service_name(port)
            port_style, service = self._shodan_utils.get_port_style_and_service(port, base_service)

            country = f"{loc.get('country_name', 'Unknown')} ({loc.get('country_code', '--')})"
            city = loc.get("city", "N/A")
            region = loc.get("region_code", "N/A")
            lat = loc.get("latitude", 0)
            lon = loc.get("longitude", 0)
            coords = f"{lat:.4f}, {lon:.4f}"
            maps_link = self._generate_maps_link(lat, lon)

            ipinfo_link = f"https://ipinfo.io/{ip}"
            shodan_link = f"https://www.shodan.io/host/{ip}"

            host_table = Table.grid(padding=(0, 2))
            host_table.add_column(justify="right", style="cyan", no_wrap=True)
            host_table.add_column(style="bold white")

            host_table.add_row("🧠 IP", f"[bold cyan]{ip}[/bold cyan]")
            host_table.add_row("🔌 Port", f"[{port_style}]{port}[/{port_style}] → [bold green]{service}[/bold green]")
            host_table.add_row("📍 Location", f"[yellow]{city}, {region}[/yellow] — [green]{country}[/green]")
            host_table.add_row("🌐 Coords", f"[white]{coords}[/white]")
            host_table.add_row("🗺️  Map", f"[link={maps_link}]Google Maps[/link]")
            host_table.add_row("🧰 OSINT", f"[link={ipinfo_link}]ipinfo[/link] | [link={shodan_link}]shodan[/link]")

            self.console.print(
                Panel(
                    host_table,
                    title=f"[bold cyan]# {idx} → Host OSINT Map Data[/bold cyan]",
                    border_style="bright_blue"
                )
            )

        self.console.print(Rule(style="bright_magenta"))
        self.console.print(
            Panel(
                "[bold white]Additional Recon Resources:[/bold white]\n"
                "- [link=https://www.shodan.io/]Shodan Search[/link] for more host fingerprints\n"
                "- [link=https://viz.greynoise.io/]GreyNoise Viz[/link] to profile noise vs. target\n"
                "- [link=https://censys.io/]Censys[/link] for certificate and device scans\n"
                "- [link=https://www.onyphe.io/]Onyphe[/link] for cyber threat context\n",
                title="[bold green]🔎 Hacker’s Recon Panel[/bold green]",
                border_style="green"
            )
        )
