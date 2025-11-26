from __future__ import annotations

import heapq
import random
import string
import copy


class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

#################
class Entry[K,V]:
    __slots__ = ('key', 'value')

    def __init__(self, priority: K, data: V) -> None:
        self.key  : K = priority
        self.value: V = data

    def __str__(self) -> str:
        return f"({self.key},{self.value})"

    def __eq__(self, other: Entry[K,V]) -> bool:
        return self.key == other.key and self.value == other.value

    def __lt__(self, other: Entry[K,V]) -> bool:
        return self.key < other.key

    # not the Pythonic way to use __repr__ but allows us to print list of Entry
    def __repr__(self) -> str: 
        return f"({repr(self.key)},{'∅' if self.value is None else repr(self.value)})"

#######################
class PriorityQueue[E]:
    __slots__ = ('_container')

    def __init__(self):
        self._container: list[Entry] = list()

    def __len__(self)  -> int:   return len(self._container)
    def is_empty(self) -> bool:  return len(self._container) == 0

    def insert(self, key: K, item: V) -> None: 
        '''
        inserts a value into the priority queue
        Parameters:
            key: the key value of the inserted value, dictating the priority
            item: the value of the item being inserted
        Returns:
            None
        '''
        heapq.heappush(self._container, Entry(key, item))

    def remove_min(self) -> Entry:
        '''
        Removeses the minimum value in the priority queue
        Returns:
            remove_min: returns the minimum value
        '''
        if len(self._container) == 0:
            raise EmptyError("Queue is Empty")
        remove_min = heapq.heappop(self._container)
        return remove_min

    def min(self) -> Entry:
        '''
        Returns the minimum value without removing the value from the queue
        Returns:
            min: the minimum value
        '''
        if len(self._container) == 0:
            raise EmptyError("Queue is Empty")
        copy_self = copy.deepcopy(self)
        min = heapq.nsmallest(1, copy_self._container)[0]
        return min

    def __str__(self) -> str:
        return str(self._container)

#########################
#if __name__ == "__main__":
    # pq = PriorityQueue()
    # print(f"len of pq = {len(pq)}")
    # print(pq.insert(0, 5))
    # print(pq.insert(1,4))
    # print(pq.insert(5, 9))
    # print(pq.insert(2, 8))
    # print(pq.insert(7, 4))
    # print(pq.insert(9, 1))
    # print(pq.insert(3, 2))
    # print(pq.insert(1,4))
    # print(pq.insert(5, 9))
    # print(f"len of pq = {len(pq)}")
    # print(pq.min())
    # print(pq.min())
    # print(pq.min())
    # print(pq.min())
    # print(pq.min())
    # print(pq.remove_min())
    # print(pq.remove_min())
    # print(pq.remove_min())
    # print(pq.remove_min())
    # print(pq.remove_min())
    # print(pq.remove_min())
    # print(pq.remove_min())
    # print(pq.remove_min())
    # print(pq)


def main() -> None:
    s = PriorityQueue()
    print(f"len of pq = {len(s)}")
    # more tests below

    # s.insert("A", 3)
    # s.insert("B", 4)
    # s.insert("C", 5)
    # s.insert("D", 5)

    # s.min()

    # s.remove_min()

    # s.insert("E",75)

    # s.insert("F", 436)
    # s.insert("G", 225)

    # print(s)

    # s.remove_min()

    # s.min()

    # s.remove_min()
    # s.remove_min()
    # s.remove_min()

    # print(s)

    pq = PriorityQueue()
    print(f"len of pq = {len(pq)}")
    print("-------insert------")
    print(pq.insert(0, 5))
    print(pq.insert(1,4))
    print(pq.insert(5, 9))
    print(pq.insert(3, 2))
    print(pq.insert(1,4))
    print(pq.insert(5, 9))
    print(f"len of pq = {len(pq)}")
    print("-------min------")
    print(pq.min())
    print(pq.min())
    print(pq.min())
    print(pq.min())
    print(pq.min())
    print("-------remove_min-----")
    print(pq.remove_min())
    print(pq.remove_min())
    print(pq.remove_min())
    print(pq.remove_min())
    print(pq.remove_min())
    print(pq)

    print("-------------------------")
    print("-------Slide 11 Test-----")
    print("-------------------------")

    q = PriorityQueue()
    q.insert(4, "C")
    q.insert(5, "A")
    q.insert(6, "Z")
    q.insert(15, "K")
    q.insert(9, "F")
    q.insert(7, "Q")
    q.insert(20, "B")
    q.insert(16, "X")
    q.insert(25, "J")
    q.insert(14, "E")
    q.insert(12, "H")
    q.insert(11, "S")
    q.insert(13, "W")

    print(q)
    print()
    q.insert(2, "T")
    print(q)



    print("-----------------------")
    print("-----Slide 18 Test-----")
    print("-----------------------")
    q = PriorityQueue()
    q.insert(4, "C")
    q.insert(5, "A")
    q.insert(6, "Z")
    q.insert(15, "K")
    q.insert(9, "F")
    q.insert(7, "Q")
    q.insert(20, "B")
    q.insert(16, "X")
    q.insert(25, "J")
    q.insert(14, "E")
    q.insert(12, "H")
    q.insert(11, "S")
    q.insert(13, "W")

    print(q)
    q.remove_min()

    print(q)

main()