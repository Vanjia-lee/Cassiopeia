import networkx as nx
import numpy as np

from cassiopeia.tools import (
    IIDExponentialBLE,
    IIDExponentialBLEGridSearchCV,
    IIDExponentialLineageTracer,
    Tree,
)


def test_no_mutations():
    r"""
    Tree topology is just a branch 0->1.
    There is one unmutated character i.e.:
        root [state = '0']
        |
        v
        child [state = '0']
    This is thus the simplest possible example of no mutations, and the MLE
    branch length should be 0
    """
    tree = nx.DiGraph()
    tree.add_node(0), tree.add_node(1)
    tree.add_edge(0, 1)
    tree.nodes[0]["characters"] = "0"
    tree.nodes[1]["characters"] = "0"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(tree.get_edge_length(0, 1), 0.0)
    np.testing.assert_almost_equal(tree.get_age(0), 0.0)
    np.testing.assert_almost_equal(tree.get_age(1), 0.0)
    np.testing.assert_almost_equal(log_likelihood, 0.0)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_saturation():
    r"""
    Tree topology is just a branch 0->1.
    There is one mutated character i.e.:
        root [state = '0']
        |
        v
        child [state = '1']
    This is thus the simplest possible example of saturation, and the MLE
    branch length should be infinity (>15 for all practical purposes)
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1])
    tree.add_edge(0, 1)
    tree.nodes[0]["characters"] = "0"
    tree.nodes[1]["characters"] = "1"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    assert tree.get_edge_length(0, 1) > 15.0
    assert tree.get_age(0) > 15.0
    np.testing.assert_almost_equal(tree.get_age(1), 0.0)
    np.testing.assert_almost_equal(log_likelihood, 0.0, decimal=5)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_hand_solvable_problem_1():
    r"""
    Tree topology is just a branch 0->1.
    There is one mutated character and one unmutated character, i.e.:
        root [state = '00']
        |
        v
        child [state = '01']
    The solution can be verified by hand. The optimization problem is:
        min_{r * t0} log(exp(-r * t0)) + log(1 - exp(-r * t0))
    The solution is r * t0 = ln(2) ~ 0.693
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1])
    tree.add_edge(0, 1)
    tree.nodes[0]["characters"] = "00"
    tree.nodes[1]["characters"] = "01"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(
        tree.get_edge_length(0, 1), np.log(2), decimal=3
    )
    np.testing.assert_almost_equal(tree.get_age(0), np.log(2), decimal=3)
    np.testing.assert_almost_equal(tree.get_age(1), 0.0)
    np.testing.assert_almost_equal(log_likelihood, -1.386, decimal=3)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_hand_solvable_problem_2():
    r"""
    Tree topology is just a branch 0->1.
    There are two mutated characters and one unmutated character, i.e.:
        root [state = '000']
        |
        v
        child [state = '011']
    The solution can be verified by hand. The optimization problem is:
        min_{r * t0} log(exp(-r * t0)) + 2 * log(1 - exp(-r * t0))
    The solution is r * t0 = ln(3) ~ 1.098
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1])
    tree.add_edge(0, 1)
    tree.nodes[0]["characters"] = "000"
    tree.nodes[1]["characters"] = "011"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(
        tree.get_edge_length(0, 1), np.log(3), decimal=3
    )
    np.testing.assert_almost_equal(tree.get_age(0), np.log(3), decimal=3)
    np.testing.assert_almost_equal(tree.get_age(1), 0.0)
    np.testing.assert_almost_equal(log_likelihood, -1.909, decimal=3)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_hand_solvable_problem_3():
    r"""
    Tree topology is just a branch 0->1.
    There are two unmutated characters and one mutated character, i.e.:
        root [state = '000']
        |
        v
        child [state = '001']
    The solution can be verified by hand. The optimization problem is:
        min_{r * t0} 2 * log(exp(-r * t0)) + log(1 - exp(-r * t0))
    The solution is r * t0 = ln(1.5) ~ 0.405
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1])
    tree.add_edge(0, 1)
    tree.nodes[0]["characters"] = "000"
    tree.nodes[1]["characters"] = "001"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(
        tree.get_edge_length(0, 1), np.log(1.5), decimal=3
    )
    np.testing.assert_almost_equal(tree.get_age(0), np.log(1.5), decimal=3)
    np.testing.assert_almost_equal(tree.get_age(1), 0.0)
    np.testing.assert_almost_equal(log_likelihood, -1.909, decimal=3)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_small_tree_with_no_mutations():
    r"""
    Perfect binary tree with no mutations: Should give edges of length 0
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1, 2, 3, 4, 5, 6])
    tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    tree.nodes[0]["characters"] = "0000"
    tree.nodes[1]["characters"] = "0000"
    tree.nodes[2]["characters"] = "0000"
    tree.nodes[3]["characters"] = "0000"
    tree.nodes[4]["characters"] = "0000"
    tree.nodes[5]["characters"] = "0000"
    tree.nodes[6]["characters"] = "0000"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    for edge in tree.edges():
        np.testing.assert_almost_equal(
            tree.get_edge_length(*edge), 0, decimal=3
        )
    np.testing.assert_almost_equal(log_likelihood, 0.0, decimal=3)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_small_tree_with_one_mutation():
    r"""
    Perfect binary tree with one mutation at a node 6: Should give very short
    edges 1->3,1->4,0->2 and very long edges 0->1,2->5,2->6.
    The problem can be solved by hand: it trivially reduces to a 1-dimensional
    problem:
        min_{r * t0} 2 * log(exp(-r * t0)) + log(1 - exp(-r * t0))
    The solution is r * t0 = ln(1.5) ~ 0.405
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1, 2, 3, 4, 5, 6]),
    tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    tree.nodes[0]["characters"] = "0"
    tree.nodes[1]["characters"] = "0"
    tree.nodes[2]["characters"] = "0"
    tree.nodes[3]["characters"] = "0"
    tree.nodes[4]["characters"] = "0"
    tree.nodes[5]["characters"] = "0"
    tree.nodes[6]["characters"] = "1"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(tree.get_edge_length(0, 1), 0.405, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(0, 2), 0.0, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(1, 3), 0.0, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(1, 4), 0.0, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(2, 5), 0.405, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(2, 6), 0.405, decimal=3)
    np.testing.assert_almost_equal(log_likelihood, -1.909, decimal=3)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_small_tree_with_saturation():
    r"""
    Perfect binary tree with saturation. The edges which saturate should thus
    have length infinity (>15 for all practical purposes)
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1, 2, 3, 4, 5, 6]),
    tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    tree.nodes[0]["characters"] = "0"
    tree.nodes[1]["characters"] = "0"
    tree.nodes[2]["characters"] = "1"
    tree.nodes[3]["characters"] = "1"
    tree.nodes[4]["characters"] = "1"
    tree.nodes[5]["characters"] = "1"
    tree.nodes[6]["characters"] = "1"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    assert tree.get_edge_length(0, 2) > 15.0
    assert tree.get_edge_length(1, 3) > 15.0
    assert tree.get_edge_length(1, 4) > 15.0
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_small_tree_regression():
    r"""
    Regression test. Cannot be solved by hand. We just check that this solution
    never changes.
    """
    # Perfect binary tree with normal amount of mutations on each edge
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1, 2, 3, 4, 5, 6]),
    tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    tree.nodes[0]["characters"] = "000000000"
    tree.nodes[1]["characters"] = "100000000"
    tree.nodes[2]["characters"] = "000006000"
    tree.nodes[3]["characters"] = "120000000"
    tree.nodes[4]["characters"] = "103000000"
    tree.nodes[5]["characters"] = "000056700"
    tree.nodes[6]["characters"] = "000406089"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(tree.get_edge_length(0, 1), 0.203, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(0, 2), 0.082, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(1, 3), 0.175, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(1, 4), 0.175, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(2, 5), 0.295, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(2, 6), 0.295, decimal=3)
    np.testing.assert_almost_equal(log_likelihood, -22.689, decimal=3)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_small_symmetric_tree():
    r"""
    Symmetric tree should have equal length edges.
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1, 2, 3, 4, 5, 6]),
    tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    tree.nodes[0]["characters"] = "000"
    tree.nodes[1]["characters"] = "100"
    tree.nodes[2]["characters"] = "100"
    tree.nodes[3]["characters"] = "110"
    tree.nodes[4]["characters"] = "110"
    tree.nodes[5]["characters"] = "110"
    tree.nodes[6]["characters"] = "110"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(
        tree.get_edge_length(0, 1), tree.get_edge_length(0, 2)
    )
    np.testing.assert_almost_equal(
        tree.get_edge_length(1, 3), tree.get_edge_length(1, 4)
    )
    np.testing.assert_almost_equal(
        tree.get_edge_length(1, 4), tree.get_edge_length(2, 5)
    )
    np.testing.assert_almost_equal(
        tree.get_edge_length(2, 5), tree.get_edge_length(2, 6)
    )
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_small_tree_with_infinite_legs():
    r"""
    Perfect binary tree with saturated leaves. The first level of the tree
    should be normal (can be solved by hand, solution is log(2)),
    the branches for the leaves should be infinity (>15 for all practical
    purposes)
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1, 2, 3, 4, 5, 6]),
    tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    tree.nodes[0]["characters"] = "00"
    tree.nodes[1]["characters"] = "10"
    tree.nodes[2]["characters"] = "10"
    tree.nodes[3]["characters"] = "11"
    tree.nodes[4]["characters"] = "11"
    tree.nodes[5]["characters"] = "11"
    tree.nodes[6]["characters"] = "11"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(tree.get_edge_length(0, 1), 0.693, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(0, 2), 0.693, decimal=3)
    assert tree.get_edge_length(1, 3) > 15
    assert tree.get_edge_length(1, 4) > 15
    assert tree.get_edge_length(2, 5) > 15
    assert tree.get_edge_length(2, 6) > 15
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_on_simulated_data():
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1, 2, 3, 4, 5, 6]),
    tree.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    tree.nodes[0]["age"] = 1
    tree.nodes[1]["age"] = 0.9
    tree.nodes[2]["age"] = 0.1
    tree.nodes[3]["age"] = 0
    tree.nodes[4]["age"] = 0
    tree.nodes[5]["age"] = 0
    tree.nodes[6]["age"] = 0
    np.random.seed(1)
    tree = Tree(tree)
    IIDExponentialLineageTracer(
        mutation_rate=1.0, num_characters=100
    ).overlay_lineage_tracing_data(tree)
    for node in tree.nodes():
        tree.set_age(node, -1)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    assert 0.9 < tree.get_age(0) < 1.1
    assert 0.8 < tree.get_age(1) < 1.0
    assert 0.05 < tree.get_age(2) < 0.15
    np.testing.assert_almost_equal(tree.get_age(3), 0)
    np.testing.assert_almost_equal(tree.get_age(4), 0)
    np.testing.assert_almost_equal(tree.get_age(5), 0)
    np.testing.assert_almost_equal(tree.get_age(6), 0)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_subtree_collapses_when_no_mutations():
    r"""
    A subtree with no mutations should collapse to 0. It reduces the problem to
    the same as in 'test_hand_solvable_problem_1'
    """
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1, 2, 3, 4]),
    tree.add_edges_from([(0, 1), (1, 2), (1, 3), (0, 4)])
    tree.nodes[0]["characters"] = "0"
    tree.nodes[1]["characters"] = "1"
    tree.nodes[2]["characters"] = "1"
    tree.nodes[3]["characters"] = "1"
    tree.nodes[4]["characters"] = "0"
    tree = Tree(tree)
    model = IIDExponentialBLE()
    model.estimate_branch_lengths(tree)
    log_likelihood = model.log_likelihood
    np.testing.assert_almost_equal(
        tree.get_edge_length(0, 1), np.log(2), decimal=3
    )
    np.testing.assert_almost_equal(tree.get_edge_length(1, 2), 0.0, decimal=3)
    np.testing.assert_almost_equal(tree.get_edge_length(1, 3), 0.0, decimal=3)
    np.testing.assert_almost_equal(
        tree.get_edge_length(0, 4), np.log(2), decimal=3
    )
    np.testing.assert_almost_equal(log_likelihood, -1.386, decimal=3)
    log_likelihood_2 = IIDExponentialBLE.log_likelihood(tree)
    np.testing.assert_almost_equal(log_likelihood, log_likelihood_2, decimal=3)


def test_IIDExponentialBLEGridSearchCV():
    tree = nx.DiGraph()
    tree.add_nodes_from([0, 1]),
    tree.add_edges_from([(0, 1)])
    tree.nodes[0]["characters"] = "000"
    tree.nodes[1]["characters"] = "001"
    tree = Tree(tree)
    model = IIDExponentialBLEGridSearchCV(
        minimum_branch_lengths=(0, 1.0, 3.0),
        l2_regularizations=(0,),
        verbose=True,
    )
    model.estimate_branch_lengths(tree)
    minimum_branch_length = model.minimum_branch_length
    np.testing.assert_almost_equal(minimum_branch_length, 1.0)