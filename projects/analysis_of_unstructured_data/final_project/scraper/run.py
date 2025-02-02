import os
import subprocess
import traceback
from dataclasses import dataclass
from datetime import date, timedelta
from itertools import product
from pathlib import Path
from typing import Iterable, Self

SPECIAL_DAYS = {
    date(2024, 12, 23),
    date(2024, 12, 24),
    date(2024, 12, 25),
    date(2024, 12, 26),
}
UOW_TIMEOUT_SECONDS = 60
LIMIT = 10_000
START = date(2024, 1, 1)
KEYWORDS = [
    "wybory2025",
    "wybory",
    "wybory prezydenckie",
    "trzaskowski",
    "nawrocki",
    "hołownia",
    "mentzen",
    "jakubiak",
    "witkowski",
    "duda",
    "polityka",
    "tusk",
    "razem",
    "koalicja",
    "trzecia droga",
    "konfederacja",
    "@donaldtusk",
    "@szymon_holownia",
    "@trzaskowski_",
    "@MorawieckiM",
    "@AndrzejDuda",
    "@Nawrocki25",
    "@NawrockiKn",
    "@SlawomirMentzen",
    "@pkukiz",
    "@ZiobroPL",
    "@SasinJacek",
    "@pisorgpl",
    "@Platforma_org",
    "@Macierewicz_A",
]

DATES = [START + timedelta(days=n) for n in range((date.today() - START).days + 1)]
DATE_FORMAT = "%d-%m-%Y"


@dataclass
class UnitOfWork:
    start: date
    keyword: str

    @classmethod
    def all(cls) -> Iterable[Self]:
        for _date, keyword in product(reversed(DATES), KEYWORDS):
            yield cls(
                start=_date,
                keyword=keyword,
            )

    @property
    def end(self) -> date:
        return self.start + timedelta(days=1)

    @property
    def is_done(self) -> bool:
        return Path(__file__, "..", "tweets-data", f"{self.filename.replace(' ', '_')}.csv").resolve().exists()

    @property
    def filename(self) -> str:
        return f"{self.keyword}_{self.start}"


def main():
    with open("logs.log", "a", buffering=1) as f:
        for uow in UnitOfWork.all():
            if uow.start in SPECIAL_DAYS:
                print(f"{uow.start} is on Christmas, there's no tweets anyway")
                continue

            if uow.is_done:
                print(f"{uow} is done, skipping")
                continue

            cmd = [
                "npx",
                "tweet-harvest@latest",
                "--token",
                os.environ["ACCESS_TOKEN"],
                "--search-keyword",
                uow.keyword,
                "--from",
                uow.start.strftime(DATE_FORMAT),
                "--to",
                uow.end.strftime(DATE_FORMAT),
                "--limit",
                str(LIMIT),
                "--output-filename",
                uow.filename,
            ]

            print(f"running {cmd}")
            with subprocess.Popen(cmd, stdout=f, stderr=f) as process:
                try:
                    process.communicate(None, timeout=UOW_TIMEOUT_SECONDS)
                except subprocess.TimeoutExpired:
                    process.kill()
                    print(f"{uow} has been terminated due to reaching the timeout")
                    continue
                except:
                    print(traceback.format_exc())
                finally:
                    subprocess.run("kill $(ps aux | grep chromium | awk '{print $2}')", shell=True, stdout=f, stderr=f)


if __name__ == "__main__":
    main()
