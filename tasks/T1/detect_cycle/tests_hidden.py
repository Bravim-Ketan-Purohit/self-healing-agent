from solution import ListNode, has_cycle


def test_single_node_self_cycle():
    a = ListNode(1)
    a.next = a
    assert has_cycle(a) is True


def test_two_nodes_no_cycle():
    a = ListNode(1, ListNode(2))
    assert has_cycle(a) is False


def test_two_nodes_with_cycle():
    a = ListNode(1)
    b = ListNode(2)
    a.next = b
    b.next = a
    assert has_cycle(a) is True


def test_cycle_in_middle():
    nodes = [ListNode(i) for i in range(5)]
    for i in range(4):
        nodes[i].next = nodes[i + 1]
    nodes[4].next = nodes[2]  # cycle: 2->3->4->2
    assert has_cycle(nodes[0]) is True


def test_long_list_no_cycle():
    head = ListNode(0)
    current = head
    for i in range(1, 100):
        current.next = ListNode(i)
        current = current.next
    assert has_cycle(head) is False


def test_long_list_with_tail_cycle():
    nodes = [ListNode(i) for i in range(100)]
    for i in range(99):
        nodes[i].next = nodes[i + 1]
    nodes[99].next = nodes[50]
    assert has_cycle(nodes[0]) is True


def test_cycle_at_second_node():
    a = ListNode(1)
    b = ListNode(2)
    c = ListNode(3)
    a.next = b
    b.next = c
    c.next = b  # cycle: 2->3->2
    assert has_cycle(a) is True


def test_three_nodes_no_cycle():
    a = ListNode(1, ListNode(2, ListNode(3)))
    assert has_cycle(a) is False
