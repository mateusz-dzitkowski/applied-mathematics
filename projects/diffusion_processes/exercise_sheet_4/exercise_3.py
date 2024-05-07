from pprint import pprint
from statistics import mean
from typing import Callable

from matplotlib import animation
from matplotlib import pyplot as plt
import networkx as nx


FPS = 1
BITRATE = 2400


def animate_random_walk(g: nx.Graph, length: int, filename: str):
    fig, ax = plt.subplots()

    path = next(nx.generate_random_paths(g, sample_size=1, path_length=length))
    edge_list = list(zip(path[:-1], path[1:]))

    def animate(n: int):
        ax.clear()
        nx.draw(g, nx.circular_layout(g), with_labels=True, node_color="skyblue", ax=ax)
        nx.draw_networkx_nodes(g, nx.circular_layout(g), nodelist=[path[n]], node_color="red")
        nx.draw_networkx_edges(g, nx.circular_layout(g), edgelist=edge_list[:n], edge_color="orange")

    print("saving the animation...")
    animation.FuncAnimation(
        fig=fig,
        func=animate,  # type: ignore
        frames=length,
    ).save(
        filename=filename,
        writer=animation.PillowWriter(fps=FPS, bitrate=BITRATE),
    )
    plt.close()


def hitting_times(g: nx.Graph, origin: int, sample_size: int = 10_000, transform: Callable[[list[int]], float | int] = mean) -> dict[int, float | int]:
    result: dict[int, list[int]] = dict()

    for path in nx.generate_random_paths(g, sample_size=sample_size, path_length=2 * len(g.nodes)):
        if origin not in path:
            continue

        path = path[path.index(origin):]  # fix the path to be starting at origin
        for node in g.nodes:
            if node not in path:
                continue

            if node not in result:
                result[node] = []

            result[node].append(path.index(node))

    return {key: transform(val) for key, val in result.items()}


def show_graph(g: nx.Graph):
    nx.draw(g, nx.circular_layout(g), with_labels=True)
    plt.show()


def main():
    g = nx.watts_strogatz_graph(10, 4, 0.4)
    pprint(hitting_times(g, 0, transform=min))
    pprint(hitting_times(g, 0, transform=mean))
    show_graph(g)


if __name__ == "__main__":
    main()
