from collections import deque
from Queue import PriorityQueue

class PeekQueue:
    def __init__(self):
        self._dp = deque()

    def isEmpty(self):
        return self.size() == 0

    def size(self):
        return len(self._dp)

    def add(self, item):
        self._dp.append(item)

    def remove(self):
        return self._dp.popleft()

    def peek(self):
        return self._dp[0]
