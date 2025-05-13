## ShodanX⚡ – A terminal-powered recon and OSINT tool built on top of the Shodan Services.

<h1 align="center">
  <img src="static/Shodanx.png" alt="shodanx" width="450px" height="500px">
  <br>
</h1>


<p align="center">
    <a href="https://github.com/RevoltSecurities/shodanx?tab=readme-ov-file#features">Features</a> |
    <a href="https://github.com/RevoltSecurities/shodanx?tab=readme-ov-file#installation">Installation</a> |
    <a href="https://github.com/RevoltSecurities/shodanx?tab=readme-ov-file#usage">Usage</a> |
    <a href="https://github.com/RevoltSecurities/shodanx?tab=readme-ov-file#post-installation">Post Installation Setup</a>
</p>

![GitHub last commit](https://img.shields.io/github/last-commit/RevoltSecurities/ShodanX) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/RevoltSecurities/shodanX) [![GitHub license](https://img.shields.io/github/license/RevoltSecurities/ShodanX)](https://github.com/RevoltSecurities/ShodanX/blob/main/LICENSE)


### Features🔧:
---

<h1 align="center">

<img src="https://github.com/RevoltSecurities/shodanx">
<br>
</h1>


* `🔐 shodanx auth` – Configure and store your Shodan API key securely.
* `🔓 shodanx login` – Validate your access level and API key status.
* `🏢 shodanx org` – Perform organization-wide scans using Shodan’s powerful facets.
* `🌐 shodanx domain` – Enumerate domain-related metadata, open ports, and host exposures.
* `📡 shodanx subdomain` – Discover passive subdomains via Shodan’s DNS intel.
* `🔒 shodanx ssl` – Track reused or expired SSL certificates via fingerprint searches.
* `🎯 shodanx custom` – Run advanced Shodan dorks and custom filter queries.
* `📦 shodanx internetdb` – Use Shodan’s lightweight InternetDB for quick IP/domain analysis.
* `🗺️ shodanx map` – Visualize geographic distribution of exposed services and ports.
* `🧬 shodanx cvedb` – Map hosts to known vulnerabilities using the CVE database.
* `🏭 shodanx entitydb` – Explore technologies, software, and vendors across exposed systems.
* `🌍 shodanx exposuredb` – Identify publicly exposed assets and data leaks by country.
* `🖼️ shodanx faviconmap` – Track systems by unique favicons for lateral discovery.
* `📈 shodanx trends` – Analyze exposure trends over time (Enterprise access required).

---


## Installation🚀

shodanx can be easily installed using **pip**


```bash
pip install git+https://github.com/RevoltSecurities/ShodanX --break-system-packages
```

> ✅ Make sure you have Python 3.13 or newer installed.  

  
### Usage:
---
```code
shodanx -h
```

```yaml
   _____    __                __                   _  __
  / ___/   / /_   ____   ____/ /  ____ _   ____   | |/ /
  \__ \   / __ \ / __ \ / __  /  / __ `/  / __ \  |   / 
 ___/ /  / / / // /_/ // /_/ /  / /_/ /  / / / / /   |  
/____/  /_/ /_/ \____/ \__,_/   \__,_/  /_/ /_/ /_/|_|  
                                                        

                     - RevoltSecurities

╭───────────────────────╮
│                       │
│    SHODANX ⚡ HELP    │
│                       │
╰───────────────────────╯
DESCRIPTION

ShodanX is a terminal-powered recon and OSINT tool built on top of the Shodan Services.
It empowers ethical hackers and red teamers to identify exposed infrastructure,
search CVEs, map attack surfaces, and run internet-wide queries in real time.

MODES (shodanx <mode>)

┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Mode       ┃ Description                                                      ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ auth       │ Configure and save your Shodan API key for authenticated access. │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ login      │ Verify your ShodanX access level and API key validity.           │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ org        │ Perform organization-wide scans using Shodan facets.             │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ domain     │ Enumerate metadata, ports, and host exposure for a domain.       │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ subdomain  │ Discover passive subdomains using Shodan’s DNS data.             │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ ssl        │ Search by SSL fingerprint to track reused/expired certs.         │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ custom     │ Execute advanced queries using Shodan filters and dorks.         │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ internetdb │ Lightweight analysis of IPs/domains via Shodan InternetDB API.   │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ map        │ Visualize geo-distribution of exposed services and ports.        │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ cvedb      │ Identify vulnerable systems via Shodan’s CVE database.           │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ entitydb   │ Explore technologies/vendors via Shodan’s EntityDB.              │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ exposuredb │ Discover globally exposed assets and leaks by country.           │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ faviconmap │ Find systems using specific favicons via Shodan FaviconMap.      │
├────────────┼──────────────────────────────────────────────────────────────────┤
│ trends     │ View historical exposure trends (Shodan Enterprise required).    │
└────────────┴──────────────────────────────────────────────────────────────────┘
FLAGS
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Flag       ┃ Description                      ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ -h, --help │ Show this help message and exit. │
└────────────┴──────────────────────────────────┘
USAGE
shodanx <mode> 

DETAILS
 shodanx auth        → Configure and save your Shodan API key for authenticated access. 
 shodanx login       → Verify your ShodanX access level and API key validity.           
 shodanx org         → Perform organization-wide scans using Shodan facets.             
 shodanx domain      → Enumerate metadata, ports, and host exposure for a domain.       
 shodanx subdomain   → Discover passive subdomains using Shodan’s DNS data.             
 shodanx ssl         → Search by SSL fingerprint to track reused/expired certs.         
 shodanx custom      → Execute advanced queries using Shodan filters and dorks.         
 shodanx internetdb  → Lightweight analysis of IPs/domains via Shodan InternetDB API.   
 shodanx map         → Visualize geo-distribution of exposed services and ports.        
 shodanx cvedb       → Identify vulnerable systems via Shodan’s CVE database.           
 shodanx entitydb    → Explore technologies/vendors via Shodan’s EntityDB.              
 shodanx exposuredb  → Discover globally exposed assets and leaks by country.           
 shodanx faviconmap  → Find systems using specific favicons via Shodan FaviconMap.      
 shodanx trends      → View historical exposure trends (Shodan Enterprise required).

```

### Post Installation:

Once you've successfully installed `shodanx`, follow these quick steps to get fully authenticated and ready to scan:

### 1. 🔑 Authenticate Your Shodan API Key

Start by running the `auth` command to securely store your credentials:

```bash
shodanx auth
```

You'll be prompted to enter:

* **Username** – for local session identification
* **Password** – used for encrypting your local credentials
* **Shodan API Key** – required for authenticated access to most Shodan services

> ✅ **Security Note:** All your sensitive inputs (username, password, API key) are securely stored in your local user shodanx configuration file. No external calls or storage are involved during this setup.

### 2. 🧠 Session Login via Shodan Web Cookie

Next, run the `login` command to authenticate against Shodan’s session-protected endpoints:

```bash
shodanx login
```

You'll be asked to paste your **active Shodan session cookie** (copied as a single string) from:

* Browser Dev Tools → Application → Cookies → `.shodan.io`
* OR intercept it via **Burp Suite** / **Proxy tools**

Paste the session string when prompted. This is used for advanced session-based features.


### 3. 🚀 You're Ready!

You now have access to the full `shodanx` suite of modules.

> 💡 **Note:** Certain modules like `trends`  require a **Shodan Enterprise** API key for access to premium data visualizations and trend insights and `map` require a **Shodan's** high level subscription account cookie 

---


## Acknowledgements

**ShodanX** is built with ❤️ by **[RevoltSecurities](https://github.com/RevoltSecurities)** — for hackers, by hackers.

We deeply appreciate all the users who trust ShodanX for automating and enhancing their cybersecurity workflows. Your usage, feedback, and support drive the continued evolution of this powerful tool.
Thank you for choosing ShodanX to power your recon, enumeration, and exploitation efforts.

> Stay ethical. Stay sharp. Stay ahead.
> — *With respect, the RevoltSecurities*
---
