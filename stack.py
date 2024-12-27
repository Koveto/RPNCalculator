"""
stack.py
12/26/2024
Last-in First-out container
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
        self.stack = self.stack[:len(stack)-1]
        return o