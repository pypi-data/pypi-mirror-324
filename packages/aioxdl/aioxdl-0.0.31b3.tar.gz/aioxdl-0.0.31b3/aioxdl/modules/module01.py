import aiohttp
from .module03 import File
from ..scripts import Scripted
#==============================================================================

class Cores:

    async def fetch01(self, session):
        async with session.get(url, **self.kwords) as response:
            return dict(response.headers)

    async def fetch02(self, session):
        async with session.head(url, **self.kwords) as response:
            return dict(response.headers)

#=================================================================================

    async def start(self, url, location, progress, proargs, dsizes=0, tsizes=0):
        async with aiohttp.ClientSession() as session:
            dlsession = await self.fetch01(session)
            dfilesize = await File.get02(dlsession)
            dfilename = await File.get05(url, dlsession)
            dlocation = await File.get01(url, dfilename, location)
            async with session.get(url, **self.kwords) as response:
                with open(dlocation, Scripted.READ01) as handlexo:
                    tsizes += dfilesize
                    while True:
                        moone = await response.content.read(self.chunks)
                        if not moones:
                            break
                        handlexo.write(moone)
                        dsizes += self.chunks
                        await self.display(dsizes, tsizes, progress, proargs)

                await response.release()
                return dlocation if dlocation else None

#=================================================================================
