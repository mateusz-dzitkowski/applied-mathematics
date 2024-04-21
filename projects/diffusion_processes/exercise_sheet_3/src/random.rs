use petgraph::graph::UnGraph;
use itertools::iproduct;
use rand::Rng;


pub fn random_graph(n: u32, p: f64) -> UnGraph<usize, ()> {
    UnGraph::<usize, ()>::from_edges(get_random_edges(n, p))
}

fn get_random_edges(n: u32, p: f64) -> Vec<(u32, u32)> {
    iproduct!(0..n, 0..n)
        .filter(|(x, y)| x < y && rand::thread_rng().gen_range(0. .. 1.) < p)
        .collect()
}
