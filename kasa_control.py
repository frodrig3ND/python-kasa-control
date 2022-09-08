import asyncio
from kasa import Discover

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

dev = asyncio.run(Discover.discover_single(host="192.168.1.205"))
print(f"{dev}")

devices = asyncio.run(Discover.discover(target="192.168.1.255"))
for addr, dev in devices.items():
    asyncio.run(dev.update())
    print(f"{addr} >> {dev}")

