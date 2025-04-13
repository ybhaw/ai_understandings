"""
Got the idea from:
https://www.analyticsvidhya.com/blog/2023/10/introduction-to-hnsw-hierarchical-navigable-small-world/
"""

from typing import List

_incrementor = 0


class Node:
    def __init__(self, value):
        self.value = value
        self.neighbors = []
        global _incrementor
        self.id = _incrementor
        _incrementor += 1

    def add_neighbor(self, node):
        if node == self:
            return
        if node not in self.neighbors:
            self.neighbors.append(node)
            node.add_neighbor(self)

    def __repr__(self):
        return f"Node(id={self.id}, value={self.value})"

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Node):
            return False
        return self.id < other.id


class NSW:
    def __init__(self):
        self.nodes = []

    def insert(self, value: list[float]) -> Node:
        node = Node(value)
        if not self.nodes:
            self.nodes.append(node)
            return node
        all_neighbours = [self._find_closest(node)]
        i = 0
        while i < len(all_neighbours):
            current_node = all_neighbours[i]
            node.add_neighbor(current_node)
            for neighbor in current_node.neighbors:
                if (
                    neighbor not in all_neighbours
                    and self._compare_a_to_c_and_a_to_b_to_c(
                        node, current_node, neighbor
                    )
                ):
                    all_neighbours.append(neighbor)
            i += 1
        self.nodes.append(node)
        return node

    def _find_closest(self, node: Node) -> Node:
        closest = None
        if not self.nodes:
            raise ValueError("No nodes in the graph")
        min_distance = float("inf")
        nodes_to_look: List[Node] = [self.nodes[0]]
        i = 0
        while i < len(nodes_to_look):
            current_node = nodes_to_look[i]
            distance = self._distance_compare(current_node, node)
            if distance < min_distance:
                min_distance = distance
                closest = current_node
            closest_next_neighbor = None
            next_closest_distance = float("inf")
            for neighbor in current_node.neighbors:
                new_close = self._distance_compare(neighbor, node)
                if new_close < next_closest_distance:
                    next_closest_distance = new_close
                    closest_next_neighbor = neighbor
            if closest_next_neighbor is not None:
                if next_closest_distance < min_distance:
                    nodes_to_look.append(closest_next_neighbor)
            i += 1
        assert closest is not None
        return closest

    def _distance_compare(self, node1: Node, node2: Node, /):
        square = 0
        for a, b in zip(node1.value, node2.value):
            square += (a - b) ** 2
        return square

    def _compare_a_to_c_and_a_to_b_to_c(self, a: Node, b: Node, c: Node) -> bool:
        """
        Compare a->c and a->b->c
        Useful to determine if a node needs to be added to nearest neighbors
        :return: True if a->c is closer or equal to a->b->c
        """
        a_to_c = self._distance_compare(a, c) ** 0.5
        a_to_b = self._distance_compare(a, b) ** 0.5
        return a_to_c <= a_to_b

    def search(self, vector: List[float], k: int = 1) -> List[List[float]]:
        if not self.nodes:
            raise ValueError("No nodes in the graph")
        node = Node(vector)
        results = []
        closest = self._find_closest(node)
        results.append(closest)

        k = min(k, len(self.nodes))
        i = 0
        while len(results) < k:
            current_node = results[i]
            results.extend(
                sorted(
                    current_node.neighbors,
                    key=lambda x: self._distance_compare(x, node),
                )
            )
            i += 1
        return [node.value for node in results[:k]]
