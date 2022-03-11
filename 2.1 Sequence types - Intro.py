'''
------------------------------------------------------------------------------------
What is a sequence?

In Math: S = x1, x2, x3, x4, …                 (countable sequence)

Note the sequence of indices: 1, 2, 3, 4, …

We can refer to any item in the sequence by using it's index number x2 or S[2]

So we have a concept of the first element, the second element, and so on… →positional ordering

Python lists have a concept of positional order, but sets do not 
A list is a sequence type
A set is not

In Python, we start index numbers at 0, not 1 (we'll see why later)

S = x0, x1, x2, x3, …
→ S[2]is the third element
------------------------------------------------------------------------------------
Built-In Sequence Types

mutable    -------------- lists and bytearrays
immutable  -------------- strings, 
                          tuples (in reality a tuple is more than just a sequence type),
                          range(more limited than lists, strings and tuples) 
                          and bytes

Additional Standard Types:  collections package  --> namedtuple and deque
                            arraymodule          --> array
                            
------------------------------------------------------------------------------------
Homogeneous vs Heterogeneous Sequences

Strings are homogeneous sequences
    each element is of the same type (a character)   #'python'

Lists are heterogeneous sequences
    each element may be a different type [1, 10.5, 'python']

Homogeneous sequence types are usually more efficient (storage wise at least)

e.g. prefer using a string of characters, rather than a list or tuple of characters

------------------------------------------------------------------------------------
Iterable Type vs Sequence Type

What does it mean for an object to be iterable?
it is a container type of object and we can list out the elements in that object one by one


So any sequence type is iterable
 l = [1, 2, 3]  l[0]
                for e in l

But an iterable is not necessarily a sequence type

s = {1, 2, 3}  for e in s <this works>    →iterables are more general
               s[0] <This does not work>


------------------------------------------------------------------------------------
Standard Sequence Methods

Built-in sequence types, both mutable and immutable, support the following methods
x in s
s1 + s2 concatenation
s * n (or n * s)  (n an integer) repetition
x not in s

len(s) 

min(s)  (if an ordering between elements of s is defined)
max(s)
This is not the same as the ordering (position) of elements 
inside the container, this is the ability to compare pairwise 
elements using an order comparison (e.g. <, <=, etc.)



s.index(x) index of first occurrence of xin s
s.index(x, i)  index of first occurrence of xin sat or after index i
s.index(x, i, j)  index of first occurrence of xin sat or after index i and before index j

------------------------------------------------------------------------------------
Standard Sequence Methods

s[i]      the element at index i

s[i:j]      the slice from index i, to (but not including) j

s[i:j:k]      extended slice from index i, to (but not including) j, in steps of k


Note that slices will return in the same container type

rangeobjects are more restrictive:
    no concatenation / repetition
    min, max, in, not in not as efficient

We will come back to slicing in a lot more detail in an upcoming video
------------------------------------------------------------------------------------
Review: Beware of Concatenations

x = [1, 2]     a = x + x      a → [1, 2, 1, 2]

x = 'python'   a = x + x      a → 'pythonpython'

x = [ [0, 0] ] a = x + x      a → [ [0, 0], [0, 0] ]

id(x[0]) == id(a[0]) == id(a[1])

a[0][0] = 100 a → [ [100, 0], [100, 0] ]

a[0] is x[0]
a[1] is x[0]


Review: Beware of Repetitions

a = [1, 2] * 2         a → [1, 2, 1, 2]

a = [ [0, 0] ] * 2     a → [ [0, 0], [0, 0] ]

id == id(a[0]) == id(a[1])

a[0][0] = 100 a → [ [100, 0], [100, 0] ]

a = 'python' * 2 a → 'pythonpython'

a = ['python'] * 2 a → ['python', 'python']
'''
l = [1,2,3]
t = (1,2,3)
s = 'python'

l[0]#1
t[1]#2
s[3] #'h'

for c in s:
    print(c)

'''
p
y
t
h
o
n
'''

s = {10,20,30}
for e in s:
    print(e)
    
'''

10
20
30
'''

#however the order is not guranteed

s = {'x',10, 'a','A'}
for e in s:
    print(e)
'''
A
10
a
x
'''

#this is the difference between iterables and sequence types. Sets are iterables and not sequence types
s[0]#TypeError: 'set' object is not subscriptable

#certain sequence types are mutables
l = [1,2,3]
t = (1,2,3)

#we can access elements via indexing
l[0]
t[1]

#but we cannot set values to tuples
#However, tuples itself are not imutables. We can have list inside the tuples that can be mutable

t = ([1,2],3,4)
t[2] =2 #TypeError: 'tuple' object does not support item assignment

t[0][0] =100
t #([100, 2], 3, 4)

'a' in ['a','b','c'] #True

100 in range(200) #True

len('python'), len([1, 2, 3]), len({10, 20, 30}), len({'a': 1, 'b': 2}) #(6, 3, 3, 2)

#less than or greater than user compariosion operators. But for some data types comparision operators are not supported
type(2+2j) #complex

2+2j<100+100j #'<' not supported between instances of 'complex' and 'complex'

a = [100, 300, 200]
min(a), max(a) #(100, 300)

#to have min and max functions on certailn data types, we need to have pairwise comparision operator
#also we cannot compare heterogeneous data types

l = [1,'a',3,'A']
max(l) # '>' not supported between instances of 'str' and 'int'

#concatination: takes two or more elements of same type and combines them together
[1,2,3]+[4,5,6] #[1, 2, 3, 4, 5, 6]
#also we cannot add two different sequence/iterable types
(1,2,3)+[4,5,6] #TypeError: can only concatenate tuple (not "list") to tuple

'abc'+['d','e','f'] 
#TypeError: can only concatenate str (not "list") to str

#we can use different methods

list('abc')+['d','e','f'] #['a', 'b', 'c', 'd', 'e', 'f']

#we can also use join method
'***'.join([1,2,3]) #TypeError: sequence item 0: expected str instance, int found
#why is this giving error? well because we are adding string to an int. which are incompatible
#so we have to convert int to string and then try
'***'.join(['1','2','3']) #'1***2***3'
#good thing about join is, it does not add extra sequence at the end. so this can be useful in seperating values into csv

','.join(['a','b','c']) #'a,b,c'

#we can also multiply the sequence 
a=[1,2,3]
a*3 #[1, 2, 3, 1, 2, 3, 1, 2, 3]

'abc'*3 #'abcabcabc'

s = "gnu's not unix"
enumerate(s) #<enumerate at 0x1acc66e5b00>
list(enumerate(s))
'''
[(0, 'g'),
 (1, 'n'),
 (2, 'u'),
 (3, "'"),
 (4, 's'),
 (5, ' '),
 (6, 'n'),
 (7, 'o'),
 (8, 't'),
 (9, ' '),
 (10, 'u'),
 (11, 'n'),
 (12, 'i'),
 (13, 'x')]
'''
s.index('n') #returns index of first find
s.index('n',2) # second argument specifies to look for n after 2nd index and the next index is 6
s.index('n',1)#1 it finds n at forst index so it returns 1
s.index('n',s.index('n')+1)#6
s.index('z') #returns exception ValueError: substring not found as there is no value
s.index('n',12) #this also returns exception as there is no n after 12th index

#Slicing
#We'll come back to slicing in a later lecture, but sequence types generally support slicing, even ranges (as of Python 3.2). Just like concatenation, slices will return the same type as the sequence being sliced:

s = 'python'
l = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
s[0:3], s[4:6] #('pyt', 'on')
l[0:3], l[4:6] #([1, 2, 3], [5, 6])


#It's ok to extend ranges past the bounds of the sequence:
s[4:1000]#'on'


#If your first argument in the slice is 0, you can even omit it. Omitting the second argument means it will include all the remaining elements:
s[0:3], s[:3] #('pyt', 'pyt')
s[3:1000], s[3:], s[:] #('hon', 'hon', 'python')

#

#We can even have extended slicing, which provides a start, stop and a step:
s, s[0:5], s[0:5:2] #('python', 'pytho', 'pto')
s, s[::2] #('python', 'pto')

#Technically we can also use negative values in slices, including extended slices (more on that later):
s, s[-3:-1], s[::-1] #('python', 'ho', 'nohtyp')
r = range(11)  # numbers from 0 to 10 (inclusive)
print(r) #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(list(r)) #[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
range(0, 11)

print(r[:5]) #[0, 1, 2, 3, 4]
range(0, 5)
print(list(r[:5])) #[0, 1, 2, 3, 4]
#As you can see, slicing a range returns a range object as well, as expected.

#Caveats with Concatenation and Repetition
#Consider this:

x = [2000]
id(x[0]) #2177520743920
l = x + x
l #[2000, 2000]
id(l[0]), id(l[1]) #(2177520743920, 2177520743920)
#As expected, the objects in l[0] and l[1] are the same.

#Could also use:

l[0] is l[1] #True
#This is not a big deal if the objects being concatenated are immutable. But if they are mutable:

x = [ [0, 0] ]
l = x + x
l #[[0, 0], [0, 0]]
l[0] is l[1] #True
#And then we have the following:

l[0][0] = 100
l[0] #[100, 0]
l #[[100, 0], [100, 0]]
#Notice how changing the 1st item of the 1st element also changed the 1st item of the second element.

#While this seems fairly obvious when concatenating using the + operator as we have just done, the same actually happens with repetition and may not seem so obvious:

x = [ [0, 0] ]
m = x * 3
m #[[0, 0], [0, 0], [0, 0]]
m[0][0] = 100
m #[[100, 0], [100, 0], [100, 0]]
#And in fact, even x changed:

x #[[100, 0]]
#If you really want these repeated objects to be different objects, you'll have to copy them somehow. A simple list comprehensions would work well here:

x = [ [0, 0] ]
m = [e.copy() for e in x*3]
m #[[0, 0], [0, 0], [0, 0]]
m[0][0] = 100
m #[[100, 0], [0, 0], [0, 0]]
x #[[0, 0]]
