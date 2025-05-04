"""
stack.py
4/29/2025 Kobe Goodwin

Last-in First-out (LIFO) container.
"""

class Stack:
    def __init__(self):
        """
        Initializes an empty stack.
        
        Returns:
            Instance of Stack
        """
        self.stack = []

    def push(self, o):
        """
        Pushes an object to the top of the stack.

        Args:
            o: The object to push onto the stack.
            
        Returns:
            None
        """
        self.stack.append(o)

    def peek(self):
        """
        Returns the object at the top of the stack without removing it.

        Returns:
            The object at the top of the stack
            None if the stack is empty.
        """
        if self.stack:
            return self.stack[-1]
        return None

    def pop(self):
        """
        Removes and returns the object at the top of the stack.

        Returns:
            The object at the top of the stack
            None if the stack is empty.
        """
        if self.stack:
            return self.stack.pop()
        return 0.0

    def is_empty(self):
        """
        Checks if the stack is empty.

        Returns:
            bool: True if the stack is empty
                  False if the stack is not empty
        """
        return len(self.stack) == 0

    def size(self):
        """
        Returns the size of the stack.

        Returns:
            int: The number of items in the stack.
        """
        return len(self.stack)
    
    def __str__(self):
        """
        Returns the stack as a string
        
        Returns:
            str: The stack as a string
        """
        return str(self.stack)

    def __add__(self, other):
        """
        Creates a Stack where other is on bottom
        Ex. [0] + [1] = [1, 0]. 0 is on TOP.
        
        Args:
            other (Stack): stack to add with
        
        Returns:
            Stack: New stack with other on bottom
        """
        result = Stack()
        result.push(other)
        for i in self.stack:
            result.push(i)
        return result



