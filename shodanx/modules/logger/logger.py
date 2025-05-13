from colorama import Fore, Style, init
import sys
import random
from datetime import datetime
from enum import Enum, auto
import random

init()

class LogLevel(Enum):
    DEBUG = auto()
    VERBOSE = auto()
    INFO = auto()
    WARN = auto()
    ERROR = auto()
    CRITICAL = auto()
    NONE = auto()  

class Logger:
    def __init__(self, name: str = None, colored: bool = True, level: LogLevel = LogLevel.INFO):
        self.colored = colored
        self.name = name
        self.level = level
        self.red = Fore.RED
        self.green = Fore.GREEN
        self.yellow = Fore.YELLOW
        self.blue = Fore.BLUE
        self.magenta = Fore.MAGENTA
        self.cyan = Fore.CYAN
        self.white = Fore.WHITE
        self.bold = Style.BRIGHT
        self.reset = Style.RESET_ALL
        self.color_list = [self.red, self.green, self.yellow, self.blue, self.magenta, self.cyan, self.white]
        self.random_color = random.choice(self.color_list)

        
        self.colors = {
            LogLevel.INFO: Fore.BLUE,
            LogLevel.WARN: Fore.YELLOW,
            LogLevel.ERROR: Fore.RED,
            LogLevel.VERBOSE: Fore.GREEN,
            LogLevel.DEBUG: Fore.CYAN,
            LogLevel.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
            'time': Fore.BLUE
        }
        
        self.level_names = {
            LogLevel.DEBUG: "DEBUG",
            LogLevel.VERBOSE: "VERBOSE",
            LogLevel.INFO: "INFO",
            LogLevel.WARN: "WARN",
            LogLevel.ERROR: "ERROR",
            LogLevel.CRITICAL: "CRITICAL"
        }
    
    def set_level(self, level: LogLevel):
        self.level = level
    
    def should_log(self, level: LogLevel) -> bool:
        return level.value >= self.level.value and self.level != LogLevel.NONE
    
    def _get_timestamp(self):
        return datetime.now().strftime('%H:%M:%S')
    
    def _format_level(self, level: LogLevel):
        if not self.colored:
            return self.level_names.get(level, "LOG")
        color = self.colors.get(level, Fore.WHITE)
        return f"{Style.BRIGHT}{color}{self.level_names.get(level, 'LOG')}{Style.RESET_ALL}"
    
    def _format_name(self):
        if not self.name:
            return ""
        if not self.colored:
            return f"[{self.name}]"
        return f"[{Style.BRIGHT}{Fore.MAGENTA}{self.name}{Style.RESET_ALL}]"
    
    def _format_timestamp(self):
        if not self.colored:
            return f"[{self._get_timestamp()}]"
        return f"[{Style.BRIGHT}{self.colors['time']}{self._get_timestamp()}{Style.RESET_ALL}]"
    
    def _log(self, level: LogLevel, message: str):
        if not self.should_log(level):
            return
            
        timestamp = self._format_timestamp()
        name = self._format_name()
        level_str = self._format_level(level)
        
        if self.colored:
            message = f"{Style.BRIGHT}{Fore.WHITE}{message}{Style.RESET_ALL}"
            
        log_line = f"{timestamp} {name} [{level_str}]: {message}"
        print(log_line, file=sys.stderr)
    
    def debug(self, message: str):
        self._log(LogLevel.DEBUG, message)
        
    def verbose(self, message: str):
        self._log(LogLevel.VERBOSE, message)
        
    def info(self, message: str):
        self._log(LogLevel.INFO, message)
        
    def warn(self, message: str):
        self._log(LogLevel.WARN, message)
        
    def error(self, message: str):
        self._log(LogLevel.ERROR, message)
        
    def critical(self, message: str):
        self._log(LogLevel.CRITICAL, message)
        
    def custom(self, level_name: str, message: str, color: str = Fore.WHITE):
        if not self.colored:
            level_str = level_name.upper()
        else:
            level_str = f"{Style.BRIGHT}{color}{level_name.upper()}{Style.RESET_ALL}"
            
        timestamp = self._format_timestamp()
        name = self._format_name()
        
        if self.colored:
            message = f"{Style.BRIGHT}{Fore.WHITE}{message}{Style.RESET_ALL}"
            
        log_line = f"{timestamp}{name}[{level_str}]: {message}"
        print(log_line, file=sys.stderr)
    
    def banner(self, banner: str):
        print(banner, file=sys.stderr)
        
    def stdin(self, message: str):
        print(message)