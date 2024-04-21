mod random;

const N: u32 = 2000;
const P: f64 = 0.2;


fn main() {
    for p in (0. .. 1.).step_by(0.01) {
        dbg!(p);
    }
    let g = random::random_graph(N, P);
    dbg!(g.node_count());
    dbg!((P * N as f64 * (N as f64 - 1.) / 2.) as u32);
    dbg!(g.edge_count());
}
