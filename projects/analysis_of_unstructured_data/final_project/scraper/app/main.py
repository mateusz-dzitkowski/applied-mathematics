from multiprocessing import Queue

from app import config
from app.workers import TweetWorker, UserWorker
from playwright.sync_api import BrowserContext, sync_playwright
from sqlalchemy import create_engine


def main():
    context = prepare_browser_context()
    users_queue = Queue(maxsize=100)
    tweet_queue = Queue(maxsize=100)

    with create_engine(config.DATABASE_URL).connect() as conn:
        user_worker = UserWorker(
            page=context.new_page(),
            queue=users_queue,
            conn=conn,
        )
        tweet_worker = TweetWorker(
            page=context.new_page(),
            queue=tweet_queue,
            conn=conn,
        )

        tweet_worker.queue.put("https://x.com/Catsillyness/status/1861406277143769383")
        user_worker.queue.put("https://x.com/Catsillyness")

        user_worker.start()
        tweet_worker.start()

        user_worker.join()
        tweet_worker.join()


def prepare_browser_context() -> BrowserContext:
    playwright = sync_playwright().start()
    device = playwright.devices["Desktop Chrome"]
    browser = playwright.chromium.launch()
    context = browser.new_context(**device)
    return context


if __name__ == "__main__":
    main()
