import networkx as nx
from matplotlib import pyplot as plt
from pandas import read_csv, DataFrame


def from_csv(file_name: str) -> nx.DiGraph:
    data = read_csv(file_name)
    return nx.from_pandas_edgelist(data, create_using=nx.DiGraph())


def get_stats(g: nx.DiGraph) -> DataFrame:
    data = DataFrame()
    data["degree"] = dict(nx.degree(g))
    data["clustering"] = nx.clustering(g)
    data["closeness"] = nx.closeness_centrality(g)
    data["betweenness"] = nx.betweenness_centrality(g)
    return data.sort_index()


if __name__ == "__main__":
    g = from_csv("graph.csv")

    print(f"Num of nodes: {nx.number_of_nodes(g)}")
    print(f"Density of the graph: {nx.density(g)}")
    print(get_stats(g))

    nx.draw_networkx(g, pos=nx.drawing.kamada_kawai_layout(g), arrows=False)
    plt.show()
