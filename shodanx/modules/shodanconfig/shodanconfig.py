from pathlib import Path
from appdirs import user_config_dir

class ShodanxConfig:
    def __init__(self, app_name: str = "ShodanX"):
        self.app_name = app_name
        if not self.app_name:
            raise ValueError("App name is required")
        self._ensure_config_dir_exists()
        self._ensure_config_files_exist()
        
    @property
    def config_dir(self) -> Path:
        return Path(user_config_dir(self.app_name))
    
    def config_auth(self) -> Path:
        return self.config_dir / "provider-config.yaml"
    
    def config_cookie(self) -> Path:
        return self.config_dir / "cookies.yaml"
    
    def _ensure_config_dir_exists(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def _ensure_config_files_exist(self) -> None:
        files = {
            self.config_auth(): "shodanx:\n    username:wiener\n    password:peter\n apikey:DIOBSFOUBGFOUBSOFBOFBF\n", #this is not valid key
            self.config_cookie(): "cookies:paste-ur-cookie-here"
        }
        for path, default_content in files.items():
            if not path.exists():
                path.write_text(default_content)