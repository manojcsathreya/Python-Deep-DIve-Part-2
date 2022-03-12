'''
Mutable sequence types
Mutating Objects

names = ['Eric', 'John']

names ---> Eric <@0xFF255>
           John
           
names = names + ['Michael']

names ---> Eric     <@0xAA2345>
           John
           Michael
           

This is NOT mutation!
           
Mutating an object means changing the object's state without creating a new object

names = ['Eric', 'John'] 
names.append('Michael')


names --->  Eric  <@0xFF255>
            John
            Michael
--------------------------------------------------------------------------------------
Mutating Using []

s[i] = x      element at index i is replaced with x
s[i:j] = s2   slice is replaced by the contents of the iterable s2
del s[i]      removes element at index i
del s[i:j]    removes entire slice

We can even assign to extended slices: s[i:j:k] = s2

We will come back to mutating using slicing in a lot more detail in an 
upcoming video
--------------------------------------------------------------------------------------
Some methods supported by mutable sequence types such as lists

s.append(x) appends x to the end of s

s.clear() removes all items from s

s.insert(i, x) inserts x at index i

s.pop(i) removes and returns element at index i

s.remove(x) removes the first occurrence of xin s

s.reverse() does an in-place reversal of elements of s

s.copy() returns a shallow copy

s.extend(iterable) appends contents of iterable to the end of s

and more...
'''


#Mutable Sequences
#When dealing with mutable sequences, we have a few more things we can do - essentially adding, removing and replacing elements in the sequence.

#This mutates the sequence. The sequence's memory address has not changed, but the internal state of the sequence has.

#Replacing Elements
#We can replace a single element as follows:

l = [1, 2, 3, 4, 5]
print(id(l)) #1979932141064
l[0] = 'a'
print(id(l), l) #1979932141064  ['a', 2, 3, 4, 5]

 
#We can remove all elements from the sequence:

l = [1, 2, 3, 4, 5]
l.clear()
print(l) #[]
#Note that this is NOT the same as doing this:
l = [1, 2, 3, 4, 5]
l = []
print(l) #[]


#The net effect may look the same, l is an empty list, but observe the memory addresses:

l = [1, 2, 3, 4, 5]
print(id(l)) #1979932698824
l.clear()
print(l, id(l)) #[] 1979932698824

#vs

l = [1, 2, 3, 4, 5]
print(id(l)) #1979932699144
l = []
print(l, id(l)) #[] 1979932698824
#In the second case you can see that the object referenced by l has changed, but not in the first case.

#Why might this be important?

#Suppose you have the following setup:

suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
alias = suits
suits = []
print(suits, alias)#[] ['Spades', 'Hearts', 'Diamonds', 'Clubs']

#But using clear:

suits = ['Spades', 'Hearts', 'Diamonds', 'Clubs']
alias = suits
suits.clear()
print(suits, alias) #[] []
#Big difference!!

#We can also replace elements using slicing and extended slicing. Here's an example, but we'll come back to this in a lot of detail:

l = [1, 2, 3, 4, 5]
print(id(l)) #1979932698504
l[0:2] = ['a', 'b', 'c', 'd', 'e']
print(id(l), l) #1979932698504 ['a', 'b', 'c', 'd', 'e', 3, 4, 5]
#Appending and Extending
#We can also append elements to the sequence (note that this is not the same as concatenation):

l = [1, 2, 3]
print(id(l)) #1979932697992
l.append(4)
print(l, id(l)) #[1, 2, 3, 4] 1979932697992
#If we had "appended" the value 4 using concatenation WE USE EXTEND

l = [1, 2, 3]
print(id(l)) #1979932193288
l = l + [4]
print(id(l), l) #1979932698312 [1, 2, 3, 4]
#If we want to add more than one element at a time, we can extend a sequence with the contents of any iterable (not just sequences):

l = [1, 2, 3, 4, 5]
print(id(l)) #1979932844488
l.extend({'a', 'b', 'c'})
print(id(l), l) #1979932844488 [1, 2, 3, 4, 5, 'c', 'b', 'a']
#Of course, since we extended using a set, there was not gurantee of positional ordering.

#If we extend with another sequence, then positional ordering is retained:

l = [1, 2, 3]
l.extend(('a', 'b', 'c'))
print(l) #[1, 2, 3, 'a', 'b', 'c']
#Removing Elements
#We can remove (and retrieve at the same time) an element from a mutable sequence:

l = [1, 2, 3, 4]
print(id(l)) #1979932193288
popped = l.pop(1)
print(id(l), popped, l) #1979932193288 2 [1, 3, 4]
#If we do not specify an index for pop, then the last element is popped:

l = [1, 2, 3, 4]
popped = l.pop()
print(popped) #4
print(id(l), popped, l) #1979932696968 4 [1, 2, 3]
#Inserting Elements
#We can insert an element at a specific index. What this means is that the element we are inserting will eb at that index position, and element that was at that position and all the remaining elements to the right are pushed out:

l = [1, 2, 3, 4]
print(id(l)) #1979932143176
l.insert(1, 'a')
print(id(l), l) #1979932143176 [1, 'a', 2, 3, 4]


#Reversing a Sequence
#We can also do in-place reversal:

l = [1, 2, 3, 4]
print(id(l)) #1979930587080
l.reverse()
print(id(l), l) #1979930587080 [4, 3, 2, 1]
#We can also reverse a sequence using extended slicing (we'll come back to this later):

l = [1, 2, 3, 4]
l[::-1] #[4, 3, 2, 1]
#But this is NOT mutating the sequence - the slice is returning a new sequence - that happens to be reversed.

l = [1, 2, 3, 4]
print(id(l)) #1979932143176
l = l[::-1]
print(id(l), l) #1979932696968 [4, 3, 2, 1]


#Copying Sequences
#We can create a copy of a sequence:

l = [1, 2, 3, 4]
print(id(l)) #1979932700040
l2 = l.copy()
print(id(l2), l2) #1979932696968 [1, 2, 3, 4]
#Note that the id of l and l2 is not the same.

#In this case, using slicing does work the same as using the copy method:

l = [1, 2, 3, 4]
print(id(l)) #1979932847304
l2 = l[:]
print(id(l2), l2) #1979932700040 [1, 2, 3, 4]
#As you can see in both cases we end up with new objects.

#So, use copy() or [:] - up to you, they end up doing the same thing.

#We'll come back to copying in some detail in an upcoming video as this is an important topic with some subtleties.
