import aiohttp
#==============================================================================

class Cores:

    async def start(self, url, location, progress, progress_args):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, **self.kwords) as response:
                self.tsizes += await self.getsizes(response)
                with open(location, "wb") as handlexo:
                    while True:
                        chunks = await response.content.read(self.chunks)
                        if not chunks:
                            break
                        handlexo.write(chunks)
                        self.dsizes += self.chunks
                        await self.display(progress, progress_args)

                await response.release()
                return location if location else None

#==============================================================================
