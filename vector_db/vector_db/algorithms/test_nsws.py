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
