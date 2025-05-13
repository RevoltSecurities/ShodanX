from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

class Helper:
    def __init__(self) -> None:
        self.console = Console()
        
    def main_help(self):
        self.console.print(Panel.fit(
            Text("SHODANX ⚡ HELP", justify="center", style="bold blue"),
            border_style="blue",
            padding=(1, 4)
        ))

        self.console.print("[bold blue]DESCRIPTION[/bold blue]")
        self.console.print(
            "[bold white]\nShodanX is a terminal-powered recon and OSINT tool built on top of the Shodan Services.\n"
            "It empowers ethical hackers and red teamers to identify exposed infrastructure,\n"
            "search CVEs, map attack surfaces, and run internet-wide queries in real time.\n[/bold white]"
        )

        self.console.print("[bold blue]MODES (shodanx <mode>)[/bold blue]\n")
        mode_table = Table(show_header=True, header_style="bold magenta", show_lines=True)
        mode_table.add_column("Mode", style="bold cyan", no_wrap=True)
        mode_table.add_column("Description", style="bold white")

        modes = [
            ("auth", "Configure and save your Shodan API key for authenticated access."),
            ("login", "Verify your ShodanX access level and API key validity."),
            ("org", "Perform organization-wide scans using Shodan facets."),
            ("domain", "Enumerate metadata, ports, and host exposure for a domain."),
            ("subdomain", "Discover passive subdomains using Shodan’s DNS data."),
            ("ssl", "Search by SSL fingerprint to track reused/expired certs."),
            ("custom", "Execute advanced queries using Shodan filters and dorks."),
            ("internetdb", "Lightweight analysis of IPs/domains via Shodan InternetDB API."),
            ("map", "find exposed services and ports using Shodan Map"),
            ("cvedb", "Find new and CVE infromations via Shodan’s CVE database."),
            ("entitydb", "Explore technologies/vendors via Shodan’s EntityDB."),
            ("exposuredb", "Discover globally exposed assets and leaks by country."),
            ("faviconmap", "Find systems using specific favicons via Shodan FaviconMap."),
            ("trends", "View historical exposure trends (Shodan Enterprise required)."),
        ]
        for mode, desc in modes:
            mode_table.add_row(mode, desc)
        self.console.print(mode_table)

        self.console.print("[bold blue]FLAGS[/bold blue]")
        flag_table = Table(show_header=True, header_style="bold magenta")
        flag_table.add_column("Flag", style="bold cyan", no_wrap=True)
        flag_table.add_column("Description", style="bold white")
        flag_table.add_row("-h, --help", "Show this help message and exit.")
        self.console.print(flag_table)

        self.console.print("[bold blue]USAGE[/bold blue]")
        self.console.print("[bold white]shodanx <mode> [options][/bold white]\n")

        self.console.print("[bold blue]DETAILS[/bold blue]")
        detail_table = Table(show_header=False, box=None)
        for mode, desc in modes:
            detail_table.add_row(f"[bold white]shodanx[/] [bold cyan]{mode}[/]", f"[bold white]→ {desc}[/]")
        self.console.print(detail_table)

    def _print_mode_help(self, title: str, description: str, flags: list):
        self.console.print(Panel.fit(
            Text(title, justify="center", style="bold blue"),
            border_style="blue",
            padding=(1, 4)
        ))
        self.console.print(f"[bold blue]DESCRIPTION[/bold blue]\n[bold white]{description}[/bold white]\n")

        self.console.print("[bold blue]FLAGS[/bold blue]")
        flag_table = Table(show_header=True, header_style="bold magenta")
        flag_table.add_column("Flag", style="bold cyan", no_wrap=True)
        flag_table.add_column("Description", style="bold white")
        for flag, desc in flags:
            flag_table.add_row(flag, desc)
        self.console.print(flag_table)

    def help_org(self):
        self._print_mode_help(
            "ORG MODE",
            "Perform organization-wide scans using Shodan facets.",
            [
                ("--organization, -org", "Name of the target organization to investigate."),
                ("--facet, -fct", "Group results by a facet like 'ip', 'asn', or 'country'. Default is 'ip'."),
                ("--output, -o", "Specify output file to save results in JSON format."),
                ("--verbose, -v", "Enable detailed logs during execution.")
            ]
        )

    def help_domain(self):
        self._print_mode_help(
            "DOMAIN MODE",
            "Enumerate metadata, ports, and host exposure for a domain.",
            [
                ("--domain, -domain", "Domain name to scan for public exposure."),
                ("--facet, -fct", "Group results by facet such as 'port' or 'org'. Default is 'ip'."),
                ("--output, -o", "Save output to a file in structured JSON.")
            ]
        )

    def help_ssl(self):
        self._print_mode_help(
            "SSL MODE",
            "Search by SSL fingerprint to track reused/expired certs.",
            [
                ("--ssl-query, -sq", "SSL hash or certificate fingerprint to search."),
                ("--facet, -fct", "Group SSL certs by facet (e.g. org, product, port)."),
                ("--output, -o", "Path to file where results will be saved.")
            ]
        )

    def help_custom(self):
        self._print_mode_help(
            "CUSTOM MODE",
            "Execute advanced queries using Shodan filters and dorks.",
            [
                ("--custom-query, -cq", "Custom query using Shodan filters like 'port:80 country:IN'."),
                ("--facet, -fct", "Group matched data using facets like 'asn', 'port', etc."),
                ("--output, -o", "Output file to store query results.")
            ]
        )

    def help_subdomain(self):
        self._print_mode_help(
            "SUBDOMAIN MODE",
            "Discover passive subdomains using Shodan’s DNS data.",
            [
                ("--domain, -d", "Domain to extract subdomains from (e.g. example.com)."),
                ("--output, -o", "Save discovered subdomains to file."),
                ("--verbose, -v", "Enable detailed logging and subdomain count.")
            ]
        )

    def help_cvedb(self):
        self._print_mode_help(
            "CVEDB MODE",
            "Identify vulnerable systems via Shodan’s CVE database.",
            [
                ("--cpe, -cpe", "Common Platform Enumeration (CPE) string to filter results."),
                ("--product, -product", "Target product name (e.g., apache, nginx)."),
                ("--cve, -cve", "Specific CVE ID to search affected systems."),
                ("--exploited, -exploited", "Only show systems confirmed as exploited."),
                ("--start-date, -sd", "Filter results starting from this date (YYYY-MM-DD)."),
                ("--end-date, -ed", "Filter results ending at this date (YYYY-MM-DD)."),
                ("--limits, -l", "Limit number of results. Default is 1000."),
                ("--output, -o", "Save the found CVE results in a give file (only support JSON format)"),
            ]
        )

    def help_entitydb(self):
        self._print_mode_help(
            "ENTITYDB MODE",
            "Explore technologies/vendors via Shodan’s EntityDB.",
            [
                ("--id, -id", "Vendor or technology name/ID to investigate.")
            ]
        )

    def help_exposuredb(self):
        self._print_mode_help(
            "EXPOSUREDB MODE",
            "Discover globally exposed assets and leaks by country.",
            [
                ("--country, -country", "country name to search from the shodan exposure database")
            ]
        )

    def help_faviconmap(self):
        self._print_mode_help(
            "FAVICONMAP MODE",
            "Find systems using specific favicons via Shodan FaviconMap.",
            [
                ("--top, -top", "Limit results to top N most common favicons (default: 500)."),
                ("--all, -all", "Return all favicon matches regardless of count.")
            ]
        )

    def help_internetdb(self):
        self._print_mode_help(
            "INTERNETDB MODE",
            "Lightweight analysis of IPs/domains via Shodan InternetDB API.",
            [
                ("--domain, -d", "Domain to gather InternetDB intelligence data."),
                ("--output, -o", "Save summary output to a file."),
                ("--ips, -ips", "Comma-separated list of IPs to analyze (e.g. 1.1.1.1,8.8.8.8).")
            ]
        )

    def help_auth(self):
        self._print_mode_help(
            "AUTH MODE",
            "Configure and save your Shodan API key.",
            []
        )

    def help_login(self):
        self._print_mode_help(
            "LOGIN MODE",
            "Verify your ShodanX access level and API key validity and session cookies validity",
            []
        )

    def help_trends(self):
        self._print_mode_help(
            "TRENDS MODE",
            "View historical exposure trends (Shodan Enterprise API Key required).",
            [
                ("--query, -query", "Search term for trend analysis."),
                ("--facet, -fct", "Facet used for historical grouping (e.g. org, port)."),
                ("--output, -o", "Save output trends to a file."),
                ("--help, -h", "Display this help message for the trends mode.")
            ]
        )

    def help_map(self):
        self._print_mode_help(
            "MAP MODE",
            "Visualize geo-distribution of exposed services and ports.",
            [
                ("--place, -place", "Geographical target area (e.g. city, country, continent)."),
                ("--output, -o", "Path to output image or file."),
                ("--help, -h", "Display this help message for the map mode.")
            ]
        )

    def help_update(self):
        
        self._print_mode_help(
            "UPDATE MODE",
            "Handles the Updates & Updates information of ShodanX",
            [
                ("--show-updates, -sup", "shows the latest version updates information"),
                ("--update, -up", "updates the shodanx to latest version"),
                ("--help, -h", "Display this help message for the map mode.")
            ]
        )