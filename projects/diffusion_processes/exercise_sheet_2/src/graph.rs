use std::collections::{HashMap, VecDeque};
use std::fmt::{Debug, Display};
use std::hash::Hash;

#[derive(Debug, PartialEq, Clone)]
pub struct Node<T> {
    label: T,
}

impl<T> Node<T> {
    pub fn new(label: T) -> Self {
        Self { label }
    }
}

#[derive(Debug, PartialEq, Clone)]
pub struct Edge<T> {
    from: T,
    to: T,
    weight: f64,
}

impl<T> Edge<T> {
    pub fn new(from: T, to: T, weight: f64) -> Self {
        Self { from, to, weight }
    }

    pub fn new_unweighted(from: T, to: T) -> Self {
        Self {
            from,
            to,
            weight: 1.,
        }
    }
}

#[derive(Debug, Default)]
pub struct Graph<T: Eq + Clone + Hash> {
    nodes: HashMap<T, Node<T>>,
    edges: Vec<Edge<T>>,
}

impl<T: Eq + Clone + Hash + Display + Debug> Graph<T> {
    pub fn add_node(&mut self, node: Node<T>) {
        self.nodes.insert(node.label.clone(), node);
    }

    pub fn add_nodes<U>(&mut self, nodes: U)
    where
        U: IntoIterator<Item = Node<T>>,
    {
        nodes.into_iter().for_each(|node| self.add_node(node))
    }

    pub fn add_edge(&mut self, edge: Edge<T>) {
        self.edges.push(edge);
    }

    pub fn add_edges<U>(&mut self, edges: U)
    where
        U: IntoIterator<Item = Edge<T>>,
    {
        edges.into_iter().for_each(|edge| self.add_edge(edge))
    }

    pub fn contains(&self, key: &T) -> bool {
        self.nodes.contains_key(key)
    }

    pub fn get_neighbors(&self, key: T) -> Vec<Node<T>> {
        let mut neighbors: Vec<Node<T>> = self
            .edges
            .iter()
            .filter_map(|Edge { from, to, weight }| {
                if from == &key {
                    self.nodes.get(&to)
                } else if to == &key {
                    self.nodes.get(&from)
                } else {
                    None
                }
            })
            .cloned()
            .collect();
        neighbors.dedup();
        neighbors
    }

    pub fn get_nodes(&self) -> Vec<Node<T>> {
        self.nodes.values().cloned().collect()
    }

    pub fn get_edges(&self) -> Vec<Edge<T>> {
        self.edges.iter().cloned().collect()
    }

    pub fn get_shortest_path_lengths(&self, source: T) -> Option<HashMap<T, f64>> {
        if !self.contains(&source) {
            return None;
        }

        let mut lengths = HashMap::from([(source.clone(), 0.)]);
        let mut queue = VecDeque::from([(source, 0.)]);

        while let Some((node, length)) = queue.pop_front() {
            if length > *lengths.entry(node.clone()).or_insert(f64::MAX) {
                continue;
            }
            for edge in self
                .edges
                .iter()
                .filter(|Edge { from, to, weight }| from == &node || to == &node)
            {
                let neighbor = if edge.from == node {
                    &edge.to
                } else {
                    &edge.from
                };
                let total_length = length + edge.weight;

                let neighbor_length = lengths.entry(neighbor.clone()).or_insert(f64::MAX);
                if total_length < *neighbor_length {
                    *neighbor_length = total_length;
                    queue.push_back((neighbor.clone(), total_length));
                }
            }
        }
        Some(lengths)
    }

    pub fn to_dot(&self) -> String {
        let mut output = "digraph g {\n".to_string();
        self.edges.iter().for_each(|edge| {
            output.push_str(format!("\t\"{}\" -> \"{}\"\n", edge.from, edge.to).as_str())
        });
        output.push_str("}");
        output
    }

    pub fn save_graph(&self, path: &str) {
        std::fs::write(path, self.to_dot()).unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::{fixture, rstest};

    #[fixture]
    fn graph() -> Graph<String> {
        Graph::default()
    }

    #[fixture]
    fn a() -> Node<String> {
        Node::new("a".to_string())
    }

    #[fixture]
    fn b() -> Node<String> {
        Node::new("b".to_string())
    }

    #[fixture]
    fn c() -> Node<String> {
        Node::new("c".to_string())
    }

    #[rstest]
    fn test_add_node_adds_node(mut graph: Graph<String>, a: Node<String>) {
        graph.add_node(a.clone());
        assert_eq!(graph.nodes, HashMap::from([(a.clone().label, a)]));
    }

    #[rstest]
    fn test_add_nodes_adds_nodes(mut graph: Graph<String>, a: Node<String>, b: Node<String>) {
        let nodes = vec![a.clone(), b.clone()];
        graph.add_nodes(nodes);
        assert_eq!(
            graph.nodes,
            HashMap::from([(a.clone().label, a), (b.clone().label, b)])
        );
    }

    #[rstest]
    fn test_add_node_is_idempotent(mut graph: Graph<String>, a: Node<String>) {
        graph.add_node(a.clone());
        graph.add_node(a.clone());
        assert_eq!(graph.nodes, HashMap::from([(a.clone().label, a)]));
    }

    #[rstest]
    fn test_add_edge_adds_edge(mut graph: Graph<String>, a: Node<String>, b: Node<String>) {
        graph.add_nodes(vec![a.clone(), b.clone()]);
        graph.add_edge(Edge::new_unweighted(a.clone().label, b.clone().label));
        assert_eq!(graph.edges, vec![Edge::new_unweighted(a.label, b.label)]);
    }

    #[rstest]
    fn test_add_edges_adds_edges(mut graph: Graph<String>, a: Node<String>, b: Node<String>) {
        graph.add_edges(vec![
            Edge::new_unweighted(a.clone().label, b.clone().label),
            Edge::new_unweighted(a.clone().label, a.clone().label),
        ]);
        assert_eq!(
            graph.edges,
            vec![
                Edge::new_unweighted(a.clone().label, b.clone().label),
                Edge::new_unweighted(a.clone().label, a.clone().label)
            ]
        )
    }

    #[rstest]
    #[case(a.clone(), true)]
    #[case(b(), false)]
    fn test_contains_returns_true_iff_graph_contains_node(
        mut graph: Graph<String>,
        a: Node<String>,
        #[case] to_insert: Node<String>,
        #[case] expected: bool,
    ) {
        graph.add_node(to_insert.clone());
        assert_eq!(graph.contains(&a.label), expected);
    }

    #[rstest]
    fn test_get_neighbours_returns_neighbours(
        mut graph: Graph<String>,
        a: Node<String>,
        b: Node<String>,
        c: Node<String>,
    ) {
        let nodes = vec![a.clone(), b.clone(), c.clone()];
        graph.add_nodes(nodes);
        graph.add_edges(vec![
            Edge::new_unweighted(a.clone().label, b.clone().label),
            Edge::new_unweighted(a.clone().label, c.clone().label),
        ]);
        assert_eq!(graph.get_neighbors(a.label), vec![b, c]);
    }

    #[rstest]
    fn test_get_neighbours_doesnt_count_double_edges_as_two_neighbours(
        mut graph: Graph<String>,
        a: Node<String>,
        b: Node<String>,
    ) {
        let nodes = vec![a.clone(), b.clone()];
        graph.add_nodes(nodes);
        graph.add_edges(vec![
            Edge::new_unweighted(a.clone().label, b.clone().label),
            Edge::new_unweighted(a.clone().label, b.clone().label),
        ]);
        assert_eq!(graph.get_neighbors(a.label), vec![b])
    }

    #[rstest]
    fn test_graph_to_string_dot_notation(
        mut graph: Graph<String>,
        a: Node<String>,
        b: Node<String>,
        c: Node<String>,
    ) {
        graph.add_nodes(vec![a.clone(), b.clone(), c.clone()]);
        graph.add_edges(vec![
            Edge::new_unweighted(a.clone().label, b.clone().label),
            Edge::new_unweighted(b.clone().label, c.clone().label),
            Edge::new_unweighted(c.clone().label, a.clone().label),
        ]);
        assert_eq!(
            graph.to_dot(),
            "digraph g {\n\t\"a\" -> \"b\"\n\t\"b\" -> \"c\"\n\t\"c\" -> \"a\"\n}".to_string()
        );
    }

    #[rstest]
    fn test_get_shortest_path_lengths(
        mut graph: Graph<String>,
        a: Node<String>,
        b: Node<String>,
        c: Node<String>,
    ) {
        graph.add_nodes(vec![a.clone(), b.clone(), c.clone()]);
        graph.add_edges(vec![
            Edge::new(a.clone().label, b.clone().label, 2.),
            Edge::new(b.clone().label, c.clone().label, 3.),
        ]);
        assert_eq!(
            graph.get_shortest_path_lengths(a.clone().label).unwrap(),
            HashMap::from([
                (a.clone().label, 0.),
                (b.clone().label, 2.),
                (c.clone().label, 5.),
            ]),
        );
        assert_eq!(
            graph.get_shortest_path_lengths(b.clone().label).unwrap(),
            HashMap::from([
                (a.clone().label, 2.),
                (b.clone().label, 0.),
                (c.clone().label, 3.),
            ]),
        );
        assert_eq!(
            graph.get_shortest_path_lengths(c.clone().label).unwrap(),
            HashMap::from([
                (a.clone().label, 5.),
                (b.clone().label, 3.),
                (c.clone().label, 0.),
            ]),
        );
    }

    #[rstest]
    fn test_get_shortest_path_lengths_no_such_key(graph: Graph<String>) {
        assert!(graph.get_shortest_path_lengths("abc".to_string()).is_none())
    }
}
