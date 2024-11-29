from abc import ABC, abstractmethod
from asyncio import Queue
from datetime import datetime
from parsel import Selector
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

    async def _get_text_from_selector(self, selector: str) -> str:
        await self.page.wait_for_selector(selector)
        soup = await self.page.inner_text(selector)
        log.warning(soup)
        return soup

    async def _get_number_from_selector(self, selector: str) -> int:
        return parse_followers(await self._get_text_from_selector(selector))

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
                name=await self._get_text_from_selector('[data-testid="UserName"] > div > div > div > div > div > div > span > span'),
                description=await self._get_text_from_selector('[data-testid="UserDescription"] > span'),
                following=await self._get_number_from_selector('a[href$="following"] > span > span'),
                followers=await self._get_number_from_selector('a[href$="followers"] > span > span'),
            ),
        )
        await self.conn.commit()


class TweetWorker(Worker):
    def __init__(self, users_queue: Queue, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.users_queue = users_queue

    async def handle(self, url: str):
        tweet_id = tweet_id_from_url(url)
        if await self.querier.does_tweet_exist(id=tweet_id):
            log.warning(f"{url} has been visited already")
            return

        user_handle = user_handle_from_url(url)
        await self.users_queue.put(f"https://x.com/{user_handle}")
        await self.page.goto(url)
        await self.page.wait_for_selector("//article[@data-testid='tweet']")
        await self.page.mouse.wheel(0, 15000)
        tweet = (await self.page.query_selector_all("//article[@data-testid='tweet']"))[0]
        html = await tweet.inner_html()
        selector = Selector(html)

        await self.querier.create_tweet(
            CreateTweetParams(
                id=tweet_id,
                tweeted_at=datetime.strptime(selector.xpath(".//time/@datetime").get(), "%Y-%m-%dT%H:%M:%S.%fZ"),
                text="".join(selector.xpath(".//*[@data-testid='tweetText']//text()").getall()),
                replies=parse_followers(selector.xpath('.//a[contains(@href,"comments")]//text()').get()),
                retweets=parse_followers(selector.xpath('.//a[contains(@href,"retweets")]//text()').get()),
                likes=parse_followers(selector.xpath('.//a[contains(@href,"likes")]//text()').get()),
                views=parse_followers(selector.xpath('.//span[contains(text(),"Views")]/../preceding-sibling::div//text()').get()),
                user_handle=user_handle,
                parent_id=None,
            ),
        )
        await self.conn.commit()

    async def _get_datetime_from_selector(self, selector: str) -> datetime:
        await self.page.wait_for_selector(selector)
        return datetime.strptime(await self.page.get_attribute(selector, "datetime"), "%Y-%m-%dT%H:%M:%S.%fZ")


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
