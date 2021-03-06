#
# Developed by 10Pines SRL
# License: 
# This work is licensed under the 
# Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. 
# To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ 
# or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, 
# California, 94041, USA.
#  

import unittest

class Stack:

    STACK_EMPTY_DESCRIPTION = 'Stack is empty'

    class EmptyElement:
        def __init__(self):
            pass

        def previous(self):
            raise Exception(Stack.STACK_EMPTY_DESCRIPTION)

        def object(self):
            raise Exception(Stack.STACK_EMPTY_DESCRIPTION)

    class Element:
        def __init__(self, anObject, previous):
            self._object = anObject
            self._previous = previous

        def previous(self):
            return self._previous

        def object(self):
            return self._object

    EMPTY = EmptyElement()

    def __init__(self):
        self._top = Stack.EMPTY
        self._size = 0

    def top(self):
        return self._top.object()

    def isEmpty(self):
        return self._top is Stack.EMPTY

    def push(self, anObject):
        self._top = Stack.Element(anObject, self._top)
        self._size += 1

    def pop(self):
        previousTopObject = self._top.object()
        self._top = self._top.previous()
        self._size -= 1
        return previousTopObject

    def size(self):
        return self._size
    
class StackTest(unittest.TestCase):
    
    def testStackShouldBeEmptyWhenCreated(self):
        stack = Stack()
        
        self.assertTrue(stack.isEmpty())

    def testPushAddElementsToTheStack(self):
        stack = Stack()
        stack.push('something')
        
        self.assertFalse(stack.isEmpty())

    def testPopRemovesElementsFromTheStack(self):
        stack = Stack()
        stack.push("Something")
        stack.pop()
        
        self.assertTrue(stack.isEmpty())
    
    def testPopReturnsLastPushedObject(self):
        stack = Stack()
        pushedObject = "Something"
        stack.push(pushedObject)
        self.assertEquals(pushedObject, stack.pop())
    
    def testStackBehavesLIFO(self):
        firstPushed = "First"
        secondPushed = "Second"
        stack = Stack()
        stack.push(firstPushed)
        stack.push(secondPushed)
        
        self.assertEquals(secondPushed,stack.pop())
        self.assertEquals(firstPushed,stack.pop())
        self.assertTrue(stack.isEmpty())
    
    def testTopReturnsLastPushedObject(self):
        stack = Stack()
        pushedObject = "Something"

        stack.push(pushedObject)

        self.assertEquals(pushedObject, stack.top())

    def testTopDoesNotRemoveObjectFromStack(self):
        stack = Stack()
        pushedObject = "Something"

        stack.push(pushedObject)

        self.assertEquals( 1,stack.size()) 
        stack.top()
        self.assertEquals( 1,stack.size())

    def testCanNotPopWhenThereAreNoObjectsInTheStack(self):
        stack = Stack()
        
        try:
            stack.pop()
            self.fail()
        except Exception as stackIsEmpty:
            self.assertEquals(Stack.STACK_EMPTY_DESCRIPTION,stackIsEmpty.message)
        
    def testCanNotTopWhenThereAreNoObjectsInTheStack(self):
        stack = Stack()

        try:
            stack.top()
            self.fail()
        except Exception as stackIsEmpty:
            self.assertEquals(Stack.STACK_EMPTY_DESCRIPTION,stackIsEmpty.message)
    
if __name__ == "__main__":
    unittest.main()
