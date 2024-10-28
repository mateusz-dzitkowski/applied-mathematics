package tree

import "math"

type Position struct {
	X, Y int
}

func (p Position) distanceSq(other Position) int {
	return (p.X-other.X)*(p.X-other.X) + (p.Y-other.Y)*(p.Y-other.Y)
}

func (p Position) getCoord(axis int) int {
	if axis == 0 {
		return p.X
	}
	return p.Y
}

type Object[T any] struct {
	Pos   Position
	Props T
}

type Node[T any] struct {
	object Object[T]
	left   *Node[T]
	right  *Node[T]
}

type Tree[T any] struct {
	root *Node[T]
}

func New[T any]() *Tree[T] {
	return &Tree[T]{}
}

func (t *Tree[T]) Insert(object Object[T]) {
	t.root = insert(t.root, object, 0)
}

func (t *Tree[T]) FindNearestNeighbours(node *Node[T], k int) []*Node[T] {
	return []*Node[T]{} // TODO
}

func insert[T any](node *Node[T], object Object[T], depth int) *Node[T] {
	if node == nil {
		return &Node[T]{object: object}
	}

	axis := depth % 2

	if goLeft(axis, node, object) {
		node.left = insert(node.left, object, depth+1)
	} else {
		node.right = insert(node.right, object, depth+1)
	}

	return node
}

func findNearestNeighbours[T any](node *Node[T], target Object[T], k, depth int, objects *[]Object[T], distances *[]int) {
	if node == nil {
		return
	}

	dist := node.object.Pos.distanceSq(target.Pos)
	axis := depth % 2
	var next, other *Node[T]

	if goLeft(axis, node, target) {
		next = node.left
		other = node.right
	} else {
		next = node.right
		other = node.left
	}

	findNearestNeighbours[T](next, target, k, depth+1, objects, distances)

	if len(*objects) < k || math.Abs(target.Pos.getCoord(axis)-node.object.Pos.getCoord(axis)) < (*distances)[len(*distances)-1] {

	}
}

func goLeft[T any](axis int, node *Node[T], object Object[T]) bool {
	return (axis == 0 && object.Pos.X < node.object.Pos.X) || (axis == 1 && object.Pos.Y < node.object.Pos.Y)
}
