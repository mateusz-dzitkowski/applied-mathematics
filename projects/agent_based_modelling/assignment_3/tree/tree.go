package tree

import (
	"math"
	"sort"
)

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

func (t *Tree[T]) FindKNearestNeighbours(pos Position, k int) []Object[T] {
	result := make([]Object[T], 0)
	closestNodes := make([]Node[T], 0)
	closestDist := math.MaxInt

	findKNearestNeighbours(t.root, pos, k, 0, &closestNodes, &closestDist)
	for _, node := range closestNodes {
		result = append(result, node.object)
	}

	sort.Slice(result, func(i, j int) bool {
		return result[i].Pos.distanceSq(pos) < result[j].Pos.distanceSq(pos)
	})

	return result
}

func findKNearestNeighbours[T any](node *Node[T], target Position, k int, depth int, closestNodes *[]Node[T], closestDist *int) {
	if node == nil {
		return
	}

	*closestDist = min(node.object.Pos.distanceSq(target), *closestDist)
	*closestNodes = append(*closestNodes, *node)

	axis := depth % 2

	var next, other *Node[T]

	if goLeft(axis, node, target) {
		next = node.left
		other = node.right
	} else {
		next = node.right
		other = node.left
	}

	findKNearestNeighbours[T](next, target, k, depth+1, closestNodes, closestDist)

	delta := target.getCoord(axis) - node.object.Pos.getCoord(axis)
	delta2 := delta * delta
	if len(*closestNodes) < k || delta2 < *closestDist {
		findKNearestNeighbours[T](other, target, k, depth+1, closestNodes, closestDist)
	}
}

func insert[T any](node *Node[T], object Object[T], depth int) *Node[T] {
	if node == nil {
		return &Node[T]{object: object}
	}

	axis := depth % 2

	if goLeft(axis, node, object.Pos) {
		node.left = insert(node.left, object, depth+1)
	} else {
		node.right = insert(node.right, object, depth+1)
	}

	return node
}

func goLeft[T any](axis int, node *Node[T], pos Position) bool {
	return (axis == 0 && pos.X < node.object.Pos.X) || (axis == 1 && pos.Y < node.object.Pos.Y)
}
