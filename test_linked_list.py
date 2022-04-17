
import linked_list

def test_linked_list_iterate():
    my_list = linked_list.LinkedList([1, 5, 4])
    assert len(my_list) == 3
    for (actual,expected) in zip(my_list, [1, 5, 4]):
        assert type(actual) == type(expected)
        assert actual == expected

def test_linked_list_push_and_pop():
    my_list = linked_list.LinkedList([2, 3])
    my_list.push_back(4)
    my_list.push_front(1)
    assert my_list[0] == 1
    assert my_list[3] == 4
    assert len(my_list) == 4

    x = my_list.pop_front()
    assert x == 1
    x = my_list.pop_back()
    assert x == 4
    assert len(my_list) == 2
    
    x = my_list.pop_front()
    assert x == 2
    x = my_list.pop_back()
    assert x == 3

    assert len(my_list) == 0

def test_repr_linked_list():
    my_list = linked_list.LinkedList([1,3,4])
    print(repr(my_list))
    print(my_list.backward_repr())
