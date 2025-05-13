import os
import aiofiles
import asyncio
import importlib.metadata as metadata
import httpx
from rich.console import Console
from rich.markdown import Markdown
from shodanx.modules.logger.logger import Logger


class GitUtils:
    def __init__(self, repo: str, package: str, config_path: str):
        self.repo = repo
        self.package = package
        self.config_path = config_path
        self.console = Console()
        self.logger = Logger()

    def current_version(self) -> str:
        try:
            return metadata.version(self.package)
        except metadata.PackageNotFoundError:
            self.logger.warn(f"Package {self.package} not found.")
            return "Unknown"
        
    async def git_version(self) -> str:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(f"https://api.github.com/repos/{self.repo}/releases/latest")
                if response.status_code == 200:
                    return response.json().get("tag_name")
                else:
                    return None
        except Exception as e:
            return None

    async def fetch_latest_zip_url(self) -> str | None:
        url = f"https://api.github.com/repos/{self.repo}/releases/latest"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    return response.json().get("zipball_url")
                else:
                    self.logger.warn("Failed to fetch latest release info from GitHub.")
        except Exception as e:
            self.logger.error(f"Error fetching update URL: {e}")
        return None

    async def download_and_install(self, zip_url: str):
        filepath = os.path.join(self.config_path, f"{self.package}.zip")
        try:
            self.logger.info("Downloading latest version...")
            async with httpx.AsyncClient(timeout=20) as client:
                async with client.stream("GET", zip_url) as response:
                    if response.status_code == 200:
                        async with aiofiles.open(filepath, "wb") as f:
                            async for chunk in response.aiter_bytes():
                                await f.write(chunk)
                    else:
                        self.logger.warn("Failed to download the latest release.")
                        return

            process = await asyncio.create_subprocess_exec(
                "pipx", "install", filepath, "--force",
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL
            )
            await process.communicate()
            if process.returncode == 0:
                self.logger.success(f"{self.package} updated successfully.")
            else:
                self.logger.warn("Update failed. Try manual update.")
        except Exception as e:
            self.logger.error(f"Update failed: {e}")
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

    async def show_update_log(self):
        url = f"https://api.github.com/repos/{self.repo}/releases/latest"
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    log = response.json().get("body", "")
                    self.console.print(Markdown(log))
                else:
                    self.logger.info(f"Could not fetch logs. Visit: https://github.com/{self.repo}")
        except Exception as e:
            self.logger.error(f"Error fetching changelog: {e}")