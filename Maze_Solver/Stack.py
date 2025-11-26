from typing import TypeVar
T = TypeVar("T")  # use T as a type

class EmptyError(Exception):
    ''' class extending Exception to better document stack errors '''
    def __init__(self, message: str):
        self.message = message

class Stack:
    ''' class to implement a stack ADT using a Python list '''

    __slots__ = ("_data")  # a Python list

    def __init__(self):
        self._data = []

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
        if len(self._data) > 0 and type(self._data[0]) != type(item):
            raise TypeError("Types do not match")  
        self._data.append(item)

    def pop(self) -> T:
        ''' removes the topmost element from the stack and returns that element
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.pop(): stack is empty')
        return self._data.pop()  # calling Python list pop()

    def top(self) -> T:
        ''' returns the topmost element from the stack without modifying the stack
        Returns:
            the topmost item, of arbitrary type
        Raises:
            EmptyError exception if the stack is empty
        '''
        if len(self._data) == 0:
            raise EmptyError('Error in ArrayStack.top(): stack is empty')
        return self._data[-1]

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
        result = "--- top ---\n"
        if len(self._data) > 0:
            max_len    = max(len(str(datum)) for datum in self._data)
            half_width = max(0, (len(result) - max_len) // 2)
            # "\n".join creates a new string, deliminted by "\n" characters, where
            # the elements between each "\n" in the string are drawn from the
            # reverse of the data list so as to print the stack from top to bottom
            result += "\n".join(f"{datum:>{max_len + half_width}}" for datum in self._data[::-1])
            result += "\n--- bot ---"
        else:
            result += "--- bot ---"
            
        return result

    
def main() -> None:
    s = Stack()
    print("-----push-----")
    s.push(3)
    s.push(4)
    s.push(5)
    s.push(12)
   # s.push("bonney")
    print(s)
    print("------is_empty------")
    print(s.is_empty())
    print("-------top---------")
    print(s.top())
    print("------pop------")
    s.pop()
    print(s)
    s.pop()
    print(s)
    s.pop()
    print(s)
    s.pop()
    print(s)
   # s.pop()
   # print(s)
    print("------is_empty------")
    print(s.is_empty())
    

if __name__ == "__main__":
    main()
