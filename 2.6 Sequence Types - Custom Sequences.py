'''
Creating our own Sequence types

We will cover Abstract Base Classes later in this course, so we'll revisit this topic again

At it's most basic, an immutable sequence type should support two things:
returning the length of the sequence (technically, we don't even really need that!)
given an index, returning the element at that index

If an object provides this functionality, then we should in theory be able to:
retrieve elements by index using square brackets []
iterate through the elements using Python's native looping mechanisms
e.g. for loops, comprehensions
---------------------------------------------------------------------------------
Remember that sequence types are iterables, but not all iterables are sequence types

Sequence types, at a minimum, implement the following methods:

__len__ __getitem__

At its most basic, the __getitem__ method takes in a single integer argument – the index

However, it may also choose to handle a slicetype argument

So how does this help when iterating over the elements of a sequence?
---------------------------------------------------------------------------------
The __getitem__ method

The __getitem__ method should return an element of the sequence based on the specified index
or raise an IndexError exception if the index is out of bounds   (and may, but does not have 
to, support negative indices 
and slicing)

my_list = ['a', 'b', 'c', 'd', 'e', 'f']

Python's listobject implements the __getitem__ method:

my_list.__getitem__(0) → 'a'
my_list.__getitem__(1) → 'b'
my_list.__getitem__(-1) → 'f'
my_list.__getitem__(slice(None, None, -1)) 
→ ['f', 'e', 'd', 'c', 'b', 'a']


---------------------------------------------------------------------------------
The __getitem__ method
But if we specify an index that is out of bounds:
my_list.__getitem__(100) → IndexError
my_list.__getitem__(-100) → IndexError

All we really need from this __getitem__ method is the ability to
return an element for a valid index
raise an IndexError exception for an invalid index

Also remember, that sequence indices start at 0

i.e. we always know the index of the first element of the sequence
---------------------------------------------------------------------------------
Implementing a forloop
So now we know: sequence indexing starts at 0
__getitem__(i) will return the element at index i
__getitem__(i) will raise an IndexError exception when iis out of bounds

my_list = [0, 1, 2, 3, 4, 5]

for item in my_list:
print(item ** 2)

index = 0
while True:
try:
item = my_list.__getitem__(index)
except IndexError:
break
print(item ** 2)
index += 1

The point is that if the object implements __getitem__
we can iterate through it using a forloop, or even a comprehension
---------------------------------------------------------------------------------
The __len__ Method

In general sequence types support the Python built-in function len()

To support this all we need to do is implement the __len__ method in our custom sequence type

my_list = [0, 1, 2, 3, 4, 5]

len(my_list) → 6
my_list.__len__() → 6
---------------------------------------------------------------------------------
Writing our own Custom Sequence Type

to implement our own custom sequence type we should then implement:
__len__
__getitem__

At the very least __getitem__ should:
return an element for a valid index [0, length-1]
raise an IndexError exception if index is out of bounds

Additionally we can choose to support:
negative indices i < 0→i = length - i
slicing handle sliceobjects as argument to __getitem__

---------------------------------------------------------------------------------

'''

# we will focus on immutable sequence types
my_list = [1,2,3,4,5]
print(len(my_list)) #5
#same as 
print(my_list.__len__()) #5
my_list[2] #3
#same as 
my_list.__getitem__(2) #3
my_list[::-1] #[5, 4, 3, 2, 1]
my_list.__getitem__(slice(None,None,-1)) #[5, 4, 3, 2, 1]

for item in my_list:
    print(item**2)
    '''
    1
4
9
16
25
    '''
    
# we want to write the equivalent 
index = 0

while True:
    print(my_list.__getitem__(index))
    index+=1
# this returns IndexError: list index out of range 

#to handle that explicitly 
index = 0
while True:
    try:
        print(my_list.__getitem__(index))
    except IndexError:
        break
    index+=1
    # This ran without an exception
'''
1
2
3
4
5
'''
#implementing our own sequence types

class silly:
    
    def __init__(self,n):
        self.n = n
        
    def __len__(self):
        print('You asked for length')
        return self.n

    def __getitem__(self,value):
        print(f'you requested for value at position {value}')
        return 'This is a silly element'
    
Silly = silly(10)

len(Silly)
'''
You asked for length
Out[3]: 10
'''
    
Silly.__getitem__(30)
'''
you requested for value at position 30
Out[4]: 'This is a silly element
'''
#in order to handle -ve index values or index out of bound scenarios"

class silly:
    
    def __init__(self,n):
        self.n = n
        
    def __len__(self):
        print('You asked for length')
        return self.n

    def __getitem__(self,value):
        if value<0 or value > self.n:
            raise IndexError
        print(f'you requested for value at position {value}')
        return 'This is a silly element'
    
    
Silly = silly(10)
Silly.__getitem__(100)     #IndexError
Silly[200] #IndexError

for item in Silly:
    print(item)

'''
you requested for value at position 0
This is a silly element
you requested for value at position 1
This is a silly element
you requested for value at position 2
This is a silly element
you requested for value at position 3
This is a silly element
you requested for value at position 4
This is a silly element
you requested for value at position 5
This is a silly element
you requested for value at position 6
This is a silly element
you requested for value at position 7
This is a silly element
you requested for value at position 8
This is a silly element
you requested for value at position 9
This is a silly element
you requested for value at position 10
This is a silly element
'''
#we don;t need len of the sequence 

class silly:
    
    def __init__(self,n):
        self.n = n
        
    '''def __len__(self):
        print('You asked for length')
        return self.n'''

    def __getitem__(self,value):
        if value<0 or value > self.n:
            raise IndexError
        print(f'you requested for value at position {value}')
        return 'This is a silly element'
    
    
Silly = silly(10)
for item in Silly:
    print(item)
    '''
    you requested for value at position 0
This is a silly element
you requested for value at position 1
This is a silly element
you requested for value at position 2
This is a silly element
you requested for value at position 3
This is a silly element
you requested for value at position 4
This is a silly element
you requested for value at position 5
This is a silly element
you requested for value at position 6
This is a silly element
you requested for value at position 7
This is a silly element
you requested for value at position 8
This is a silly element
you requested for value at position 9
This is a silly element
you requested for value at position 10
This is a silly element
    '''
    
#why? cause python only cares about excpetion that we are providing at the get item method


class silly:
    
    def __init__(self,n):
        self.n = n
        
    def __len__(self):
        print('You asked for length')
        return self.n

    def __getitem__(self,value):
        #if value<0 or value > self.n:
         #   raise IndexError
        print(f'you requested for value at position {value}')
        return 'This is a silly element'
    
    
Silly = silly(10)
for item in Silly:
    print(item)
#this prints elements infinetely

Silly[0:5:2]
'''
you requested for value at position slice(0, 5, 2)
Out[13]: 'This is a silly element'
'''
Silly[3]
'''
Silly[3]
you requested for value at position 3
'''   
# we need to differentiate between these
from functools import lru_cache

@lru_cache(2**10)
def fib(n):
    if n<2:
        return 1
    else: 
        return fib(n-1)+ fib(n-2)
    
fib(5) #8
fib(100) #573147844013817084101
fib(100000) #RecursionError: maximum recursion depth exceeded

class fibb:
    
    def __init__(self,n):
        self.n = n
        
    def __len(self):
        return self.n
    
    def __getitem__(self,value):
        if isinstance(value, int):
            if value <0 or value>=self.n:
                raise IndexError
            return fibb._fib(value)
    @staticmethod
    @lru_cache(2**10)
    def _fib(n):
        if n<2:
            return 1
        else: 
            return fib(n-1)+ fib(n-2)
            
        
f = fibb(8)
f[3] #3
f[4] #5
list(f) # [1, 1, 2, 3, 5, 8, 13, 21]

#to do sequence

class fibb:
    
    def __init__(self,n):
        self.n = n
        
    def __len__(self):
        return self.n
    
    def __getitem__(self,value):
        if isinstance(value, int):
            if value <0 or value>=self.n:
                raise IndexError
            return fibb._fib(value)
        else:
            start,stop,step = value.indicies(self.n)
            rng= range(start,stop,step)
            return [fibb._fib(i) for i in rng]
            
    @staticmethod
    @lru_cache(2**10)
    def _fib(n):
        if n<2:
            return 1
        else: 
            return fibb._fib(n-1)+ fibb._fib(n-2)
    
f = fib(10)
    
list(f)
    
  
