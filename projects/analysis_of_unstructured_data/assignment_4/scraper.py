from itertools import combinations
from typing import Iterator

import httpx
import networkx as nx
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from text_unidecode import unidecode

PAPERS = "papers"
COPAPERS = "copapers"


class CoauthorGraph(nx.Graph):
    def add_coauthor_group(self, coauthors: list[str]):
        for coauthor in coauthors:
            if coauthor not in self:
                self.add_node(coauthor, **{PAPERS: 1})
            else:
                self.nodes[coauthor][PAPERS] += 1

        for foo, bar in combinations(coauthors, 2):
            if bar not in self[foo]:
                self.add_edge(foo, bar, **{COPAPERS: 1})
            else:
                self[foo][bar][COPAPERS] += 1

    def draw(self):
        plt.figure(figsize=(20, 20))
        node_sizes = [self.nodes[node][PAPERS] * 20 for node in self.nodes]
        edge_widths = [self[u][v][COPAPERS] for u, v in self.edges]
        layout = nx.spring_layout(self, k=0.7, iterations=50)
        nx.draw(self, layout, with_labels=True, node_size=node_sizes, width=edge_widths, edge_color="gray")
        plt.show()


def get_site() -> BeautifulSoup:
    response = httpx.get("https://alfa.im.pwr.edu.pl/~hugo/HSC/Publications.html", verify=False)
    return BeautifulSoup(response.content, features="html.parser")


def get_groups_of_coauthors(soup: BeautifulSoup) -> Iterator[list[str]]:
    for section in soup.find_all("ol", attrs={"type": "1", "start": "1"}):
        for paper in section.find_all("font", recursive=False):
            just_names: str = paper.text.split('"')[0].split("(")[0]
            just_names_fixed = just_names.replace(". ", ".").replace(".", ". ")
            yield [unidecode(item.strip()) for item in just_names_fixed.split(",") if item.strip() != ""]


def main():
    soup = get_site()
    graph = CoauthorGraph()

    for group in get_groups_of_coauthors(soup):
        graph.add_coauthor_group(group)

    graph.draw()


if __name__ == "__main__":
    main()
