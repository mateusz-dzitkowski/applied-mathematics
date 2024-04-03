pub trait Edgy<T> {
    fn from(&self) -> &T;

    fn to(&self) -> &T;

    fn weight(&self) -> f64;
}

#[derive(Debug, PartialEq, Clone, Default)]
pub struct WeightedEdge<T> {
    from: T,
    to: T,
    weight: f64,
}

impl<T> WeightedEdge<T> {
    pub fn new(from: T, to: T, weight: f64) -> Self {
        Self { from, to, weight }
    }
}

impl<T> Edgy<T> for WeightedEdge<T> {
    fn from(&self) -> &T {
        &self.from
    }

    fn to(&self) -> &T {
        &self.to
    }

    fn weight(&self) -> f64 {
        self.weight
    }
}

#[derive(Debug, PartialEq, Clone, Default)]
pub struct UnweightedEdge<T> {
    from: T,
    to: T,
}

impl<T> UnweightedEdge<T> {
    pub fn new(from: T, to: T) -> Self {
        Self { from, to }
    }
}

impl<T> Edgy<T> for UnweightedEdge<T> {
    fn from(&self) -> &T {
        &self.from
    }

    fn to(&self) -> &T {
        &self.to
    }
    fn weight(&self) -> f64 {
        1.
    }
}
