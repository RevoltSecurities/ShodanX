import httpx
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils
from typing import Dict,List
from rich import box

class ShodanExposureDB():
    def __init__(self,country: str, session:httpx.AsyncClient):
        self.logger = Logger()
        self.console = Console()
        self._shodan_utils = ShodanxUtils()
        self.country = country.lower()
        self._shodan_url = "https://shodan.nyc3.digitaloceanspaces.com/exposure-data"
        self.session = session
        self.countries = {
            "united states": "US.json",
            "australia": "AU.json",
            "austria": "AT.json",
            "bangladesh": "BD.json",
            "bahamas": "BS.json",
            "belarus": "BY.json",
            "belgium": "BE.json",
            "brazil": "BR.json",
            "bulgaria": "BG.json",
            "canada": "CA.json",
            "caribbean": "KY.json", 
            "chile": "CL.json",
            "china": "CN.json",
            "costa rica": "CR.json",
            "denmark": "DK.json",
            "finland": "FI.json",
            "france": "FR.json",
            "germany": "DE.json",
            "guatemala": "GT.json",
            "hong kong": "HK.json",
            "hungary": "HU.json",
            "iceland": "IS.json",
            "india": "IN.json",
            "indonesia": "ID.json",
            "israel": "IL.json",
            "iran": "IR.json",
            "ireland": "IE.json",
            "italy": "IT.json",
            "japan": "JP.json",
            "kazakhstan": "KZ.json",
            "kenya": "KE.json",
            "kyrgyzstan": "KG.json",
            "malaysia": "MY.json",
            "mexico": "MX.json",
            "montenegro": "ME.json",
            "morocco": "MA.json",
            "mozambique": "MZ.json",
            "netherlands": "NL.json",
            "norway": "NO.json",
            "panama": "PA.json",
            "philippines": "PH.json",
            "poland": "PL.json",
            "portugal": "PT.json",
            "romania": "RO.json",
            "russia": "RU.json",
            "serbia": "RS.json",
            "slovakia": "SK.json",
            "slovenia": "SI.json",
            "spain": "ES.json",
            "south africa": "ZA.json",
            "south korea": "KR.json",
            "sweden": "SE.json",
            "switzerland": "CH.json",
            "taiwan": "TW.json",
            "turks & caicos": "TC.json",
            "ukraine": "UA.json",
            "venezuela": "VE.json",
            "vietnam": "VN.json"
        }

    def get_json_filename(self) -> str:
        return self.countries.get(self.country, None)
    
    async def search_exposure(self) -> dict:
        try:
            country_file = self.get_json_filename()
            if country_file is None:
                self.logger.warn(f"{self.country} is not found in shodan exposure db, please continue search with other countries.")
                return {}
            url = f"{self._shodan_url}/{country_file}"
            response: httpx.Response = await self.session.request("GET", url, timeout=30)
            if response.status_code != 200:
                return {}
            data = response.json()
            self.display_reports(data)
            return data
        except Exception as e:
            self.logger.warn(f"Error occured in the exposure search due to: {e}")
            return {}

    def _create_threat_overview(self, data: Dict) -> Table:
        table = Table(
            title=f"🔓 [bold #00ff41]ShodanX Threat Matrix[/] | [bold #ff00ff]{self.country}[/]",
            box=box.DOUBLE_EDGE,
            border_style="bold #ff00ff",
            header_style="bold #00ffff",
            style="bold #00ff41 on #0a0a0a"
        )
        table.add_column("[bold #ff5555]Threat Vector[/]", style="bold #00ffff")
        table.add_column("[bold #ff5555]Exposure Count[/]", justify="right", style="bold #ff00ff")

        table.add_row(
            Panel("[blink bold white] CRITICAL THREATS [/]", style="on #330000"),
            "",
            style="on #330000"
        )
        table.add_row("💀 Compromised DBs", f"[blink bold red]{data.get('numCompromisedDB', 0)}[/]")
        table.add_row("☠️ ICS Devices", f"[bold red]{data.get('numIcs', 0)}[/]")
        table.add_row("🔥 BlueKeep", f"[blink bold red]{data.get('numBluekeep', 0)}[/]")
        table.add_row("💣 EternalBlue", f"[blink bold red]{data.get('numEternalblue', 0)}[/]")

        table.add_row(
            Panel("[bold yellow] SECURITY WARNINGS [/]", style="on #333300"),
            "",
            style="on #333300"
        )
        table.add_row("📷 Exposed Webcams", f"[bold yellow]{data.get('numOpenWebcams', 0)}[/]")
        table.add_row("🛡️ Top CVE", f"[bold yellow]{data.get('vuln', 'N/A')}[/]")

        return table

    def _create_port_analysis(self, ports_data: List[List[str]]) -> Table:
        """Create detailed port analysis table using ShodanxUtils"""
        table = Table(
            title="[bold #00ffff]Port Vulnerability Analysis[/]",
            box=box.ROUNDED,
            border_style="bold #00ffff",
            show_lines=True,
            style="bold #00ff41 on #0a0a0a"
        )
        table.add_column("#", style="bold #ff5555", justify="right")
        table.add_column("Port", style="bold #00ffff")
        table.add_column("Service", style="bold #ffff00")
        table.add_column("Risk", style="bold white")
        table.add_column("Count", style="bold #00ff41", justify="right")

        for i, (port_str, count) in enumerate(ports_data, 1): 
            try:
                port = int(port_str)
                style, service = self._shodan_utils.get_port_style_and_service(port)
                
                if "red" in style:
                    risk = "[blink bold red]HIGH[/]"
                elif "yellow" in style:
                    risk = "[bold yellow]MEDIUM[/]"
                else:
                    risk = "[bold #00ff41]LOW[/]"
                
                table.add_row(
                    str(i),
                    f"[{style}]{port}[/]",
                    service,
                    risk,
                    f"[bold white]{count}[/]"
                )
            except ValueError:
                continue

        return table

    def _create_crypto_analysis(self, data: Dict) -> Table:
        table = Table(
            title="🔐 [bold #ffff00]Crypto Weaknesses[/]",
            box=box.SQUARE,
            border_style="bold #ffff00",
            style="bold #00ff41 on #0a0a0a"
        )
        table.add_column("Protocol", style="bold #00ffff")
        table.add_column("Count", style="bold #ff5555", justify="right")
        table.add_column("Risk", style="bold white")

        crypto_data = [
            ("SSLv2", data.get("numSsl2", 0), "[bold red]CRITICAL[/]"),
            ("SSLv3", data.get("numSsl3", 0), "[bold red]HIGH[/]"),
            ("TLS1.0", data.get("numTls1", 0), "[bold yellow]MEDIUM[/]"),
            ("TLS1.1", data.get("numTls11", 0), "[bold yellow]MEDIUM[/]"),
            ("TLS1.2", data.get("numTls12", 0), "[bold #00ff41]LOW[/]")
        ]

        for proto, count, risk in crypto_data:
            table.add_row(proto, str(count), risk)

        return table

    def display_reports(self, data: Dict):
        if not data:
            return

        threat_table = self._create_threat_overview(data)
        port_table = self._create_port_analysis(data.get("ports", []))
        crypto_table = self._create_crypto_analysis(data)

        critical_count = sum([
            data.get("numBluekeep", 0),
            data.get("numEternalblue", 0),
            data.get("numCompromisedDB", 0)
        ])
        
        threat_level = (
            "[blink bold red on #330000] CRITICAL THREATS [/]" if critical_count > 0 else
            "[bold yellow on #333300] WARNING [/]" if data.get("numSsl3", 0) > 100 else
            "[bold #00ff41 on #003300] SECURE [/]"
        )

        self.console.print(Panel(
            threat_table,
            title="[bold #ff5555] ShodanX EXPOSURE INTELLIGENCE [/]",
            border_style="bold #ff00ff",
            padding=(1, 2)
        ))

        self.console.print(Panel(
            port_table,
            title="[bold #00ffff] PORT VULNERABILITY ANALYSIS [/]",
            border_style="bold #00ffff")
        )

        self.console.print(Panel(
            crypto_table,
            title="[bold #ffff00] CRYPTOGRAPHIC WEAKNESSES ANALYSIS [/]",
            border_style="bold #ffff00")
        )

        self.console.print(Panel.fit(
            threat_level,
            title="[bold white] SYSTEM THREAT LEVEL [/]",
            border_style="bold red" if critical_count > 0 else "bold yellow"
        ))
