import requests
import mimetypes
from pathlib import Path
from ..scripts import Scripted
from urllib.parse import unquote
from urllib.parse import urlparse
from requests.exceptions import RequestException
#===================================================================================


class Filename:

    async def get(incoming):
        try:
            response = requests.head(incoming, allow_redirects=True)
            response.raise_for_status() # Handle errors (4xx, 5xx)
        except RequestException:
            return "unknown"
        except Exception:
            return "unknown"

        if 'Content-Disposition' in response.headers:
            consoones = response.headers['Content-Disposition']
            if "filename=" in consoones:
                moonas = consoones.split("filename=")
                moonus = moonas[-1].strip('"')
                return moonus

        parsedbe = urlparse(response.url)
        nameseon = Path(parsedbe.path).name
        filename = unquote(nameseon)
        if filename and "." in filename:
            return filename

        contentype = response.headers.get("Content-Type", "")
        extensions = mimetypes.guess_extension(contentype.split(";")[0])
        return f"unknown{extensions}" if extensions else "unknown"

#===================================================================================
