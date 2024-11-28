import asyncio
from asyncio import LifoQueue

from app import config
from app.workers import TweetWorker, UserWorker
from playwright.async_api import BrowserContext, async_playwright
from sqlalchemy.ext.asyncio import create_async_engine


async def main():
    context = await get_browser_context()
    users_queue = LifoQueue(maxsize=100)
    tweet_queue = LifoQueue(maxsize=100)

    async with create_async_engine(config.DATABASE_URL).connect() as conn:
        user_worker = UserWorker(
            page=await context.new_page(),
            queue=users_queue,
            conn=conn,
        )
        tweet_worker = TweetWorker(
            page=await context.new_page(),
            queue=tweet_queue,
            conn=conn,
        )

        for url in [
            "https://x.com/RadekPiasecki1",
            "https://x.com/SlawomirMentzen",
            "https://x.com/kirawontmiss",
            "https://x.com/reedshannon",
            "https://x.com/bennyjohnson",
            "https://x.com/IAPonomarenko",
            "https://x.com/willnights1",
            "https://x.com/TheFigen_",
            "https://x.com/ZiobroPL",
            "https://x.com/Inevitablewest",
            "https://x.com/szymon_holownia",
            "https://x.com/SpotifyUK",
            "https://x.com/GarbageHuman24",
        ]:
            await user_worker.queue.put(url)

        tasks = [
            asyncio.create_task(tweet_worker.run()),
            asyncio.create_task(user_worker.run()),
        ]

        await users_queue.join()
        await tweet_queue.join()

        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)


async def get_browser_context() -> BrowserContext:
    playwright = await async_playwright().start()
    device = playwright.devices["Desktop Chrome"]
    browser = await playwright.chromium.launch()
    context = await browser.new_context(**device)
    return context


if __name__ == "__main__":
    asyncio.run(main())
