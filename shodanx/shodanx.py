import asyncio
import click
import httpx
from shodanx.modules.logger.logger import Logger
from shodanx.modules.shodanconfig.shodanconfig import ShodanxConfig
from shodanx.modules.help.help import Helper
from shodanx.modules.shodanauth.shodanauth import ShodanAuth
from shodanx.modules.shodancvedb.shodancvedb import ShodanxCVEDB
from shodanx.modules.shodanentity.shodanentity import ShodanxEntityDB
from shodanx.modules.shodanexposure.shodanexposure import ShodanExposureDB
from shodanx.modules.shodanfaviconmap.shodanfaviconmap import ShodanFaviconMap
from shodanx.modules.shodaninternetdb.shodaninternetdb import ShodanxInternetDB
from shodanx.modules.shodanmaps.shodanmaps import ShodanxMapsOSINT
from shodanx.modules.shodansearch.shodansearch import ShodanXWebSearch
from shodanx.modules.shodansubdomain.shodansubdomain import ShodanXSubdomainEnumerator
from shodanx.modules.shodantrends.shodantrends import ShodanxTrendsDB
from shodanx.modules.shodanutils.shodanutils import ShodanxUtils
from shodanx.modules.shodanxsave.shodanxsave import ShodanxSave
from shodanx.modules.gitutils.gitutils import GitUtils
from shodanx.modules.version.version import Version
from shodanx.modules.banner.banner import Banner
import tempfile
import os
import sys


class ShodanX:
    def __init__(self):
        self.logger = Logger()
        self.utils = ShodanxUtils()
        self.banner = Banner("shodanX")
        self.helps = Helper()
        self.config = ShodanxConfig()
        self.tmpdir = tempfile.gettempdir()
        self.saver = ShodanxSave(self.logger)
        self.git = GitUtils("RevoltSecurities/ShodanX", "shodanx", self.tmpdir)
        self.auth_yaml = self.config.config_auth()
        self.auth_cookie = self.config.config_cookie()
        self.version = Version()
        self.git_version = self.version.version
        self.pypi = self.version.pypi
        self.banner.render()
        self.Version()
    
    def show_help(self):
        self.banner.render()
        self.helps.main_help()
        
    def Version(self):
        async def versions():
            currentgit = await self.git.git_version()
            if not currentgit:
                self.logger.warn("unable to get the latest version of shodanx")
                return
            
            if currentgit == self.git_version:
                print(f"[{self.logger.blue}{self.logger.bold}version{self.logger.reset}]:{self.logger.bold}{self.logger.white}shodanx current version {self.git_version} ({self.logger.green}latest{self.logger.reset}{self.logger.bold}{self.logger.white}){self.logger.reset}", file=sys.stderr)
            else:
                print(f"[{self.logger.blue}{self.logger.bold}version{self.logger.reset}]:{self.logger.bold}{self.logger.white}shodanx current version {self.git_version} ({self.logger.red}outdated{self.logger.reset}{self.logger.bold}{self.logger.white}){self.logger.reset}", file=sys.stderr)
            return
        self._run_async(versions())

    def _run_async(self, coro):
        asyncio.run(coro)
        
    def auth(self,help):
        if help:
            self.helps.help_auth()
            return
        
        async def asyncauth():
            authenticator = ShodanAuth(self.auth_yaml, self.auth_cookie)
            data = await authenticator.shell()
            if data is None:
                self.logger.warn("No data found, please run the auth mode with proper and enter proper credentials")
                return
            setter = await self.utils.set_auth(self.auth_yaml, data.get("username"), data.get("password"), data.get("apikey"))
        self._run_async(asyncauth())
        
    def login(self,help):
        if help:
            self.helps.help_login()
            return

        async def asynclogin():
            async with httpx.AsyncClient(verify=False) as session:
                authenticator = ShodanAuth(self.auth_yaml, self.auth_cookie, session)
                cookies = await authenticator.shell_login()
                if cookies is None:
                    return
                setcookies = await self.utils.set_cookie(self.auth_cookie, cookies)
                self.logger.info("Logging into shodan with configured cookies, please wait :)")
                session = await authenticator.valid_session()
                if session:
                    self.logger.info("Successfully logged into shodan using shodanx authenticator")
                else:
                    self.logger.warn(f"Unable to log into shodan, please check your credenitals or manually set cookies in this file: {self.auth_cookie}")
                return
        self._run_async(asynclogin())
        
    def org(self, help,organization, facet, output, verbose):
        if help:
            self.helps.help_org()
            return
        
        if not organization:
            self.logger.warn("org search mode of shodanx requires organization name to pass!")
            return

        async def asyncorg():
            async with httpx.AsyncClient(verify=False) as session:
                shodansearch = ShodanXWebSearch(query=f'org:"{organization}"', facet=facet, session=session, verbose=verbose)
                response = await shodansearch.search()
                data = response.get("shodan_web_search", None)
                if data is None:
                    self.logger.warn(f"No results found for {organization}")
                    return
                for result in data:
                    self.logger.stdin(result)
                    if output:
                        await self.saver.save(output,result)

        self._run_async(asyncorg())

    def domain(self, help,domain, facet, output):
        if help:
            self.helps.help_domain()
            return
        
        if not domain:
            self.logger.warn("domain search mode requires domain name")
            return

        async def asyncdomain():
            async with httpx.AsyncClient(verify=False) as session:
                shodansearch = ShodanXWebSearch(query=f'hostname:"{domain}"', facet=facet, session=session)
                response = await shodansearch.search()
                data = response.get("shodan_web_search", None)
                if data is None:
                    self.logger.warn(f"No results found for {domain}")
                    return
                for result in data:
                    self.logger.stdin(result)
                    if output:
                        await self.saver.save(output,result)
                    
        self._run_async(asyncdomain())

    def ssl(self,help,query, facet, output):
        if help:
            self.helps.help_ssl()
            return
        
        if not query:
            self.logger.warn("ssl search mode requires a query")
            return

        async def asyncssl():
            async with httpx.AsyncClient(verify=False) as session:
                shodansearch = ShodanXWebSearch(query=query, facet=facet, session=session)
                response = await shodansearch.search()
                data = response.get("shodan_web_search", None)
                if data is None:
                    self.logger.warn(f"No results found for {query}")
                    return
                for result in data:
                    self.logger.stdin(result)
                    if output:
                        await self.saver.save(output,result)

        self._run_async(asyncssl())

    def custom(self, help,query, facet, output):
        if help:
            self.helps.help_custom()
            return
        
        if not query:
            self.logger.warn("custom search mode requires query")
            return

        async def asynccustom():
            async with httpx.AsyncClient(verify=False) as session:
                shodansearch = ShodanXWebSearch(query=query, facet=facet, session=session)
                response = await shodansearch.search()
                data = response.get("shodan_web_search", None)
                if data is None:
                    self.logger.warn(f"No results found for {query}")
                    return
                for result in data:
                    self.logger.stdin(result)
                    if output:
                        await self.saver.save(output,result)

        self._run_async(asynccustom())

    def subdomain(self,help, domain, output, verbose):
        if help:
            self.helps.help_subdomain()
            return
        if not domain:
            self.logger.warn("subdomain search requires domain")
            return

        async def asyncsubdomain():
            async with httpx.AsyncClient(verify=False) as session:
                shodanenum = ShodanXSubdomainEnumerator(domain, verbose=verbose, session=session)
                response = await shodanenum.enumerate()
                data = response.get("shodan_subdomains")
                if data is None:
                    self.logger.warn(f"No subdomains found for {domain}")
                    return
                for result in data:
                    self.logger.stdin(result)
                    if output:
                        await self.saver.save(output,result)

        self._run_async(asyncsubdomain())

    def cvedb(self, help,cpe, product, cve, exploited, start_date, end_date, limits, output):
        if help:
            self.helps.help_cvedb()
            return
        
        async def asynccve():
            async with httpx.AsyncClient(verify=False, follow_redirects=True) as session:
                cvemap = ShodanxCVEDB(session=session, is_kev=exploited, start_date=start_date, end_date=end_date, limit=limits)
                if cpe:
                    data = await cvemap.search(cpe=cpe)
                elif product:
                    data = await cvemap.search(product=product)
                elif cve:
                    data = await cvemap.search_cve_by_id(cve)
                else:
                    data = await cvemap.search()
                    
                if output:
                    await self.saver.save(output,data,True)
                    
        self._run_async(asynccve())

    def entitydb(self,help, id=None):
        if help:
            self.helps.help_entitydb()
            return
        
        async def asyncentitydb():
            async with httpx.AsyncClient(verify=False) as session:
                entitydbs = ShodanxEntityDB(session=session)
                data = await (entitydbs.list_entity_by_id(id) if id else entitydbs.list_all_entities())

        self._run_async(asyncentitydb())

    def exposuredb(self,help, country):
        if help:
            self.helps.help_exposuredb()
            return
        
        if not country:
            self.logger.warn("exposuredb requires country to search")
            return

        async def asyncexposure():
            async with httpx.AsyncClient(verify=False) as session:
                exposures = ShodanExposureDB(country=country, session=session)
                data = await exposures.search_exposure()

        self._run_async(asyncexposure())

    def faviconmap(self, help,top, all):
        if help:
            self.helps.help_faviconmap()
            return
        
        async def asyncfavicon():
            async with httpx.AsyncClient(verify=False) as session:
                favisearch = ShodanFaviconMap(all=all, top=top, session=session)
                data = await favisearch.search()

        self._run_async(asyncfavicon())

    def internetdb(self, help,domain, output, ips):
        if help:
            self.helps.help_internetdb()
            return
        
        async def asyncinternetdb():
            async with httpx.AsyncClient(verify=False) as session:
                dbsearch = ShodanxInternetDB(domain=domain, session=session, output=output)
                if domain:
                    data = await dbsearch.do()
                elif ips:
                    if os.path.exists(ips):
                        Ips = await self.utils.async_reader(ips)
                    else:
                        Ips = ips.split(",")
                    data = await dbsearch.search_all(Ips)

        self._run_async(asyncinternetdb())
        
    def trends(self,help,query,facet,output):
        if help:
            self.helps.help_trends()
            return
        
        async def asynctrends():
            async with httpx.AsyncClient(verify=False) as session:
                trendssearch = ShodanxTrendsDB(self.auth_yaml, query, session,facet)
                data = await trendssearch.search_trends()
                if output:
                    await self.saver.save(output,data,True)
                return
        self._run_async(asynctrends())
        
    def map(self,help,place,output):
        if help:
            self.helps.help_map()
            return
        
        async def asyncmaps():
            async with httpx.AsyncClient(verify=False) as session:
                mapsearch = ShodanxMapsOSINT(session=session)
                data = await mapsearch.search(cookies_file=self.auth_cookie, place=place)
                if output:
                    await self.saver.save(output,data,True)
                return
        self._run_async(asyncmaps())
        
    async def show_updates(self):
        await self.git.show_update_log()
        return
    
    def update(self,help,update,show_updates):
        if help:
            self.helps.help_update()
            return
        
        async def updatehandler():
            if show_updates:
                await self.show_updates()
                return
            
            if update:
                current = await self.git.git_version()
                if not current:
                    self.logger.warn("unable to get the latest version of shodanx")
                    return
                
                if current == self.git_version:
                    self.logger.info("ShodanX is already in latest version")
                    return
                
                zipurl = await self.git.fetch_latest_zip_url()
                if not zipurl:
                    self.logger.warn("unable to get the latest source code of ShodanX")
                    return
                
                await self.git.download_and_install(zipurl)
                newpypi = self.git.current_version()
                if newpypi == self.pypi:
                    self.logger.warn("unable to update ShodanX to the latest version, please try manually")
                    return
                
                self.logger.info(f"ShodanX has been updated to version")
                await self.show_updates()
                return
        self._run_async(updatehandler())

settings = dict(help_option_names=['-h', '--help'])

def customizer(ctx, param, value): 
    
    if value and not ctx.resilient_parsing:
        if not ctx.invoked_subcommand:
            Banner(tool_name="ShodanX").render()
            Helper().main_help()
            exit()
        else:
            ctx.invoke(ctx.command, ['--help'])

@click.group(context_settings=settings)
@click.option("-h", "--help", is_flag=True, is_eager=True, expose_value=False, callback=customizer)
def cli():
    pass


@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("--organization", "-org", type=str)
@click.option("--facet", "-fct", default="ip")
@click.option("--output", "-o", type=str)
@click.option("--verbose", "-v", is_flag=True)
def org(**kwargs):
    ShodanX().org(**kwargs)

@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("--domain", "-domain", type=str)
@click.option("--facet", "-fct", default="ip")
@click.option("--output", "-o", type=str)
def domain(**kwargs):
    ShodanX().domain(**kwargs)

@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("--ssl-query", "-sq", type=str)
@click.option("--facet", "-fct", default="ip")
@click.option("--output", "-o", type=str)
def ssl(**kwargs):
    ShodanX().ssl(help=kwargs["help"],query=kwargs["ssl_query"], facet=kwargs["facet"], output=kwargs["output"])

@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("--custom-query", "-cq", type=str)
@click.option("--facet", "-fct", default="ip")
@click.option("--output", "-o", type=str)
def custom(**kwargs):
    ShodanX().custom(help=kwargs["help"],query=kwargs["custom_query"], facet=kwargs["facet"], output=kwargs["output"])

@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("--domain", "-d", type=str)
@click.option("--output", "-o", type=str)
@click.option("--verbose", "-v", is_flag=True)
def subdomain(**kwargs):
    ShodanX().subdomain(**kwargs)

@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("-cpe", "--cpe", type=str)
@click.option("-product", "--product", type=str)
@click.option("-cve", "--cve", type=str)
@click.option("-exploited", "--exploited", is_flag=True)
@click.option("-sd","--start-date",  type=str,default=None)
@click.option("-ed","--end-date", type=str, default=None)
@click.option("-l", "--limits", type=int, default=1000)
@click.option("-o", "--output", type=str,default=None)
def cvedb(**kwargs):
    ShodanX().cvedb(**kwargs)


@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("-id", "--id", type=str)
def entitydb(**kwargs):
    ShodanX().entitydb(**kwargs)

@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("-country", "--country", type=str)
def exposuredb(**kwargs):
    ShodanX().exposuredb(**kwargs)

@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("-top", "--top", type=int, default=500)
@click.option("-all", "--all", is_flag=True)
def faviconmap(**kwargs):
    ShodanX().faviconmap(**kwargs)

@cli.command()
@click.option("-h", "--help",is_flag=True)
@click.option("-d", "--domain", type=str)
@click.option("-o", "--output", type=str)
@click.option("-ips", "--ips", type=str)
def internetdb(**kwargs):
    ShodanX().internetdb(**kwargs)

@cli.command()
@click.option("-h", "--help",is_flag=True)
def auth(**kwargs):
    ShodanX().auth(**kwargs)
    
@cli.command()
@click.option("-h", "--help",is_flag=True)
def login(**kwargs):
    ShodanX().login(**kwargs)
    
@cli.command()
@click.option("-h", "--help", is_flag=True)
@click.option("-query", "--query", type=str, default=None)
@click.option("-fct", "--facet", type=str, default="ip")
@click.option("-o", "--output", type=str, default=None)
def trends(**kwargs):
    ShodanX().trends(**kwargs)
    
@cli.command()
@click.option("-h", "--help", is_flag=True)
@click.option("-place", "--place", type=str,default=None)
@click.option("-o", "--output", type=str,default=None)
def map(**kwargs):
    ShodanX().map(**kwargs)

@cli.command()
@click.option("-h", "--help", is_flag=True)
@click.option("-up", "--update", is_flag=True)
@click.option("-sup", "--show-updates", is_flag=True)
def update(**kwargs):
    ShodanX().update(**kwargs)
    
if __name__ == "__main__":
    cli()
