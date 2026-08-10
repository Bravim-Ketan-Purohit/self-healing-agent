from solution import MedianCollection


def test_basic_median():
    mc = MedianCollection()
    mc.add(3)
    mc.add(1)
    mc.add(2)
    assert mc.median() == 2


def test_even_count_median():
    mc = MedianCollection()
    mc.add(1)
    mc.add(2)
    mc.add(3)
    mc.add(4)
    assert mc.median() == 2.5


def test_remove():
    mc = MedianCollection()
    mc.add(1)
    mc.add(2)
    mc.add(3)
    mc.remove(1)
    assert mc.median() == 2.5


def test_size():
    mc = MedianCollection()
    assert mc.size() == 0
    mc.add(5)
    mc.add(5)
    assert mc.size() == 2
