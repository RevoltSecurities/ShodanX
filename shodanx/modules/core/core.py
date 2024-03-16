import aiohttp
import asyncio
import aiofiles
from colorama import Fore, Style, Back
from bs4 import  XMLParsedAsHTMLWarning, MarkupResemblesLocatorWarning, BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
from fake_useragent import UserAgent
import warnings
import os

red =  Fore.RED

green = Fore.GREEN

magenta = Fore.MAGENTA

cyan = Fore.CYAN

mixed = Fore.RED + Fore.BLUE

blue = Fore.BLUE

yellow = Fore.YELLOW

white = Fore.WHITE

lm = Fore.LIGHTMAGENTA_EX

reset = Style.RESET_ALL

bold = Style.BRIGHT


async def save(url, output):
    
    try:
        
        
            if output:
        
        
            
                if os.path.isfile(output):
                
                    filename = output
                
                elif os.path.isdir(output):
                
                    filename = os.path.join(output, f"ShodanX_results.txt")
                
                else:
                
                    filename = output
                    
            else:
               
                
                    filename = "shodanX_results.txt"
                
        
            async with aiofiles.open(filename, "a") as w:
                
                    await w.write(url + '\n')

    except KeyboardInterrupt as e:
        
        
        print(f"\n[{bold}{blue}INFO{reset}]: {bold}{white}ShodanX exits{reset}")
        
        quit()
        
    except asyncio.CancelledError as e:
        
        
        SystemExit

async def core_request(query, facet, agents, timeout, redirects, username, output):
    
    try:
        
        total = []
        
        url = f"https://www.shodan.io/search/facet?query={query}&facet={facet}"
        
        if agents:
            
            agent = UserAgent()
            
        else:
            
            agent = "ShodanX+https://github.com/sanjai-AK47/ShodanX"
            
        headers = {'User-Agent': agent}
        
        redirect = True if redirects else False
        
        
        async with aiohttp.ClientSession() as session:
            
            async with session.get(url, ssl=False, timeout=timeout, allow_redirects=redirect, headers=headers) as response:
                
                responsed = await response.text()
                
                
                with warnings.catch_warnings():
                
                
                    warnings.filterwarnings("ignore", category=UserWarning)
                    
                    warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)
                    
                    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
                    
                    soup = BeautifulSoup(responsed, "lxml")
                    
                    results = soup.find_all('strong')
                    
                    for result in results:
                        
                        total.append(result.get_text())
                        
                    if len(total) == 0:
                        
                        print(f"[{bold}{red}ALERT{reset}]: {bold}{white}Sorry {username} There is no data available for your queries and facet in shodan{reset}")
        
                        quit()
                        
                    
                    print(f"""[{bold}{blue}INFO{reset}]: {bold}{white}Results Found for your query and facet: {query} & facet:"{facet}"{reset}""")
                    
                    
                    for result in total:
                        
                        
                        print(f"[{bold}{blue}INFO{reset}]: {bold}{white}{result}{reset}")
                        
                        await save(result, output)
                        
                    print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Total Results Found: {len(total)}{reset}")
                        
                        
    except KeyboardInterrupt as e:
        
        print(f"[{blue}INFO{reset}]: {bold}{white}ShodanX exits..{reset}")
        
        SystemExit
        
    except aiohttp.ClientConnectionError as e:         
        
            print(f"[{bold}{red}INFO{reset}]: {bold}{white}Client Connection Exceeds for: {url} , {username} please try again your query{reset}")
            
    except asyncio.TimeoutError as e:
        
            print(f"[{bold}{red}INFO{reset}]: {bold}{white}Client Timeout Exceeds for: {url}, {username} please try again your query{reset}")
            
    except asyncio.CancelledError as e:
        
        SystemExit
        
    except Exception as e:
        
        pass
                        
                        
                        
                        