#!/usr/bin/env python3
from art import text2art
from shodanx.modules.logger.logger import Logger
import random

class Banner:
    def __init__(self, tool_name: str = "RevoltSecurities"):
        self.tool_name = tool_name
        self.fonts = ["big", "ogre", "shadow", "script", "graffiti", "slant"]
        self.logger = Logger(name="BannerPrinter")

    def render(self) -> str:
        selected_font = random.choice(self.fonts)
        banner_art = text2art(self.tool_name, font=selected_font)
        banner = f"""{self.logger.bold}{self.logger.random_color}{banner_art}{self.logger.reset}
                     {self.logger.bold}{self.logger.white}- RevoltSecurities{self.logger.reset}\n"""
        self.logger.banner(banner)