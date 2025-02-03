<p align="center">
    📦 <a href="https://pypi.org/project/aioxdl" style="text-decoration:none;">AIO DOWNLOADER</a>
</p>

<p align="center">
   <a href="https://telegram.me/Space_x_bots"><img src="https://img.shields.io/badge/Sᴘᴀᴄᴇ 𝕩 ʙᴏᴛꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.me/clinton_abraham"><img src="https://img.shields.io/badge/Cʟɪɴᴛᴏɴ Aʙʀᴀʜᴀᴍ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
   <a href="https://telegram.me/sources_codes"><img src="https://img.shields.io/badge/Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇꜱ-30302f?style=flat&logo=telegram" alt="telegram badge"/></a>
</p>

## USAGE
<details>
    <summary>Installation</summary>

```bash
pip install aioxdl
```

</details>

<details>
    <summary>Quick start</summary>

```python
import asyncio
from aioxdl.modules import Aioxdl
from aioxdl.modules import Filename
from aioxdl.functions import AioxdlTimeout

# tsize = total size
# dsize = downloaded size

async def progress(tsize, dsize):
    percentage = round((dsize / tsize) * 100, 2)
    print(f"COMPLETED : {percentage}%")

async def main():
    try:
        core = Aioxdl(timeout=2000)
        link = "https://example.in/file.txt"
        name = await Filename.filename(link)
        file = await core.download(link, name, progress=progress)
        print(file)
    except AioxdlTimeout as errors:
        print(errors)
    except Exception as errors:
        print(errors)

asyncio.run(main())
```

</details>

<details>
    <summary>Get filename</summary>

```python
import asyncio
from aioxdl.modules import Filename

async def main():
    link = "https://example.link/file.txt"
    name = await Filename.get(link)
    print(name)

asyncio.run(main())
```

</details>

<details>
    <summary>Stop download</summary>

```python
import asyncio
from aioxdl.modules import Aioxdl
from aioxdl.modules import Filename
from aioxdl.functions import Cancelled
from aioxdl.functions import AioxdlTimeout

TASK_IDS = []

# tsize = total size
# dsize = downloaded size

async def progress(tsize, dsize, tuid):
    if tuid in TASK_IDS:
        percentage = round((dsize / tsize) * 100, 2)
        print(f"COMPLETED : {percentage}%")
    else:
        raise Cancelled("Cancelled ❌")

async def main():
    try:
        tuid = 1234567890
        TASK_IDS.append(tuid)
        core = Aioxdl(timeout=2000)
        link = "https://example.in/file.txt"
        name = await Filename.filename(link)
        file = await core.download(link, name, progress=progress, progress_args=(tuid))
        print(file)
    except AioxdlTimeout as errors:
        print(errors)
    except Cancelled as cancelled:
        print(cancelled)
    except Exception as errors:
        print(errors)

asyncio.run(main())
```
</details>
