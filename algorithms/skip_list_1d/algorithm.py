"""
Notes:
    This implementation becomes foundation of HNSW algorithm.
    It is a graph-based algorithm for approximate nearest neighbor search.

Reference:
Learnings from:
https://www.analyticsvidhya.com/blog/2023/10/introduction-to-hnsw-hierarchical-navigable-small-world/
"""

from __future__ import annotations

import random
import uuid
from typing import List, Optional, Any


class LinkedListNode:
    def __init__(self, value: float):
        self.id = uuid.uuid4()
        self.value = value
        self.forward: list[LinkedListNode] = []
        self.backward: list[LinkedListNode] = []

    def __repr__(self):
        return f"Node({str(self.id)[:5]}: {self.value})"

    def __str__(self):
        return f"Node({str(self.id)[:5]}: {self.value})"


class SkipList1D:
    """
    SkipList1D is a 1-dimensional skip list implementation
    for approximate nearest neighbor search.

    Constraints:
    - doesn't take +-inf values
    """

    def __init__(
        self,
        max_level: int = 10,
        level_increase_probability: float = 0.5,
        seed: Optional[int] = 0,
    ):
        # Max level should be positive int
        if max_level <= 0:
            raise ValueError("max_level should be a positive integer")

        self.max_level = max_level
        self.level_increase_probability = level_increase_probability
        self._random = random.Random(seed)
        self._head, self._tail = self._initialize_end_node(max_level)
        self._total_nodes = 0

    def _initialize_end_node(self, max_level: int) -> LinkedListNode:
        """
        Initialize the leftmost node with negative infinity value,
        so that the first node is always less than any other node.

        Also, setting it to have max_level forward pointers,
        so we can use it as the starting point for all levels.

        :return: First node of the skip_list
        """
        left_node = LinkedListNode(float("-inf"))
        right_node = LinkedListNode(float("inf"))
        for i in range(max_level):
            left_node.forward.append(right_node)
            left_node.backward.append(right_node)
            right_node.forward.append(left_node)
            right_node.backward.append(left_node)
        return left_node, right_node

    def insert(self, value: float) -> None:
        new_node = LinkedListNode(value)
        current_head = self._head

        # Reverse order of last seen nodes in each level
        head_levels = []

        top_level = self.max_level - 1
        for i in range(top_level, -1, -1):
            while current_head.forward[i] and current_head.forward[i].value <= value:
                # Handling edge case where item was +inf
                if current_head.forward[i] == self._tail:
                    break
                current_head = current_head.forward[i]
            head_levels.append(current_head)

        # Handle the edge case where item was +inf
        if current_head == self._tail:
            head_levels = []
            for i in range(top_level, -1, -1):
                head_levels.append(current_head.backward[i])

        current_level = 0
        while current_level < self.max_level:
            current_level_head = head_levels.pop()
            new_node.forward.append(current_level_head.forward[current_level])
            new_node.backward.append(current_level_head)
            current_level_head.forward[current_level] = new_node
            # Randomly decide not to increase this level
            current_level += 1
            if self._random.random() > self.level_increase_probability:
                break

        self._total_nodes += 1

    def search(self, value: float, k: int) -> List[float]:
        current_head = self._head

        current_level = self.max_level - 1

        # Find current or left closest current_head
        for i in range(current_level, -1, -1):
            while current_head.forward[i] and current_head.forward[i].value <= value:
                # Handling edge case where item was +inf
                if current_head.forward[i] == self._tail:
                    break
                current_head = current_head.forward[i]

        left_node = current_head
        right_node = current_head.forward[0]
        if left_node == self._head:
            left_node = None
        if right_node == self._tail:
            right_node = None

        neighbours = []
        k = max(0, k)
        while k > 0 and left_node and right_node:
            left_distance = value - left_node.value
            right_distance = right_node.value - value
            if left_distance < right_distance:
                neighbours.append(left_node)
                left_node = left_node.backward[0]
            else:
                neighbours.append(right_node)
                right_node = right_node.forward[0]
            if left_node == self._head:
                left_node = None
            if right_node == self._tail:
                right_node = None
            k -= 1

        # If right_node is None, we need to keep adding left_node
        while k > 0 and right_node is None and left_node != self._head:
            neighbours.append(left_node)
            left_node = left_node.backward[0]
            k -= 1

        # If left_node is None, we need to keep adding right_node
        while k > 0 and left_node is None and right_node != self._tail:
            neighbours.append(right_node)
            right_node = right_node.forward[0]
            k -= 1

        # Remove head and tail if they are present
        neighbours = [node for node in neighbours]

        # Returns in closest to farthest order
        return [n.value for n in neighbours]
