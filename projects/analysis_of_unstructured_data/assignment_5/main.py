from functools import lru_cache

import httpx
from geopy import Location, Nominatim
from nltk import (
    Tree,
    download,
    ne_chunk,
    pos_tag,
    word_tokenize,
)


def get_book() -> str:
    return (
        httpx.get("https://www.gutenberg.org/cache/epub/103/pg103.txt")
        .text.split("*** START OF THE PROJECT GUTENBERG EBOOK AROUND THE WORLD IN EIGHTY DAYS ***")[1]
        .split("*** END OF THE PROJECT GUTENBERG EBOOK AROUND THE WORLD IN EIGHTY DAYS ***")[0]
    )


def preprocess_text(text: str) -> Tree:
    download("punkt_tab")
    download("averaged_perceptron_tagger_eng")
    download("maxent_ne_chunker_tab")
    download("words")
    return ne_chunk(pos_tag(word_tokenize(text)))


def extract_locations(tree: Tree) -> list[str]:
    return [" ".join(token for token, pos in subtree.leaves()) for subtree in tree if isinstance(subtree, Tree) and subtree.label() == "GPE"]


@lru_cache
def search_geo(nominatim: Nominatim, search_term: str):
    print(f"looking up {search_term}...")
    return nominatim.geocode(search_term, language="en")


def extract_cities(locations: list[str]) -> list[Location]:
    nominatim = Nominatim(user_agent="mati-test")
    cities = []

    for loc in locations:
        city: Location | None = search_geo(nominatim, loc)
        if not city:
            continue
        if city.raw["addresstype"] not in {"city", "suburb"}:
            continue
        if city in cities:
            continue
        cities.append(city)

    return cities


def main():
    book = get_book()
    preprocessed = preprocess_text(book)
    locations = extract_locations(preprocessed)
    cities = extract_cities(locations)
    for city in cities:
        print(city)


if __name__ == "__main__":
    main()
