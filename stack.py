"""
stack.py
2/11/2025
Last-in First-out container

init()
Creates an empty Stack

push(o)
o: generalized object to push to the top
Pushes o to the top of the stack

peek()
Returns the object at the top of the stack

pop()
Removes and returns the object at the top of the stack

isEmpty()
Returns True if empty, False if not
"""

class Stack:
    def __init__(self):
        self.stack = []
    
    def push(self, o):
        self.stack = self.stack + [o]
        
    def peek(self):
        if (len(self.stack) != 0):
            return self.stack[-1]
        return None
    
    def pop(self):
        if (len(self.stack) == 0):
            return None
        o = self.stack[-1]
        self.stack = self.stack[:len(self.stack)-1]
        return o
    
    def isEmpty(self):
        return len(self.stack) == 0
