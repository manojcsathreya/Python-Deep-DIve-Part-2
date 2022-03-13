'''
COPY SEQUENCES

----------------------------------------------------------------------------------------
Mutable sequences can be modified. 
Sometimes you want to make sure that whatever sequence you are working with cannot 
be modified, either inadvertently by yourself, or by 3rd party functions
We saw an example of this earlier with list concatenations and repetitions.

Also consider this example: <BAD EXAMPLE>
def reverse(s):
    s.reverse()
    return s    


s = [10, 20, 30]
new_list = reverse(s)  --> We should have passed it a copy of our list if we did not intend for our original list to be modified
new_list → [30, 20, 10]
s → [30, 20, 10]
----------------------------------------------------------------------------------------
Soapbox 
def reverse(s):
    s.reverse()
    return s
Generally we write functions that do not modify the contents of their arguments.
But sometimes we really want to do so, and that's perfectly fine →in-place methods
However, to clearly indicate to the caller that something is happening in-place, we should not
return the object we modified

If we don't return s in the above example, the caller will probably wonder why not?
So, in this case, the following would be a better approach:
def reverse(s):
    s.reverse()
and if we do not do in-place reversal, then we return the reversed sequence
def reverse(s):
    s2 = <copy of s>
    s2.reverse()
    return s2
----------------------------------------------------------------------------------------
How to copy a sequence
We can copy a sequence using a variety of methods:  s = [10, 20, 30]
Simple Loop     cp = []            #definitely non-Pythonic!
                for e in s:
                    cp.append(e)

List Comprehension cp = [e for e in s]

The copy method cp = s.copy() #(not implemented in immutable types, such as tuples or strings)

Slicing cp = s[0:len(s)] or, more simply cp = s[:]

The copy module

list() 
list_2 = list(list_1)
Note: tuple_2 = tuple(tuple_1) and t[:] does not create a new tuple!
----------------------------------------------------------------------------------------
Watch out when copying entire immutable sequences


l1 = [1, 2, 3]
l2 = list(l1)       l2 → [1, 2, 3]   id(l1) != id(l2)

t1 = (1, 2, 3)
t2 = tuple(t1)      t2 → (1, 2, 3) id(t1) = id(t2) same object!

t1 = (1, 2, 3)
t2 = t1[:]          t2 → (1, 2, 3) id(t1) = id(t2) same object!

Same thing with strings, also an immutable sequence type

Since the sequence is immutable, it is actually OK to return the same sequence
----------------------------------------------------------------------------------------
Shallow Copies
Using any of the techniques above, we have obtained a copy of the original sequence

s = [10, 20, 30]
cp = s.copy()
cp[0] = 100         cp → [100, 20, 30]      s → [10, 20, 30]

Great, so now our sequence swill always be safe from unintended modifications?  Not quite…

s = [ [10, 20], [30, 40] ]
cp = s.copy()
cp[0] = 'python' cp → ['python', [30, 40] ] s → [ [10, 20], [30, 40] ]

cp[1][0] = 100

cp → ['python', [100, 40] ] s → [ [10, 20], [100, 40] ]

What happened?
When we use any of the copy methods we saw a few slides ago, the copy essentially copies
all the object references from one sequence to another
s = [a, b] id(s) → 1000 id(s[0]) → 2000 id(s[1]) → 3000
cp = s.copy() id(cp) → 5000 id(cp[0]) → 2000 id(cp[1]) → 3000

When we made a copy of s, the sequence was copied, but it's elements point to the 
same memory address as the original sequence elements

The sequence was copied, but it's elements were not
This is called a shallow copy
----------------------------------------------------------------------------------------
DEEP COPY

So, if collections contain mutable elements, shallow copies are not sufficient to ensure the copy
can never be used to modify the original!
Instead, we have to do something called a deep copy.

For the previous example we might try this:

s = [ [0, 0], [0, 0] ]
cp = [e.copy() for e in s]

In this case:

cpis a copy of s
but also, every element of cpis a copy of the corresponding element in s

But what happens if the mutable elements of s themselves contain mutable elements?

s = [ [ [0, 1], [2, 3] ], [ [4, 5], [6, 7] ] ]

We would need to make copies at least 3 levels deep to ensure a true deep copy

Deep copies, in general, tend to need a recursive approach

Deep copies are not easy to do. You might even have to deal with circular references

a = [10, 20]
b = [a, 30]
a.append(b)


If you wrote your own deep copy algorithm, you would need to handle this circular reference!


In general, objects know how to make shallow copies of themselves
built-in objects like lists, sets, and dictionaries do - they have a copy() method

The standard library copymodule has generic copy and deep copy operations
The copyfunction will create a shallow copy
The deepcopy function will create a deep copy, handling nested objects, and circular 
references properly
Custom classes can implement the __copy__ and __deepcopy__ methods to allow you to 
override how shallow and deep copies are made for you custom objects
We'll revisit this advanced topic of overriding deep copies of custom 
classes in the OOP series of this course.

Suppose we have a custom class as follows:
def MyClass:
    def __init__(self, a):
        self.a = a

from copy import copy, deepcopy
x = [10, 20]
obj = MyClass(x) 
x is obj.a → True
cp_shallow = copy(obj) 
cp_shallow.a is obj.a → True
cp_deep = deepcopy(obj) 
cp_deep.a is obj.a → False

def MyClass:
    def __init__(self, a):
        self.a = a

x = MyClass(500)
y = MyClass(x)  y.a is x → True
lst = [x, y]

cp = deepcopy(lst)

cp[0] is x → False
cp[1] is y → False
cp[1].a is x → False

cp[1].a is cp[0] → True

this is not a circular reference
'''

#Shalow Copies
l1 = [1,2,3]
l1_copy = []

for e in l1:
    l1_copy.append(e)
    
print(l1_copy)
print(id(l1),id(l1_copy))

'''
[1, 2, 3]
1841573570688 1841573553600
'''

l1_copy = [e for e in l1]
print(l1_copy)
print(id(l1),id(l1_copy))
'''
[1, 2, 3]
1841573570688 1841578840960
'''

l1_copy = l1.copy()
print(l1_copy)
print(id(l1),id(l1_copy))
'''
[1, 2, 3]
1841573570688 1841573553536
'''

l1_copy = list(l1)
print(l1_copy)
print(id(l1),id(l1_copy))
'''
[1, 2, 3]
1841573570688 1841578811840
'''

l2 = list(l1)
print(l2)
print(id(l1),id(l2))
'''
[1, 2, 3]
1841573570688 1841574467392
'''

#This would not work for Tuples or strings. Why? Coz they are immutable already

t1 = (1,2,3)
t2 = tuple(t1)
print(id(t1),id(t2))
#1841578808768 1841578808768

s1 = 'python'
s2 = str(s1)
print(id(s1),id(s2))
#1841460687984 1841460687984

l2 = l1[:]
print(l2)
print(id(l1),id(l2))
#[1, 2, 3]
#1841573570688 1841575445120

t2 = t1[:]
print(t2)
print(id(t1),id(t2))
#(1, 2, 3)
#1841578808768 1841578808768


#another way of copying

import copy

l1 = [1,2,3,4]
l2 = copy.copy(l1)
print(l2)
print(id(l1),id(l2))
#[1, 2, 3, 4]
#1841573529088 1841578808960

#this also would not work with tuples

t1 = (1,2,3,4)
t2 = copy.copy(t1)
print(t2)
print(id(t1),id(t2))
'''
(1, 2, 3, 4)
1841574123456 1841574123456
'''
#DEEP COPIES
v1 = [0,0]
v2 = [0,0]

line = [v1,v2]
line2 = line.copy()

print(id(line),id(line2)) #1841573529856 1841573553600
print(id(line[0]),id(line2[0])) #1841574548352 1841574548352
#elements inside the list are pointng to the same objects

#we'll try with list comprehension
line2 = [v for v in line]
print(id(line),id(line2)) #1841573529856 1841573553536
print(id(line[0]),id(line2[0])) #1841574548352 1841574548352

print(line[0]) #[0, 0]
line[0][0] = 100
print(line,line2) #[[100, 0], [0, 0]] [[100, 0], [0, 0]]
#coz they are pointing to the same address

v1 = [1,1]
v2 = [2,2]
v3 = [3,3]
v4 = [4,4]

line1 = [v1,v2]
line2 = [v3,v4]

plane1 = [line1,line2]

plane2 = [e.copy() for e in plane1]

print(plane1)
print(plane2)
'''
[[[1, 1], [2, 2]], [[3, 3], [4, 4]]]
[[[1, 1], [2, 2]], [[3, 3], [4, 4]]]
'''
print(id(plane1[0]),id(plane2[0])) #1841573564800 1841573578176

print(id(plane1[0][0]),id(plane2[0][0])) #1841573594240 1841573594240
#but the nested elements inside the planes are same. why? cox we only copied one level of nesting
#this is the problem with copying when we are implementing on our own


#implementing deep copies
plane2 = copy.deepcopy(plane1)
print(plane1)
print(plane2)
'''
[[[1, 1], [2, 2]], [[3, 3], [4, 4]]]
[[[1, 1], [2, 2]], [[3, 3], [4, 4]]]
'''
print(plane1[0]) #[[1, 1], [2, 2]]
print(plane2[0]) #[[1, 1], [2, 2]]

print(plane1[0][0]) #[1, 1]
print(plane2[0][0]) #[1, 1]

print(id(plane1),id(plane2)) #1841573595520 1841575507456
print(id(plane1[0][0]),id(plane2[0][0])) #1841573594240 1841573578176
print(id(plane1[0][0][0]),id(plane2[0][0][0])) #140720888948528 140720888948528


class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def __repr__(self):
        return f'Point({self.x},{self.y})'
    
class Line:
    def __init__(self,p1,p2):
        self.p1 = p1
        self.p2 = p2

    def __repr__(self):
        return f'Line({self.p1.__repr__()},{self.p2.__repr__()}) '  

p1 = Point(0, 0)
p2 = Point(10, 10)

line1 = Line(p1,p2)
line2 = copy.deepcopy(line1)

print(line1) #Line(Point(0,0),Point(10,10)) 
print(line2) #Line(Point(0,0),Point(10,10)) 

print(id(line1.p1)) #1841574518112
print(id(line1.p2)) #1841574517584

print(id(line1.p1.x)) #140720888948496
print(id(line2.p1.x)) #140720888948496
