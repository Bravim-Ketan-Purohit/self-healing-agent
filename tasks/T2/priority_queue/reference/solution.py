import heapq


class PriorityQueue:
    """Min-heap priority queue with push, pop, peek, and update_priority."""

    def __init__(self):
        self._heap = []  # list of [priority, counter, item]
        self._entry_finder = {}  # item -> entry
        self._counter = 0
        self._size = 0
        self._REMOVED = "<REMOVED>"

    def push(self, item: str, priority: int) -> None:
        if item in self._entry_finder:
            self._remove(item)
        entry = [priority, self._counter, item]
        self._counter += 1
        self._entry_finder[item] = entry
        heapq.heappush(self._heap, entry)
        self._size += 1

    def pop(self) -> str:
        if self._size == 0:
            raise IndexError("pop from empty priority queue")
        while self._heap:
            priority, count, item = heapq.heappop(self._heap)
            if item != self._REMOVED:
                del self._entry_finder[item]
                self._size -= 1
                return item
        raise IndexError("pop from empty priority queue")

    def peek(self) -> str:
        if self._size == 0:
            raise IndexError("peek from empty priority queue")
        while self._heap:
            priority, count, item = self._heap[0]
            if item != self._REMOVED:
                return item
            heapq.heappop(self._heap)
        raise IndexError("peek from empty priority queue")

    def update_priority(self, item: str, new_priority: int) -> None:
        if item not in self._entry_finder:
            raise KeyError(f"Item '{item}' not found in priority queue")
        self._remove(item)
        entry = [new_priority, self._counter, item]
        self._counter += 1
        self._entry_finder[item] = entry
        heapq.heappush(self._heap, entry)
        self._size += 1

    def _remove(self, item: str) -> None:
        entry = self._entry_finder.pop(item)
        entry[2] = self._REMOVED
        self._size -= 1

    def __len__(self) -> int:
        return self._size

    def __contains__(self, item: str) -> bool:
        return item in self._entry_finder
