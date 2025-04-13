from vector_db.algorithms.nsw import NSW


def test_Should_add_new_node_When_no_nodes_present():
    # Arrange
    nsw = NSW()
    value = [1.0, 2.0, 3.0]

    # Act
    node = nsw.insert(value)

    # Assert
    assert len(nsw.nodes) == 1
    assert node.value == value
    assert node.neighbors == []
    assert nsw.search(value, 1) == [[1.0, 2.0, 3.0]]


def test_Should_pass_When_multiple_nodes_are_address():
    # Arrange
    nsw = NSW()
    value1 = [1.0, 2.0, 3.0]
    value2 = [4.0, 5.0, 6.0]
    value3 = [7.0, 8.0, 9.0]

    # Act
    node1 = nsw.insert(value1)
    assert len(nsw.nodes) == 1
    assert node1.neighbors == []

    node2 = nsw.insert(value2)
    assert len(nsw.nodes) == 2
    assert node1.neighbors == [node2]
    assert node2.neighbors == [node1]

    node3 = nsw.insert(value3)
    assert len(nsw.nodes) == 3
    assert node1.neighbors == [node2]
    assert sorted(node2.neighbors) == sorted([node3, node1])
    assert node3.neighbors == [node2]


def test_Should_not_add_farther_node_as_index_When_distance_is_greater():
    # Arrange
    nsw = NSW()
    value1 = [1.0, 0.0]
    value2 = [4.0, 0.0]
    value3 = [7.0, 1.0]

    # Act
    node1 = nsw.insert(value1)
    node2 = nsw.insert(value2)
    node3 = nsw.insert(value3)

    # Assert
    assert len(nsw.nodes) == 3
    assert node1.neighbors == [node2]
    assert sorted(node2.neighbors) == sorted([node1, node3])
    assert node3.neighbors == [node2]


def test_Should_get_nearest_neighbors_When_searched():
    # Arrange
    nsw = NSW()
    value1 = [1.0, 2.0, 3.0]
    value2 = [4.0, 5.0, 6.0]
    value3 = [7.0, 8.0, 9.0]
    nsw.insert(value1)
    nsw.insert(value2)
    nsw.insert(value3)

    # Act
    neighbors = nsw.search([3.5, 5.5, 6.5], 2)

    # Assert
    assert len(neighbors) == 2
    assert neighbors[0] == [4.0, 5.0, 6.0]
    assert neighbors[1] == [7.0, 8.0, 9.0]
