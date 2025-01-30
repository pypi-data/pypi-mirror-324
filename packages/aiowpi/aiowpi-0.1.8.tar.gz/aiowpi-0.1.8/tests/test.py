import asyncio
from aiowpi import WPIClient, WOWS_ASIA

async def main():
    wpi = WPIClient("???")
    print(await wpi.player.serch(WOWS_ASIA, "???"))
    pass


if __name__ == "__main__":
    asyncio.run(main())
