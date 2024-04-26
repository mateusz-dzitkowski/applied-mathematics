import traceback
from queue import Queue
import re
from threading import Thread
from csv import writer

import wikipedia as wp


Storage = set[tuple[str, str]]


NUM_WORKERS = 20
NUM_STEPS_PER_WORKER = 1000
ENTRYPOINT = "Adam Małysz"


class Scraper:
    queue: Queue
    storage: Storage
    done: set[str]

    def __init__(self, queue: Queue, storage: Storage, done: set[str]):
        self.storage = storage
        self.queue = queue
        self.done = done

    def run(self, max_iters: int):
        counter = 0
        while counter < max_iters:
            q_page = self.queue.get()
            if q_page in self.done:
                continue

            print(f"Working on `{q_page}`")

            try:
                w_page = wp.page(q_page)
                for link in w_page.links:
                    if not should_add(link):
                        continue
                    self.storage.add((w_page.title, link))
                    self.queue.put(link)
                done.add(q_page)
            except:
                print(f"ERROR when working on {q_page}")
                print(traceback.format_exc())
                self.queue.put(q_page)
                continue

            counter += 1


def should_add(page: str) -> bool:
    # no numbers they usually mess things up
    return not bool(re.search(r"(\d|ujednoznacznienie|Kontrola Autorytatywna)", page))


def run_worker(queue: Queue, storage: Storage, done: set[str]):
    scraper = Scraper(queue, storage, done)
    scraper.run(NUM_STEPS_PER_WORKER)


if __name__ == "__main__":
    storage = set()
    done = set()
    queue = Queue()

    wp.set_lang("pl")
    for entrypoint in wp.page(ENTRYPOINT).links:
        if should_add(entrypoint):
            queue.put(entrypoint)

    try:
        tasks = [Thread(target=run_worker, args=(queue, storage, done)) for _ in range(NUM_WORKERS)]
        [task.start() for task in tasks]
        [task.join() for task in tasks]
    finally:
        with open("result.csv", "w") as f:
            w = writer(f, delimiter="\t")
            w.writerow(("source", "target"))
            w.writerows(storage)

    """
    copy (
        with edges as (select source, target from read_csv_auto('result.csv', header=true)) 
        select source, target from edges 
        where target in ( select source from edges ) 
        or target in ( select target from edges group by 1 having count(*) > 1 )
    )
    to 'result_processed.csv';
    
    copy (
        with edges as (select source, target from read_csv_auto('result.csv', header=true)) 
        select source, target from edges 
        where target in ( select source from edges )
    )
    to 'result_processed_only_in.csv';
    """
