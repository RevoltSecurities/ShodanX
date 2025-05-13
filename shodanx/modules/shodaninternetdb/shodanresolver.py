import aiodns
from typing import List, Optional

class ShodanXDNSResolver:
    def __init__(self, nameservers: Optional[List[str]] = None, timeout: int = 30):
        if nameservers:
            self.nameservers = nameservers
        else:
            self.nameservers = None
        self.resolver = aiodns.DNSResolver(nameservers=self.nameservers)
    async def resolve(self, domain: str) -> List[str]:
        try:
            result = await self.resolver.query(domain, 'A')
            return [r.host for r in result]
        except aiodns.error.DNSError:
            return []
        except Exception as e:
            return []