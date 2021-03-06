import pytest
import random
import os
import sys
sys.path.append(os.path.join('..'))
import binary_search_naive as B

# Variables for use in the tests
trials = 20
int_range = (1, 100000)

# Utility functions

def make_random_tree(size=1000):
    random_keys = get_random_list_unique()
    return B.populate_tree(random_keys)

def get_random_list_unique(size=1000):
    """Function to generate list of unique integers for use as keys."""
    random_list = [random.randint(*int_range) for i in range(size)]
    return list(set(random_list))

# Tests begin here

def test_insertion():
    """Test insertion of lists of random integers"""
    for trial in range(trials):
        random_keys = get_random_list_unique()
        tree = B.populate_tree(random_keys)
        assert B.inorder_traverse(tree) == sorted(random_keys)

def test_insertion_including_0():
    """Test outcome if keys include 0."""
    random_keys = get_random_list_unique()
    random_keys.append(0)
    tree = B.populate_tree(random_keys)
    assert B.inorder_traverse(tree) == sorted(random_keys)

def test_insertion_non_int_keys():
    """Test outcome if keys are not integers."""
    random_keys = get_random_list_unique()
    random_keys.append(1.3)
    assert pytest.raises(SystemExit, "B.populate_tree(random_keys)")

def test_insertion_dup_keys():
    """Test outcome if keys are not unique."""
    random_keys = get_random_list_unique()
    random_keys.append(random_keys[-1])
    assert pytest.raises(SystemExit, "B.populate_tree(random_keys)")

def test_keys_diff_number_data():
    """Test outcome if keys and data differ in cardinality."""
    random_keys = get_random_list_unique(1000)
    random_data = get_random_list_unique(500)
    assert pytest.raises(SystemExit, 
            "B.populate_tree(random_keys, random_data)")

def test_insert_empty():
    """Test outcome if no data is supplied to `populate_tree`."""
    tree = B.populate_tree()
    assert tree == None

def test_inorder_empty():
    """Test `inorder_traverse` if no data is supplied to `populate_tree`."""
    tree = B.populate_tree()
    assert B.inorder_traverse(tree) == []

def test_max():
    """Find maximum value."""
    random_keys = get_random_list_unique()
    assert B.max(B.populate_tree(random_keys)).key == max(random_keys)

def test_min():
    """Find minimum value."""
    random_keys = get_random_list_unique()
    assert B.min(B.populate_tree(random_keys)).key == min(random_keys)

def test_search_random():
    """Find a given random key"""
    random_keys = get_random_list_unique()
    tree = B.populate_tree(random_keys)
    for trial in range(trials):
        random_key = random.choice(random_keys)
        assert B.search(tree, random_key).key == random_key

def test_search_nonexistent():
    """Find a key that does not exist."""
    random_keys = get_random_list_unique(10)
    tree = B.populate_tree(random_keys)
    to_find = random_keys[0]
    while to_find in random_keys:
        to_find = random.randint(*int_range)
    assert B.search(tree, to_find) == None

def test_delete_leaf():
    """Delete random leaves from the tree."""
    tree = make_random_tree()
    for trial in range(trials):
        to_delete = B.breadthfirst_traverse(tree)[-1]
        tree = B.delete(tree, to_delete)
        assert B.search(tree, to_delete) == None

def test_delete_non_root_has_only_right_child():
    for trial in range(trials):
        random_keys = get_random_list_unique()
        tree = B.populate_tree(random_keys)
        # To start while loop, temporarily use this value:
        to_delete = tree
        while not (to_delete.right and 
                (not to_delete.left) and 
                to_delete.parent):
            random_key = random.choice(random_keys)
            to_delete = B.search(tree, random_key)
        tree = B.delete(tree, random_key)
        assert B.search(tree, random_key) == None

def test_delete_non_root_has_only_left_child():
    for trial in range(trials):
        random_keys = get_random_list_unique()
        tree = B.populate_tree(random_keys)
        # To start while loop, temporarily use this value:
        to_delete = tree
        while not (to_delete.left and 
                (not to_delete.right) and 
                to_delete.parent):
            random_key = random.choice(random_keys)
            to_delete = B.search(tree, random_key)
        tree = B.delete(tree, random_key)
        assert B.search(tree, random_key) == None

def test_delete_non_root_has_two_children():
    for trial in range(trials):
        random_keys = get_random_list_unique()
        tree = B.populate_tree(random_keys)
        # To start while loop, temporarily use this value:
        to_delete = tree
        while not (to_delete.left and to_delete.right and to_delete.parent):
            random_key = random.choice(random_keys)
            to_delete = B.search(tree, random_key)
        tree = B.delete(tree, random_key)
        assert B.search(tree, random_key) == None

def test_delete_root():
    """Delete random leaves from the tree."""
    for trial in range(trials):
        tree = make_random_tree()
        to_delete = tree.key
        tree = B.delete(tree, to_delete)
        assert B.search(tree, to_delete) == None

def test_delete_nonexistent():
    """Test outcome if delete is called on non-existent key."""
    random_keys = get_random_list_unique(10)
    tree = B.populate_tree(random_keys)
    # To start while loop, temporarily use value that definitely exists.
    to_delete = random_keys[0]
    while to_delete in random_keys:
        to_delete = random.randint(*int_range)
    assert B.delete(tree, to_delete) == None
