'''
ITERATOS AND ITERABLES

Iterators
We saw than an iterator is an object that implements
__iter__ →returns the object itself
__next__ →returns the next element



The drawback is that iterators get exhausted →become useless for iterating again
                                             →become throw away objects

But two distinct things going on:
maintaining the collection of items (the container) (e.g. creating, mutating (if mutable), etc)
iterating over the collection

Why should we have to re-create the collection of items just to 
iterate over them?
-------------------------------------------------------------------------------------------------
Separating the Collection from the Iterator
Instead, we would prefer to separate these two
Maintaining the data of the collection should be one object
Iterating over the data should be a separate object →iterator
That object is throw-away →but we don't throw away the collection

The collection is iterable
but the iterator is responsible for iterating over the collection

The iterable is created once
The iterator is created every time we need to start a fresh iteration
-------------------------------------------------------------------------------------------------
Example

class Cities:
    def __init__(self):
        self._cities = ['Paris', 'Berlin', 'Rome', 'London']
        self._index = 0
    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._cities):
            raise StopIteration
        else:
            item = self._cities[self._index]
            self._index += 1
            return item

Citiesinstances are iterators
Every time we want to run a new loop, we have to create a new  instance of Cities
This is wasteful, because we should not have to re-create the _cities list every time
-------------------------------------------------------------------------------------------------
Example So, let's separate the object that maintains the cities, from the iterator itself
class Cities:
    def __init__(self):
        self._cities = ['New York', 'New Delhi', 'Newcastle']
    def __len__(self):
        return len(self._cities)

class CityIterator:
    def __init__(self, cities):
        self._cities = cities
        self._index = 0
    def __iter__(self):
        return self
    def __next__(self):
        if self._index >= len(self._cities):
            raise StopIteration
            else:
                etc…
-------------------------------------------------------------------------------------------------
Example
To use the Citiesand CityIterator together here's how we would proceed:

cities = Cities() create an instance of the container object

city_iterator = CityIterator(cities) -create a new iterator – but see how we pass in the 
                                      existing citiesinstance

for city in cities_iterator:
print(city) can now use the iterator to iterate

At this point, the cities_iterator is exhausted
If we want to re-iterate over the collection, we need to create a new one

city_iterator = CityIterator(cities)

for city in cities_iterator:
    print(city)
But this time, we did not have to re-create the collection – we just 
passed in the existing one!
-------------------------------------------------------------------------------------------------
So far…
At this point we have:
a container that maintains the collection items
a separate object, the iterator, used to iterate over the collection
So we can iterate over the collection as many times as we want
we just have to remember to create a new iterator every time

It would be nice if we did not have to do that manually every time
and if we could just iterate over the Citiesobject instead of CityIterator

This is where the formal definition of a Python iterable comes in…
-------------------------------------------------------------------------------------------------
Iterables

An iterable is a Python object that implements the iterable protocol
The iterable protocol requires that the object implement a single method

__iter__ returns a new instance of the iterator object
            used to iterate over the iterable

class Cities:
    def __init__(self):
        self._cities = ['New York', 'New Delhi', 'Newcastle']
    def __len__(self):
        return len(self._cities)

    def __iter__(self):
        return CityIterator(self)
    
-------------------------------------------------------------------------------------------------
Iterable vs Iterator

An iterable is an object that implements
__iter__ →returns an iterator                 (in general, a new instance)

An iterator is an object that implements
__iter__ →returns itself (an iterator)        (not a new instance)

__next__ →returns the next element

So iterators are themselves iterables
but they are iterables that become exhausted

Iterables on the other hand never become exhausted
because they always return a new iterator that is then used to iterate
-------------------------------------------------------------------------------------------------    
Iterating over an iterable

Python has a built-in function iter()
It calls the __iter__ method (we'll actually come back to this for sequences!)
The first thing Python does when we try to iterate over an object
it calls iter() to obtain an iterator
then it starts iterating (using next, StopIteration, etc)
using the iterator returned by iter()
'''

# =============================================================================
# Iterators and Iterables
# Previously we saw that we could create iterator objects by simply implementing:
# 
# a __next__ method that returns the next element in the container
# an __iter__ method that just returns the object itself (the iterator object)
# Doing that we could use a for loop, list comprehensions, and in fact use that iterator object anywhere an iterable was expected (like enumerate, sorted, and so on).
# 
# However, we had two outstanding issues/questions:
# 
# when we looped over the iterator using a for loop (or a comprehension, or other functions that do some form of iteration), we saw that the __iter__ was always called first.
# the iterator gets exhausted after we have finished iterating it fully - which means we have to create a new iterator every time we want to use a new iteration over the collection - can we somehow avoid having to remember to do that every time?
# The answer to both of these questions are related.
# 
# Let's start by looking at how we might avoid having to create a new instance of the collection every time we want to iterate over it.
# 
# After all, we don't need a new instance of the elements, just some kind of resetting of current item.
# 
# Let's start with a simple example that has those issues:
# =============================================================================

class Cities:
    def __init__(self):
        self._cities = ['Paris', 'Berlin', 'Rome', 'Madrid', 'London']
        self._index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._cities):
            raise StopIteration
        else:
            item = self._cities[self._index]
            self._index += 1
            return item
#Now, we have an iterator object, but we need to re-create it every time we want to start the iterations from the beginning:

cities = Cities()
list(enumerate(cities))
#[(0, 'Paris'), (1, 'Berlin'), (2, 'Rome'), (3, 'Madrid'), (4, 'London')]
cities=Cities()
[item.upper() for item in cities]
#['PARIS', 'BERLIN', 'ROME', 'MADRID', 'LONDON']
cities=Cities()
sorted(cities)
#['Berlin', 'London', 'Madrid', 'Paris', 'Rome']
# =============================================================================
# So, we basically have to "restart" an iterator by creating a new one each time.
# 
# But in this case, we are also re-creating the underlying data every time - seems wasteful!
# 
# Instead, maybe we can split the iterator part of our code from the data part of our code.
# 
# =============================================================================
class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']
        
    def __len__(self):
        return len(self._cities)
#And let's create our iterator this way:

class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        self._city_obj = city_obj
        self._index = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item
#So now we can create our Cities instance once:

cities = Cities()
#and create as many iterators as we want, but passing it the same Cities instance everyt time:

iter_1 = CityIterator(cities)
for city in iter_1:
    print(city)
# =============================================================================
# New York
# Newark
# New Delhi
# Newcastle
# =============================================================================
iter_2 = CityIterator(cities)
[city.upper() for city in iter_2]
#['NEW YORK', 'NEWARK', 'NEW DELHI', 'NEWCASTLE']
#So, we're almost at a solution now. At least we can create the iterator objects without having to recreate the Cities object every time.

#But, we still have to remember to create a new iterator, and we can no longer iterate over the cities object anymore!

for city in cities:
    print(city)
# =============================================================================
# ---------------------------------------------------------------------------
# TypeError                                 Traceback (most recent call last)
# <ipython-input-11-d57230a6a2ef> in <module>()
# ----> 1 for city in cities:
#       2     print(city)
# 
# TypeError: 'Cities' object is not iterable
# 
# This is where the first question we asked comes into play. Whenever we iterated our iterator, the first thing Python did was call __iter__.
# 
# In fact, let's just check that again:
# 
# =============================================================================
class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        print('Calling CityIterator __init__')
        self._city_obj = city_obj
        self._index = 0
        
    def __iter__(self):
        print('Calling CitiyIterator instance __iter__')
        return self
    
    def __next__(self):
        print('Calling __next__')
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item
iter_1 = CityIterator(cities)
#Calling CityIterator __init__
for city in iter_1:
    print(city)
# =============================================================================
# #Calling CitiyIterator instance __iter__
# Calling __next__
# New York
# Calling __next__
# Newark
# Calling __next__
# New Delhi
# Calling __next__
# Newcastle
# Calling __next__
# Iterables
# Now we finally come to how an iterable is defined in Python.
# 
# An iterable is an object that:
# 
# implements the __iter__ method
# and that method returns an iterator which can be used to iterate over the object
# What would happen if we put an __iter__ method in the Cities object and then try to iterate?
# 
# When we try to iterate over the Cities instance, Python will first call __iter__. The __iter__ method should then return an iterator which Python will use for the iteration.
# 
# We actually have everything we need to now make Cities an iterable since we already have the CityIterator created:
# 
# =============================================================================
class CityIterator:
    def __init__(self, city_obj):
        # cities is an instance of Cities
        print('Calling CityIterator __init__')
        self._city_obj = city_obj
        self._index = 0
        
    def __iter__(self):
        print('Calling CitiyIterator instance __iter__')
        return self
    
    def __next__(self):
        print('Calling __next__')
        if self._index >= len(self._city_obj):
            raise StopIteration
        else:
            item = self._city_obj._cities[self._index]
            self._index += 1
            return item
class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']
        
    def __len__(self):
        return len(self._cities)
    
    def __iter__(self):
        print('Calling Cities instance __iter__')
        return CityIterator(self)
cities = Cities()
for city in cities:
    print(city)
# =============================================================================
# Calling Cities instance __iter__
# Calling CityIterator __init__
# Calling __next__
# New York
# Calling __next__
# Newark
# Calling __next__
# New Delhi
# Calling __next__
# Newcastle
# Calling __next__
# And watch what happens if we try to run that loop again:
# =============================================================================

for city in cities:
    print(city)
# =============================================================================
# Calling Cities instance __iter__
# Calling CityIterator __init__
# Calling __next__
# New York
# Calling __next__
# Newark
# Calling __next__
# New Delhi
# Calling __next__
# Newcastle
# Calling __next__
# A new iterator was created when the for loop started.
# 
# In fact, same happens for anything that is going to iterate our iterable - it first calls the __iter__ method of the itrable to get a new iterator, then uses the iterator to call __next__.
# 
# =============================================================================
list(enumerate(cities))
# =============================================================================
# Calling Cities instance __iter__
# Calling CityIterator __init__
# Calling __next__
# Calling __next__
# Calling __next__
# Calling __next__
# Calling __next__
# [(0, 'New York'), (1, 'Newark'), (2, 'New Delhi'), (3, 'Newcastle')]
# =============================================================================
sorted(cities, reverse=True)
# =============================================================================
# Calling Cities instance __iter__
# Calling CityIterator __init__
# Calling __next__
# Calling __next__
# Calling __next__
# Calling __next__
# Calling __next__
# ['Newcastle', 'Newark', 'New York', 'New Delhi']
# Now we can put the iterator class inside our Cities class to keep the code self-contained:
# =============================================================================

del CityIterator  # just to make sure CityIterator is not in our global scope
class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']
        
    def __len__(self):
        return len(self._cities)
    
    def __iter__(self):
        print('Calling Cities instance __iter__')
        return self.CityIterator(self)
    
    class CityIterator:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0
​
        def __iter__(self):
            print('Calling CitiyIterator instance __iter__')
            return self
​
        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item
cities = Cities()
list(enumerate(cities))
# =============================================================================
# Calling Cities instance __iter__
# Calling CityIterator __init__
# Calling __next__
# Calling __next__
# Calling __next__
# Calling __next__
# Calling __next__
# [(0, 'New York'), (1, 'Newark'), (2, 'New Delhi'), (3, 'Newcastle')]
# Technically we can even get an iterator instance ourselves directly, by calling iter() on the cities object:
# 
# =============================================================================
iter_1 = iter(cities)
iter_2 = iter(cities)
#Calling Cities instance __iter__
#Calling CityIterator __init__
#Calling Cities instance __iter__
#Calling CityIterator __init__
#As you can see, Python created and returned two different instances of the CityIterator object.

id(iter_1), id(iter_2)
#(1741231353928, 1741231354320)
#And now we also have should understand why iterators also implement the __iter__ method (that just returns themselves) - it makes them iterables too!

#Mixing Iterables and Sequences
#Cities is an iterable, but it is not a sequence type:

cities = Cities()
len(cities) #4
# =============================================================================
# cities[1]
# ---------------------------------------------------------------------------
# TypeError                                 Traceback (most recent call last)
# <ipython-input-30-e8dda3d9f35c> in <module>()
# ----> 1 cities[1]
# 
# TypeError: 'Cities' object does not support indexing
# 
# Since our Cities could also be a sequence, we could also decide to implement the __getitem__ method to make it into a sequence:
# =============================================================================

class Cities:
    def __init__(self):
        self._cities = ['New York', 'Newark', 'New Delhi', 'Newcastle']
        
    def __len__(self):
        return len(self._cities)
    
    def __getitem__(self, s):
        print('getting item...')
        return self._cities[s]
    
    def __iter__(self):
        print('Calling Cities instance __iter__')
        return self.CityIterator(self)
    
    class CityIterator:
        def __init__(self, city_obj):
            # cities is an instance of Cities
            print('Calling CityIterator __init__')
            self._city_obj = city_obj
            self._index = 0
​
        def __iter__(self):
            print('Calling CitiyIterator instance __iter__')
            return self
​
        def __next__(self):
            print('Calling __next__')
            if self._index >= len(self._city_obj):
                raise StopIteration
            else:
                item = self._city_obj._cities[self._index]
                self._index += 1
                return item
cities = Cities()
#It's a sequence:

cities[0]
#getting item...
#'New York'
#It's also an iterable:

next(iter(cities))
# =============================================================================
# Calling Cities instance __iter__
# Calling CityIterator __init__
# Calling __next__
# 'New York'
# Now that Cities is both a sequence type (__getitem__) and an iterable (__iter__), when we loop over cities, is Python going to use __getitem__ or __iter__?
# 
# =============================================================================
cities = Cities()
for city in cities:
    print(city)
# =============================================================================
# Calling Cities instance __iter__
# Calling CityIterator __init__
# Calling __next__
# New York
# Calling __next__
# Newark
# Calling __next__
# New Delhi
# Calling __next__
# Newcastle
# Calling __next__
# It uses the iterator - so Python will use the iterator if there is one, otherwise it will fall back to using __getitem__. If neither is implemented, we'll get an exception.
# 
# Of course, for selection by index or slice, the __getitem__ method must be implemented.
# 
# We'll come back to this very topic in an upcoming video, because behind the scenes, even if we only implement the __getitem__ method, Python will auto-generate an iterator for us!
# 
# Python Built-In Iterables and Iterators
# The way iterables and iterators work in our custom Cities example is exactly the way Python iterables work too.
# =============================================================================

l = [1, 2, 3]
#Since lists are iterables, they implement the __iter__ method and we can get an iterator for the list:

iter_l = iter(l)
#or could use iter_1 = l.__iter__()
type(iter_l)
#list_iterator
next(iter_l)
#1
next(iter_l)
#2
next(iter_l)
#3
next(iter_l)
# =============================================================================
# ---------------------------------------------------------------------------
# StopIteration                             Traceback (most recent call last)
# <ipython-input-42-c2f95d80ff72> in <module>()
# ----> 1 next(iter_l)
# 
# StopIteration: 
# 
# See? The same StopIteration exception is raised.
# 
# Since iter_l is an iterator, it also implements the __iter__ method, which just returns the iterator itself:
# 
# =============================================================================
id(iter_l), id(iter(iter_l))
#(1741231347248, 1741231347248)
'__next__' in dir(iter_l)
#True
'__iter__' in dir(iter_l)
#True
#Since the list l is an iterable it also implements the __iter__ method:

'__iter__' in dir(l)
#True
#but does not implement a __next__ method:

'__next__' in dir(l)
#False
#Of course, since lists are also sequence types, they also implement the __getitem__ method:

'__getitem__' in dir(l)
#True
#Sets and dictionaries on the other hand are not sequence types:

'__getitem__' in dir(set)
#False
'__iter__' in dir(set)
#True
s = {1, 2, 3}
'__next__' in dir(iter(s))
#True
'__iter__' in dir(dict)
#True
#But what does the iterator for a dictionary actually return? It iterates over what? You shoudl probably already guess the answer to that one!

d = dict(a=1, b=2, c=3)
iter_d = iter(d)
next(iter_d)
#'a'
#Dictionary iterators will iterate over the keys of the dictionary.

#To iterate over the values, we could use the values() method which returns an iterable over the values of the dictionary:

iter_vals = iter(d.values())
next(iter_vals)
#1
#And to iterate over both the keys and values, dictionaries provide an items() iterable:

iter_items = iter(d.items())
next(iter_items)
('a', 1)
#Here we get an iterator over key, value tuples

#We'll examine the usefullness of being able to iterate using next instead of a for loop, or comprehension, in the next video.
