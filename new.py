import asyncio

async def user_a():
    print("A: Started")
    await asyncio.sleep(3)
    print("A: Finished")

async def user_b():
    print("B: Started")
    await asyncio.sleep(1)
    print("B: Finished")

async def main():
    await asyncio.gather(user_a(), user_b())

asyncio.run(main())