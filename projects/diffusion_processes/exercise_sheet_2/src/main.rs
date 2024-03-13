mod graph;

use graph::{Edge, Graph, Node};

fn main() {
    let mut g = Graph::default();
    g.add_node(Node::new("a"));
    g.add_node(Node::new("b"));
    g.add_node(Node::new("c"));
    g.add_node(Node::new("d"));
    g.add_edges(vec![
        Edge::new("a", "b"),
        Edge::new("b", "c"),
        Edge::new("b", "d"),
        Edge::new("c", "a"),
        Edge::new("d", "a"),
    ]);
    println!("{}", g.to_dot());
    g.save_graph("graph.txt");
}
