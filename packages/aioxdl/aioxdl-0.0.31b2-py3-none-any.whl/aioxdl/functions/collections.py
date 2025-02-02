import aiohttp
#========================================================================================

class SMessage:

    def __init__(self, **kwargs):
        self.errors = kwargs.get("errors", None)
        self.result = kwargs.get("result", None)
        self.status = kwargs.get("status", None)
        self.scodes = kwargs.get("scodes", 8000)

#========================================================================================

class Config:

    DATA01 = {"raise_for_status": True}
    DATA02 = {"raise_for_status": True, "timeout": aiohttp.ClientTimeout(sock_read=60)}

#========================================================================================
