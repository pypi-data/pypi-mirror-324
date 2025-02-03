import time
import aiohttp
import asyncio
from .module01 import Cores
from ..scripts import Scripted
from ..functions import Config
from ..functions import SMessage
from ..functions import Cancelled
from ..functions import AioxdlTimeout
#====================================================================================

class Aioxdl(Cores):

    def __init__(self, **kwargs):
        self.chunks = 1024
        self.kwords = Config.DATA01
        self.kwords.update(kwargs)

#====================================================================================

    async def display(self, tsizes, dsizes, progress, progresss):
        if progress and tsizes != 0:
            await progress(tsizes, dsizes, *progresss)

#====================================================================================

    async def download(self, url, location=None, progress=None, progress_args=()):
        try:
            return await self.start(url, location, progress, progress_args)
        except asyncio.TimeoutError:
            raise AioxdlTimeout("TIMEOUT")

#====================================================================================

    async def clinton(self, url, location=None, progress=None, progress_args=()):
        try:
            location = await self.start(url, location, progress, progress_args)
            return SMessage(result=location, status=200)
        except aiohttp.ClientConnectorError as errors:
            return SMessage(errors=errors, status=400)
        except asyncio.TimeoutError:
            errors = Scripted.DATA01
            return SMessage(errors=errors, status=400)
        except Cancelled as errors:
            return SMessage(errors=errors, status=300)
        except Exception as errors:
            return SMessage(errors=errors, status=400)

#====================================================================================
