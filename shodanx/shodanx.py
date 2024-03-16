from colorama import Fore,Style 
import click
from bs4 import BeautifulSoup
import time as t
import warnings
import random
import sys
import requests 
import asyncio
import time
warnings.simplefilter('ignore', requests.packages.urllib3.exceptions.InsecureRequestWarning)

warnings.filterwarnings("ignore")

red =  Fore.RED

green = Fore.GREEN

magenta = Fore.MAGENTA

cyan = Fore.CYAN

mixed = Fore.RED + Fore.BLUE

blue = Fore.BLUE

yellow = Fore.YELLOW

white = Fore.WHITE

reset = Style.RESET_ALL

bold = Style.BRIGHT

colors = [ green, cyan, blue]

random_color = random.choice(colors)

settings = dict(help_option_names=['-h', '--help'])

try:
    
    from .modules.version.version import *
    
    from .modules.core.core import core_request
    
    from .modules.help.help import *
    
    from .modules.banner.banner import banner
    
    from .modules.user.user import get_username
    
except ImportError as e:
    
    print(f"[{bold}{red}INFO{reset}]: {bold}{white}Import Error occured in Module imports due to: {e}{reset}")
    
    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}If you are encountering this issue more than a time please report the issues in ShodanX Github page.. {reset}")
    
    exit()
    

def version():
    
    latest = check_version()
    
    version = "v1.0.0"
    
    if latest == version:
        
        print(f"[{blue}{bold}Version{reset}]:{bold}{white}ShodanX current version {version} ({green}latest{reset}{bold}{white}){reset}")
        
    else:
        
        print(f"[{blue}{bold}Version{reset}]: {bold}{white}ShodanX current version {version} ({red}outdated{reset}{bold}{white}){reset}")
     
    
brand = banner()


username = get_username()

def customizer(ctx, param, value): 
    
    if value and not ctx.resilient_parsing:
        
        if not ctx.invoked_subcommand:
            
            print(f"{random_color}{brand}{reset}")
            
            mode_help()
            
        else:
            
            ctx.invoke(ctx.command, ['--help'])
            
            
print(f"{bold}{white}")

@click.group(context_settings=settings)

@click.option("-h", "--help", is_flag=True, is_eager=True, expose_value=False, callback=customizer)

def cli():
    
    pass

@cli.command()
                

@click.option("-h", "--help", is_flag=True)

@click.option("-org", "--organization", type=str)

@click.option("-fct", "--facet", type=str, default="ip")

@click.option("-o", "--output", type=str)

@click.option("-ra", "--random-agent", is_flag=True)

@click.option("-to", "--timeout", type=int, default=10)

@click.option("-r", "--redirect", is_flag=True)

def org(help, organization, facet, output, random_agent, timeout, redirect):
    
    click.echo(f"{bold}{random_color}{brand}{reset}")
    
    version()
    
    if help:
        
        org_mode_help()
        
        quit()
        
    if not organization:
        
        click.echo(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username} Please provide -org value for ShodanX and Please refer the help menu below{reset}")
        
        time.sleep(1.5)
        
        org_mode_help()
        
        quit()
        
    asyncio.run(core_request(f'org:"{organization}"', facet, random_agent, timeout, redirect, username, output))
    


@cli.command()
                
@click.option("-h", "--help", is_flag=True)

@click.option("-d", "--domain", type=str)

@click.option("-fct", "--facet", type=str, default="ip")

@click.option("-o", "--output", type=str)

@click.option("-ra", "--random-agent", is_flag=True)

@click.option("-to", "--timeout", type=int, default=10)

@click.option("-r", "--redirect", is_flag=True)

def domain(help, domain, facet, output, random_agent, timeout, redirect):
    
    click.echo(f"{bold}{random_color}{brand}{reset}")
    
    version()
    
    if help:
        
        dom_mode_help()
        
        quit()
        
    if not domain:
        
        click.echo(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username} Please provide -d or --domain value for ShodanX and Please refer the help menu below{reset}")
        
        time.sleep(1.5)
        
        dom_mode_help()
        
        quit()
        
    asyncio.run(core_request(f'hostname:"{domain}"', facet, random_agent, timeout, redirect, username, output))
    


@cli.command()
                

@click.option("-h", "--help", is_flag=True)

@click.option("-sq", "--ssl-query", type=str)

@click.option("-fct", "--facet", type=str, default="ip")

@click.option("-o", "--output", type=str)

@click.option("-ra", "--random-agent", is_flag=True)

@click.option("-to", "--timeout", type=int, default=10)

@click.option("-r", "--redirect", is_flag=True)

def ssl(help, ssl_query, facet, output, random_agent, timeout, redirect):
    
    click.echo(f"{bold}{random_color}{brand}{reset}")
    
    version()
    
    if help:
        
        ssl_mode_help()
        
        quit()
        
    if not ssl_query:
        
        click.echo(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username} Please provide -sq or --ssl-query value for ShodanX and Please refer the help menu below{reset}")
        
        time.sleep(1.5)
        
        ssl_mode_help()
        
        quit()
        
    asyncio.run(core_request(f'{ssl_query}', facet, random_agent, timeout, redirect, username, output))
    
    

@cli.command()
                

@click.option("-h", "--help", is_flag=True)

@click.option("-cq", "--custom-query", type=str)

@click.option("-fct", "--facet", type=str, default="ip")

@click.option("-o", "--output", type=str)

@click.option("-ra", "--random-agent", is_flag=True)

@click.option("-to", "--timeout", type=int, default=10)

@click.option("-r", "--redirect", is_flag=True)

    
def custom(help, custom_query, facet, output, random_agent, timeout, redirect):
    
    click.echo(f"{bold}{random_color}{brand}{reset}")
    
    version()
    
    if help:
        
        org_mode_help()
        
        quit()
        
    if not custom_query:
        
        click.echo(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username} Please provide -sq or --ssl-query value for ShodanX and Please refer the help menu below{reset}")
        
        time.sleep(1.5)
        
        ssl_mode_help()
        
        quit()
        
    asyncio.run(core_request(f'{custom_query}', facet, random_agent, timeout, redirect, username, output))
    
    
@cli.command()

@click.option("-lt", "--latest", is_flag=True)

@click.option("-h", "--help", is_flag=True)


def update(latest, help):
    
    click.echo(f"{random_color}{brand}{reset}")
    
    if help:
        
        update_mode_help()
        
    
    latests = "1.0.0"
    
    version = check_version()
    
    if latests == version:
        
        click.echo(f"[{bold}{white}INFO{reset}]: {bold}{white}Hey {username} ShodanX is already in latest version{reset}")
        
    else:
        
        click.echo(f"[{bold}{blue}INFO{reset}]: {bold}{white}Updating ShodanX latest version from git.{reset}") 
        
        os.system(f"pip install git+https://github.com/sanjai-AK47/ShodanX.git")
        
        click.echo(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username} ShodanX is updated successfully , Please check it once manually.{reset}")
        
        
if __name__ == "__main__":
    
    cli()