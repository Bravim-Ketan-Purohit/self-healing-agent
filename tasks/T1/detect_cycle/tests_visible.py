from solution import ListNode, has_cycle


def test_no_cycle():
    head = ListNode(1, ListNode(2, ListNode(3)))
    assert has_cycle(head) is False


def test_cycle_at_start():
    a = ListNode(1)
    b = ListNode(2)
    c = ListNode(3)
    a.next = b
    b.next = c
    c.next = a
    assert has_cycle(a) is True


def test_empty_list():
    assert has_cycle(None) is False


def test_single_node_no_cycle():
    assert has_cycle(ListNode(1)) is False
