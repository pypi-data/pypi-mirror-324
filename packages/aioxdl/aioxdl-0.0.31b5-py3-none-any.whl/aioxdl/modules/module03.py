import os
from urllib.parse import unquote
from urllib.parse import urlparse
#==========================================================================

class File:

    async def get02(self, response):
        return int(response.get("Content-Length", 1))

#==========================================================================

    async def get01(filename, location):
        if location:
            return os.path.join(location, filename)
        else:
            return filename

#==========================================================================

    async def get05(url, headers):
        moonues = headers.get("Content-Disposition", None)
        if moonues and "filename=" in moonues:
            filename01 = moonues.index("filename=") + len("filename=")
            filename02 = moonues[filename01:]
            filename03 = unquote(filename02.strip('"'))
            filename04 = filename03.replace("/", "-")
            return filename04
        else:
            filename01 = urlparse(url).path.split("/")
            filename02 = filename01[-1]
            filename03 = unquote(filename02)
            filename04 = filename03.replace("/", "-")
            return filename04

#==========================================================================
