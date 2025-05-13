import aiofiles
import json
from shodanx.modules.logger.logger import Logger
from typing import Any


class ShodanxSave():
    def __init__(self, logger: Logger):
        self.logger = logger
    
    async def save(self,filename: str, content: Any,jsonize:bool = False) -> None:
        try:
            async with aiofiles.open(filename, "a") as streamw:
                if jsonize:
                    await streamw.write(json.dumps(content, indent=4)+ "\n")
                else:
                    await streamw.write(content + '\n')
        except Exception as e:
            self.logger.warn(f"error occured in shodanx save module due to: {e}, {type(e)}, {content}")