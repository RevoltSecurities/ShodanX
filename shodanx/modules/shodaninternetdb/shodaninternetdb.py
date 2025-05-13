from shodanx.modules.shodaninternetdb.shodanresolver import ShodanXDNSResolver
import httpx
from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils
from shodanx.modules.shodanxsave.shodanxsave import ShodanxSave
from rich.console import Console
from rich.panel import Panel
from typing import List, Dict, Optional
from rich.table import Table
from rich.text import Text
from rich.box import DOUBLE_EDGE


class ShodanxInternetDB():
    def __init__(self, session: httpx.AsyncClient, domain: str = None, output: str=None):
        self.domain = domain
        self.output = output
        self.session = session
        self.logger = Logger()
        self.console = Console()
        self.saver = ShodanxSave(self.logger)
        self._shodan_utils = ShodanxUtils()
        self._shodan_url = "https://internetdb.shodan.io"
        self.results = []
        
    async def search(self, ip: str) -> dict:
        try:
            url = f"{self._shodan_url}/{ip}"
            response: httpx.Response = await self.session.request("GET", url, timeout=30)
            if response.status_code != 200:
                return None
            data = response.json()
            return {
                'ip': data['ip'],
                'ports': data.get('ports', []),
                'cpes': data.get('cpes', []),
                'hostnames': data.get('hostnames', []),
                'tags': data.get('tags', []),
                'vulns': data.get('vulns', [])
            }
        except Exception as e:
            self.logger.warn(f"Error occurred in shodan single search InternetDB module due to: {e}")
            return {}
        
    async def search_all(self, ips: List[str]) -> List[Dict]:
        try:
            results = []
            for ip in ips:
                result = await self.search(ip)
                if result:
                    results.append(result)
                    if self.output:
                        await self.saver.save(self.output,result,True)
                    self._display_single_result(result)
            return results
        except Exception as e:
            self.logger.warn(f"Error occurred in the shodan InternetDB search module due to: {e}")
            return []
        
    async def do(self):
        try:
            shodanresolver = ShodanXDNSResolver()
            ips = await shodanresolver.resolve(self.domain)
            if ips is None:
                return []
            results = await self.search_all(ips)
            if self.output:
                await self.saver.save(self.output, results, True)
            return results
        except Exception as e:
            self.logger.warn(f"Error occurred in the internetdb search do module due to: {e}")
            return []
            
    def _create_port_table(self, result: dict) -> Table:
        table = Table(
            box=DOUBLE_EDGE,
            header_style="bold white",
            expand=True,
            show_lines=True
        )
        
        table.add_column("IP", style="bold cyan", no_wrap=True)
        table.add_column("Port", justify="center")
        table.add_column("Service", style="bold white")
        table.add_column("Service Name", style="bold white")
        table.add_column("Tags", style="bold white")
        
        ip = result['ip']
        hostnames = "\n".join(result['hostnames']) if result['hostnames'] else "N/A"
        
        for port in result['ports']:
            style, service_label = self._shodan_utils.get_port_style_and_service(port)
            service_name = self._shodan_utils.get_service_name(port)
            
            table.add_row(
                f"{ip}\n[bold yellow]{hostnames}[/]",
                Text(str(port), style=style),
                Text(service_label, style=style),
                service_name,
                ", ".join(result['tags']) or "None"
            )
            
        return table

    def _create_vulnerability_table(self, result: dict) -> Optional[Table]:
        if not result['vulns']:
            return None
            
        table = Table(
            box=DOUBLE_EDGE,
            expand=True,
            style="bold white",
            show_lines=True
        )
        
        table.add_column("Vulnerability ID", style="bold green")
        table.add_column("Exposed Ports", style="bold cyan")
        table.add_column("Related CPEs", overflow="fold", style="bold yellow")
        
        for vuln in result['vulns']:
            table.add_row(
                vuln,
                ", ".join(str(p) for p in result['ports']),
                "\n".join(result['cpes'][:3]) + ("..." if len(result['cpes']) > 3 else "")
            )
            
        return table

    def _create_host_summary(self, result: dict) -> Table:
        """Create host summary for a single result"""
        table = Table(
            box=DOUBLE_EDGE,
            header_style="bold blue",
            expand=True,
            style="bold white",
            show_lines=True,
        )
        
        table.add_column("IP", style="bold white")
        table.add_column("Hostnames", overflow="fold", style="bold magenta")
        table.add_column("Open Ports", style="bold blue")
        table.add_column("Unique Services", style="bold cyan")
        table.add_column("Vulnerabilities", style="bold green")
        
        services = {
            self._shodan_utils.get_service_name(port)
            for port in result['ports']
        }
        
        table.add_row(
            result['ip'],
            "\n".join(result['hostnames']) or "None",
            str(len(result['ports'])),
            str(len(services)),
            str(len(result['vulns'])) + " found" if result['vulns'] else "None"
        )
        return table

    def _display_single_result(self, result: dict):
        """Display all visualizations for a single IP result"""
        if not result:
            return
            
        self.console.print(Panel.fit(
            self._create_host_summary(result),
            title=f"[bold green]Target Summary for {result['ip']}[/]",
            border_style="green",
        ))
        
        self.console.print(Panel.fit(
            self._create_port_table(result),
            title=f"[bold blue]Port Analysis for {result['ip']}[/]",
            border_style="blue"
        ))
        
        vuln_table = self._create_vulnerability_table(result)
        if vuln_table:
            self.console.print(Panel.fit(
                vuln_table,
                title=f"[bold red]Vulnerabilities Found for {result['ip']}[/]",
                border_style="bold white"
            ))
        else:
            self.console.print(f"[bold red]No vulnerabilities found for {result['ip']}[/]")
        print("\n")

    def display_results(self, results: List[Dict] = None):
        display_results = results or self.results
        if not display_results:
            return
            
        self.console.print(Panel.fit(
            self._create_aggregate_host_summary(display_results),
            title="[bold green]Target Summary[/]",
            border_style="green",
        ))
        
        self.console.print(Panel.fit(
            self._create_aggregate_port_table(display_results),
            title="[bold blue]Port Analysis[/]",
            border_style="blue"
        ))
        
        vuln_table = self._create_aggregate_vulnerability_table(display_results)
        if vuln_table:
            self.console.print(Panel.fit(
                vuln_table,
                title="[bold green]Vulnerabilities Found[/bold green]",
                border_style="bold white"
            ))
        else:
            self.console.print("[bold red]No vulnerabilities found in InternetDB data[/bold red]")

    def _create_aggregate_host_summary(self, results: List[Dict]) -> Table:
        table = Table(
            box=DOUBLE_EDGE,
            header_style="bold blue",
            expand=True,
            style="bold white",
            show_lines=True,
        )
        
        table.add_column("IP", style="bold white")
        table.add_column("Hostnames", overflow="fold", style="bold magenta")
        table.add_column("Open Ports", style="bold blue")
        table.add_column("Unique Services", style="bold cyan")
        table.add_column("Vulnerabilities", style="bold green")
        
        for result in results:
            services = {
                self._shodan_utils.get_service_name(port)
                for port in result['ports']
            }
            
            table.add_row(
                result['ip'],
                "\n".join(result['hostnames']) or "None",
                str(len(result['ports'])),
                str(len(services)),
                str(len(result['vulns'])) + " found" if result['vulns'] else "None"
            )
        return table

    def _create_aggregate_port_table(self, results: List[Dict]) -> Table:
        table = Table(
            box=DOUBLE_EDGE,
            header_style="bold white",
            expand=True,
            show_lines=True
        )
        
        table.add_column("IP", style="bold cyan", no_wrap=True)
        table.add_column("Port", justify="center")
        table.add_column("Service", style="bold white")
        table.add_column("Service Name", style="bold white")
        table.add_column("Tags", style="bold white")
        
        for result in results:
            ip = result['ip']
            hostnames = "\n".join(result['hostnames']) if result['hostnames'] else "N/A"
            
            for port in result['ports']:
                style, service_label = self._shodan_utils.get_port_style_and_service(port)
                service_name = self._shodan_utils.get_service_name(port)
                
                table.add_row(
                    f"{ip}\n[bold yellow]{hostnames}[/]",
                    Text(str(port), style=style),
                    Text(service_label, style=style),
                    service_name,
                    ", ".join(result['tags']) or "None"
                )
                
        return table

    def _create_aggregate_vulnerability_table(self, results: List[Dict]) -> Optional[Table]:
        vuln_data = []
        for result in results:
            if result['vulns']:
                for vuln in result['vulns']:
                    vuln_data.append({
                        'ip': result['ip'],
                        'vulnerability': vuln,
                        'ports': ", ".join(str(p) for p in result['ports']),
                        'cpes': "\n".join(result['cpes'][:3]) + ("..." if len(result['cpes']) > 3 else "")
                    })
        
        if not vuln_data:
            return None
            
        table = Table(
            box=DOUBLE_EDGE,
            expand=True,
            style="bold white",
            show_lines=True
        )
        
        table.add_column("IP", style="bold white")
        table.add_column("Vulnerability ID", style="bold green")
        table.add_column("Exposed Ports", style="bold cyan")
        table.add_column("Related CPEs", overflow="fold", style="bold yellow")
        
        for vuln in vuln_data:
            table.add_row(
                vuln['ip'],
                vuln['vulnerability'],
                vuln['ports'],
                vuln['cpes']
            )
            
        return table