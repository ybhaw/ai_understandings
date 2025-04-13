from algorithms.skip_list_1d.algorithm import SkipList1D


def test_Should_insert_new_node_When_no_nodes_are_present():
    sut = SkipList1D()
    sut.insert(1.0)
    results = sut.search(0, 10)
    assert results == [1.0]


def test_Should_insert_multiple_nodes_When_no_nodes_are_present():
    sut = SkipList1D()
    sut.insert(1.0)
    sut.insert(2.0)
    sut.insert(3.0)
    results = sut.search(0, 10)
    assert results == [1.0, 2.0, 3.0]


def test_Should_give_correct_results_When_middle_node_is_searched():
    sut = SkipList1D()
    sut.insert(1.0)
    sut.insert(2.0)
    sut.insert(3.0)
    results = sut.search(2.0, 10)
    assert results == [2.0, 3.0, 1.0]


def test_Should_give_correct_results_When_more_elements_are_present():
    inputs = range(0, 10)
    sut = SkipList1D()
    for i in inputs:
        sut.insert(float(i))
    results = sut.search(5.0, 5)
    assert results == [5.0, 6.0, 4.0, 7.0, 3.0]


def test_Should_support_adding_negative_infinity():
    sut = SkipList1D()
    sut.insert(float("-inf"))
    results = sut.search(float("-inf"), 10)
    assert results == [float("-inf")]


def test_Should_support_adding_positive_infinity():
    sut = SkipList1D()
    sut.insert(float("inf"))
    results = sut.search(float("inf"), 10)
    assert results == [float("inf")]


def test_Should_return_n_items_When_all_items_are_same():
    sut = SkipList1D()
    for _ in range(10):
        sut.insert(1.0)
    results = sut.search(1.0, 5)
    assert results == [1.0, 1.0, 1.0, 1.0, 1.0]
