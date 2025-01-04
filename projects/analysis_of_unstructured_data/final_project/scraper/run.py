from dataclasses import dataclass
from datetime import date, timedelta
from itertools import product
import os
from pathlib import Path
import subprocess
import traceback
from typing import Self, Iterable


UOW_TIMEOUT_SECONDS = 120
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
    "starosielec",
    "duda",
    "polityka",
    "tusk",
    "razem",
    "koalicja",
    "trzecia droga",
    "pis",
    "konfederacja",
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
            if uow.is_done:
                print(f"{uow} is done, skipping")
                continue

            cmd = [
                "npx", "tweet-harvest@latest",
                "--token", os.environ["ACCESS_TOKEN"],
                "--search-keyword", uow.keyword,
                "--from", uow.start.strftime(DATE_FORMAT),
                "--to", uow.end.strftime(DATE_FORMAT),
                "--limit", str(LIMIT),
                "--output-filename", uow.filename,
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


if __name__ == "__main__":
    main()
