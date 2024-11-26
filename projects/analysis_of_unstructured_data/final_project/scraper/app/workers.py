import logging
from abc import ABC, abstractmethod
from datetime import UTC, datetime
from multiprocessing import Queue
from threading import Thread

from app.db.queries import CreateTweetParams, CreateUserParams, Querier
from playwright.sync_api import Page
from sqlalchemy import Connection

log = logging.getLogger(__file__)
log.setLevel(logging.INFO)


class Worker(Thread, ABC):
    def __init__(self, page: Page, queue: Queue, conn: Connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.queue = queue
        self.conn = conn
        self.querier = Querier(conn)

    def run(self):
        while True:
            url: str = self.queue.get()
            log.info(f"processing {url}")
            self.process(url)

    @abstractmethod
    def process(self, url: str): ...


class UserWorker(Worker):
    def process(self, url: str):
        user_handle = user_handle_from_url(url)
        db_user = self.querier.get_user(handle=user_handle)
        if db_user:
            log.warning(f"{url} has been visited already")
            return

        # TODO: visit and parse the site
        self.querier.create_user(
            CreateUserParams(
                handle=user_handle,
                name="TODO",
                description="TODO",
                following=123,
                followers=123,
            ),
        )
        self.conn.commit()


class TweetWorker(Worker):
    def process(self, url: str):
        tweet_id = tweet_id_from_url(url)
        db_tweet = self.querier.get_tweet(id=tweet_id)
        if db_tweet:
            log.warning(f"{url} has been visited already")
            return

        user_handle = user_handle_from_url(url)
        user = self.querier.get_user(handle=user_handle)
        if not user:
            log.warning(f"{user_handle} was not yet processed for tweet={url} to be processed")
            self.queue.put(url)
            return

        # TODO: visit and parse the site
        self.querier.create_tweet(
            CreateTweetParams(
                id=tweet_id,
                tweeted_at=datetime.now(UTC),
                text="MATI-TEST",
                replies=123,
                retweets=123,
                likes=1321,
                views=321,
                user_handle=user.handle,
                parent_id=None,
            ),
        )
        self.conn.commit()


def user_handle_from_url(url: str) -> str | None:
    try:
        return url.split("x.com/")[1].split("/")[0]
    except IndexError:
        log.error(f"wrong url format: {url}")
        return None


def tweet_id_from_url(url: str) -> int | None:
    try:
        return int(url.split("/")[-1])
    except (IndexError, ValueError):
        log.error(f"wrong url format: {url}")
        return None
