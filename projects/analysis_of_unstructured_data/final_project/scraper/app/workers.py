from abc import ABC, abstractmethod
from asyncio import Queue
from datetime import UTC, datetime

from app.db.queries import AsyncQuerier, CreateTweetParams, CreateUserParams
from app.log import log
from bs4 import BeautifulSoup
from playwright.async_api import Page
from sqlalchemy.ext.asyncio import AsyncConnection


class Worker(ABC):
    def __init__(self, page: Page, queue: Queue, conn: AsyncConnection):
        self.page = page
        self.queue = queue
        self.conn = conn
        self.querier = AsyncQuerier(conn)

    async def run(self):
        while True:
            url: str = await self.queue.get()
            log.debug(f"working on {url}")
            await self.handle(url)
            self.queue.task_done()

    @abstractmethod
    async def handle(self, url: str): ...


class UserWorker(Worker):
    async def handle(self, url: str):
        user_handle = user_handle_from_url(url)
        if await self.querier.does_user_exist(handle=user_handle):
            log.warning(f"{url} has been visited already")
            return

        await self.page.goto(url)
        await self.querier.create_user(
            CreateUserParams(
                handle=user_handle,
                name=await self._get_username(),
                description=await self._get_description(),
                following=await self._get_following(),
                followers=await self._get_followers(),
            ),
        )
        await self.conn.commit()

    async def _get_username(self) -> str:
        selector = '[data-testid="UserName"] > div > div > div > div > div > div > span > span'
        await self.page.wait_for_selector(selector)
        soup = get_soup(await self.page.inner_html(selector))
        return soup.text

    async def _get_description(self) -> str:
        selector = '[data-testid="UserDescription"] > span'
        await self.page.wait_for_selector(selector)
        soup = get_soup(await self.page.inner_html(selector))
        return soup.text

    async def _get_following(self) -> int:
        selector = 'a[href$="following"] > span > span'
        await self.page.wait_for_selector(selector)
        soup = get_soup(await self.page.inner_html(selector))
        return parse_followers(soup.text)

    async def _get_followers(self) -> int:
        selector = 'a[href$="followers"] > span > span'
        await self.page.wait_for_selector(selector)
        soup = get_soup(await self.page.inner_html(selector))
        return parse_followers(soup.text)


class TweetWorker(Worker):
    async def handle(self, url: str):
        tweet_id = tweet_id_from_url(url)
        if await self.querier.does_tweet_exist(id=tweet_id):
            log.warning(f"{url} has been visited already")
            return

        # TODO: visit and parse the site
        await self.querier.create_tweet(
            CreateTweetParams(
                id=tweet_id,
                tweeted_at=datetime.now(UTC),
                text="MATI-TEST",
                replies=123,
                retweets=123,
                likes=1321,
                views=321,
                user_handle=user_handle_from_url(url),
                parent_id=None,
            ),
        )
        await self.conn.commit()


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


def get_soup(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, features="html.parser")


def parse_followers(raw: str) -> int:
    mult_map = {
        "K": 1_000,
        "M": 1_000_000,
        "B": 1_000_000_000,
    }

    suffix = raw[-1].upper()
    if suffix not in mult_map:
        return int(raw.replace(",", ""))

    return int(float(raw[:-1]) * mult_map.get(suffix, 1))
