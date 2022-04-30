'''
LAZY ITERABLES

Lazy Evaluation
This is often used in class properties
properties of classes may not always be populated when the object is created
value of a property only becomes known when the property is requested - deferred

Example
class Actor:
    def __init__(self, actor_id):
        self.actor_id = actor_id
        self.bio = lookup_actor_in_db(actor_id)
        self.movies = None
    @property
    def movies(self):
        if self.movies is None:
            self.movies = lookup_movies_in_db(self.actor_id)
        return self.movies
----------------------------------------------------------------------------------------
Application to Iterables
We can apply the same concept to certain iterables

We do not calculate the next item in an iterable until it is actually requested

Example

iterable →Factorial(n)
will return factorials of consecutive integers from 0to n-1
do not pre-compute all the factorials
wait until nextrequests one, then calculate it

This is a form of lazy evaluation
----------------------------------------------------------------------------------------
Application to Iterables

Another application of this might be retrieving a list of forum posts

Posts might be an iterable
each call to nextreturns a list of 5 posts (or some page size)
but uses lazy loading
→every time nextis called, go back to database and get next 5 posts
----------------------------------------------------------------------------------------
Application to Iterables →Infinite Iterables

Using that lazy evaluation technique means that we can actually have infinite iterables

Since items are not computed until they are requested
we can have an infinite number of items in the collection

Don't try to use a for loop over such an iterable
unless you have some type of exit condition in your loop
→otherwise infinite loop!

Lazy evaluation of iterables is something that is used a lot in Python!
We'll examine that in detail in the next section on generators
'''
# =============================================================================
# Lazy Iterables
# An iterable is an object that can return an iterator (__iter__).
# 
# In turn an iterator is an object that can return itself (__iter__), and return the next value when asked (__next__).
# 
# Nothing in all this says that the iterable needs to be a finite collection, or that the elements in the iterable need to be materialized (pre-created) at the time the iterable / iterator is created.
# 
# Lazy evaluation is when evaluating a value is deferred until it is actually requested.
# 
# It is not specific to iterables however.
# 
# Simple examples of lazy evaluation are often seen in classes for calculated properties.
# 
# Let's look at an example of a lazy class property:
# =============================================================================

import math
​
class Circle:
    def __init__(self, r):
        self.radius = r
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, r):
        self._radius = r
        self.area = math.pi * r**2
#As you can see, in this circle class, every time we set the radius, we re-calculate and store the area. When we request the area of the circle, we simply return the stored value.

c = Circle(1)
#c.area
3.141592653589793
c.radius = 2
c.radius, c.area
#(2, 12.566370614359172)
#But instead of doing it this way, we could just calculate the area every time it is requested without actually storing the value:

class Circle:
    def __init__(self, r):
        self.radius = r
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, r):
        self._radius = r
​
    @property
    def area(self):
        return math.pi * self.radius ** 2
c = Circle(1)
#c.area
3.141592653589793
c.radius = 2
#c.area
12.566370614359172
#But the area is always recalculated, so we may take a hybrid approach where we want to store the area so we don't need to recalculate it every time (ecept when the radius is modified), but delay calculating the area until it is requested - that way if it is never requested, we didn't waste the CPU cycles to calculate it, or the memory to store it.

class Circle:
    def __init__(self, r):
        self.radius = r
        
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, r):
        self._radius = r
        self._area = None
​
    @property
    def area(self):
        if self._area is None:
            print('Calculating area...')
            self._area = math.pi * self.radius ** 2
        return self._area
c = Circle(1)
c.area
#Calculating area...
#3.141592653589793
c.area
#3.141592653589793
c.radius = 2
c.area
#Calculating area...
#12.566370614359172
#This is an example of lazy evaluation. We don't actually calculate and store an attribute of the class until it is actually needed.

#We can sometimes do something similar with iterables - we don't actually have to store every item of the collection - we may be able to just calculate the item as needed.

#In the following example we'll create an iterable of factorials of integers starting at 0, i.e.

#0!, 1!, 2!, 3!, ..., n!

class Factorials:
    def __init__(self, length):
        self.length = length
    
    def __iter__(self):
        return self.FactIter(self.length)
    
    class FactIter:
        def __init__(self, length):
            self.length = length
            self.i = 0
            
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.i >= self.length:
                raise StopIteration
            else:
                result = math.factorial(self.i)
                self.i += 1
                return result
            
facts = Factorials(5)
list(facts)
#[1, 1, 2, 6, 24]
#So as you can see, we do not store the values of the iterable, instead we just calculate the items as needed.

#In fact, now that we have this iterable, we don't even need it to be finite:

class Factorials:
    def __iter__(self):
        return self.FactIter()
    
    class FactIter:
        def __init__(self):
            self.i = 0
            
        def __iter__(self):
            return self
        
        def __next__(self):
            result = math.factorial(self.i)
            self.i += 1
            return result
factorials = Factorials()
fact_iter = iter(factorials)
​
for _ in range(10):
    print(next(fact_iter))
# =============================================================================
# 1
# 1
# 2
# 6
# 24
# 120
# 720
# 5040
# 40320
# 362880
# You'll notice that the main part of the iterable code is in the iterator, and the iterable itself is nothing more than a thin shell that allows us to create and access the iterator. This is so common, that there is a better way of doing this that we'll see when we deal with generators.
# =============================================================================
