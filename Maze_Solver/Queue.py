from typing import TypeVar
T = TypeVar("T")  # use T as a type
from LinkedList import LinkedList

class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

class Queue:
    ''' class to implement a stack ADT using a Python list '''

    __slots__ = ("_data")  # a Python list

    def __init__(self):
        self._data = LinkedList()

    def __len__(self) -> int:
        ''' allows the len function to be called using an ArrayStack object, e.g.,
               stack = ArrayStack()
               print(len(stack))
        Returns:
            number of elements in the stack, as an integer
        '''
        return len(self._data)

    def push(self, item: T) -> None: 
        ''' pushes a given item of arbitrary type onto the stack
        Parameters:
            item: an item of arbitrary type
        Returns:
            None
        '''

        self._data.add_right(item)

    def pop(self) -> T:
        ''' removes the topmost element from the stack and returns that element
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.pop(): stack is empty')
        return self._data.remove_left()  

    def top(self) -> T:
        ''' returns the topmost element from the stack without modifying the stack
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.top(): stack is empty')
        return self._data.front()
    def is_empty(self) -> bool:
        ''' indicates whether the stack is empty
        Returns:
            True if the stack is empty, False otherwise
        '''
       
        if len(self._data) == 0:
            return True
        else:
            return False
    


    def __str__(self) -> str:
        ''' creates a string representation of the data in the stack, using
            the maximum str length of any one datum as a centering guide 
        Returns:
            string representation of the stack
        '''

        current_value = self._data._head  # Start from the head of the linked list
        result = "--- top ---\n"
        while current_value is not None:
            result += f"{str(current_value.data)}\n"
            current_value = current_value.next  # Move to the next node
        result += "--- bot ---"
    
        return result

    
def main() -> None:
    s = Queue()
    s.push(3)
    s.push(4)
    s.push(5)
    s.top()
    print(s)
    s.pop()
    print(s)
    s.pop()
    s.pop()
    print(s.is_empty())

    b = Queue()
    b.push(-19)
    b.push(0)
    b.push(9.8)
    b.push(-11)
    print(b.top())
    b.pop()
    b.pop()
    b.pop()
    b.pop()
    print(b)

if __name__ == "__main__":
    main()
