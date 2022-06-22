import asyncio

## Define a coroutine that takes in a future
async def myCoroutine():
    print("My Coroutine")

## Spin up a quick and simple event loop
## and run until completed
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(myCoroutine())
finally:
    loop.close()