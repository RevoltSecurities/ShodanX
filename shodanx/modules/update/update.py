import requests
from colorama import Fore, Style
import subprocess
import os
from alive_progress import alive_bar

bold =Style.BRIGHT
blue = Fore.BLUE
red  = Fore.RED
white = Fore.WHITE
reset = Style.RESET_ALL


def get_zip(username): #fetching the latest zip file to update
    
    try:
        
        url = "https://api.github.com/repos/sanjai-AK47/ShodanX/releases/latest"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            
            return response.json()['zipball_url']
        
        else:
            
            print(f"[{bold}{red}ALERT{reset}]: {bold}{white}Hey {username} Update Failed for Shodanx, Please try to update the ShodanX manually{reset}")
            
            quit()
        
        
    except Exception as e:
        
        pass
    


def get_latest(url, username, path): #updating our shodanX to its latest version then called the verify for version
    
    try:
    
    
        response = requests.get(url, timeout=20, stream=True)
        
        filepath = f"{path}/shodanX.zip"
    
        if response.status_code == 200:
            
            print(f"[{bold}{blue}INFO{reset}]: {bold}{white}Hey {username}, Updating ShodanX please wait..{reset}")
    
            with open(f"{filepath}", "wb") as streamw:
            
                for data in response.iter_content():
                
                    if data:
                    
                        streamw.write(data)
                        
            try:
                            
                subprocess.run(["pip", "install", f"{filepath}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                os.remove(filepath)
                            
            except Exception as e:
                            
                print(f"[{bold}{red}ALERT{reset}]: {bold}{white}Hey {username} Update Failed for Shodanx, Please try to update the ShodanX manually{reset}")
                        
                quit()
                                    
        else:
            
            print(f"[{bold}{red}ALERT{reset}]: {bold}{white}Hey {username} Update Failed for Shodanx, Please try to update the ShodanX manually{reset}")
            
            quit()
            
    except Exception as e:
        
        pass
                    

    
def updatelog(config, username): #atlast after update
    
    try:
        url = f"https://raw.githubusercontent.com/sanjai-AK47/ShodanX/main/.github/workflows/updatelog"
        
        response = requests.get(url, timeout=20, stream=True)
        
        info = f"{config}/updatelog.py"
        
        if response.status_code == 200:
            
            with open(info, "wb") as streamw:
                
                for content in response.iter_content():
                    
                    if content:
                    
                        streamw.write(content)       
                
            try:
                            
                subprocess.run(["python3",  f"{info}"], check=True)
                
                os.remove(info)
                            
            except Exception as e:
                            
                print(f"[{bold}{red}ALERT{reset}]: {bold}{white}Hey {username} unable to fetch update logs so please visit here --> http://github.com/sanjai-AK47/ShodanX{reset}")
                        
                quit()
                
    except Exception as e:
        
        pass
    