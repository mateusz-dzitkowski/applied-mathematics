from itertools import combinations
from typing import Iterator

import httpx
import networkx as nx
import numpy as np
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
        edge_colors = [plt.cm.Blues(np.linalg.norm(self[u][v][COPAPERS]) / 10) for u, v in self.edges]

        layout = nx.spring_layout(self, k=2)
        nx.draw_networkx_nodes(self, layout, node_size=node_sizes, edgecolors="black")
        nx.draw_networkx_labels(self, layout, font_weight="bold")
        nx.draw_networkx_edges(
            self,
            pos=layout,
            edge_color=edge_colors,
            width=edge_widths,
        )
        plt.show()


def get_site() -> BeautifulSoup:
    response = httpx.get("https://alfa.im.pwr.edu.pl/~hugo/HSC/Publications.html", verify=False)
    return BeautifulSoup(response.content, features="html.parser")


def get_groups_of_coauthors(soup: BeautifulSoup) -> Iterator[list[str]]:
    for section in soup.find_all("ol", attrs={"type": "1", "start": "1"})[2:]:
        for paper in section.find_all("font", recursive=False):
            members = [member.text for member in paper.find_all("b")]
            yield [unidecode(member.replace(". ", ".").replace(".", ". ")).strip() for member in members]


def main():
    soup = get_site()
    graph = CoauthorGraph()

    for group in get_groups_of_coauthors(soup):
        graph.add_coauthor_group(group)

    graph.draw()


if __name__ == "__main__":
    main()
