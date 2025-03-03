"""
stack.py
2/13/2025 Kobe Goodwin

Last-in First-out (LIFO) container.
"""

class Stack:
    def __init__(self):
        """
        Initializes an empty stack.
        """
        self.stack = []

    def push(self, o):
        """
        Pushes an object to the top of the stack.

        Args:
            o (object): The object to push onto the stack.
        """
        self.stack.append(o)

    def peek(self):
        """
        Returns the object at the top of the stack without removing it.

        Returns:
            object: The object at the top of the stack, or None if the stack is empty.
        """
        if self.stack:
            return self.stack[-1]
        return None

    def pop(self):
        """
        Removes and returns the object at the top of the stack.

        Returns:
            object: The object at the top of the stack, or None if the stack is empty.
        """
        if self.stack:
            return self.stack.pop()
        return None

    def is_empty(self):
        """
        Checks if the stack is empty.

        Returns:
            bool: True if the stack is empty, False otherwise.
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

