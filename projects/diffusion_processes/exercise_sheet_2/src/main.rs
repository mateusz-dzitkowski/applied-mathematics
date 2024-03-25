#![allow(dead_code)]

mod graph;

use graph::{Edge, Graph, Node};

fn main() {
    let mut g = Graph::default();
    g.add_nodes("a,b,c,d,e,f,g,h,i,j".split(",").map(Node::new));
    g.add_edges(
        "a-b,b-g,i-g,c-a,g-h,i-j,a-d,h-j,e-f,a-e,j-g,d-c,a-f,h-i,c-f"
            .split(",")
            .map(|pair| pair.split("-"))
            .map(|mut item| Edge::new_unweighted(item.next().unwrap(), item.next().unwrap())),
    );
    println!("{}", g.to_dot());
    g.save_graph("graph.txt");

    dbg!(g.get_shortest_path_lengths("d"));
}
