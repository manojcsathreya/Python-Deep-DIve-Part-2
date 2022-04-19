'''
ITERATORS
Where we're at so far…

We created a custom container type object with a __next__ method
But it had several drawbacks:   →cannot use a forloop
                                →once we start using next there's no going back
                                →once we have reached StopIteration we're basically 
                                done with the object
Let's tackle the loop issue first
We saw how to iterate using __next__, StopIteration, and a whileloop

This is actually how Python handles forloops in general

Somehow, we need to tell Python that our class has that __next__
method and that it will behave in a way consistent with using a 
whileloop to iterate
Python knows we have __next__, but how does it know we implement 
StopIteration?
----------------------------------------------------------------------------------------
The iterator Protocol

A protocol is simply a fancy way of saying that our class is going to implement certain 
functionality that Python can count on

To let Python know our class can be iterated over using __next__ we implement the iterator protocol

The iterator protocol is quite simple – the class needs to implement two methods:
→__iter__ this method should just return the object (class instance) itself
sounds weird, but we'll understand why later

→__next__ this method is responsible for handing back the next 
element from the collection and raising the 
StopIteration exception when all elements have been 
handed out

An object that implements these two methods is called an iterator
----------------------------------------------------------------------------------------
Iterators
An iterator is therefore an object that implements:
__iter__ →just returns the object itself
__next__ →returns the next item from the container, or raises SopIteration

If an object is an iterator, we can use it with for loops, comprehensions, etc
Python will know how to loop (iterate) over such an object 
(basically using the same whileloop technique we used)
----------------------------------------------------------------------------------------
Example
Let's go back to our Squares example, and make it into an iterator

class Squares:
    def __init__(self, length):
        self.i = 0
        self.length = length
    def __next__(self):
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i ** 2
            self.i += 1
            return result
    #Adding __iter__
    def __iter__(self):
        return self

sq = Squares(5)
for item in sq:
    print(item)

0
1
4
9
16

→

Still one issue though!
The iterator cannot be "restarted"
Once we have looped through all the items
the iterator has been exhausted

To loop a second time through the 
collection we have to create a new 
instance and loop through that
'''
'''
In the last lecture we saw that we could approach iterating over a collection using this concept of next.

But there were some downsides that did not resolve (yet!):

we cannot use a for loop
once we exhaust the iteration (repeatedly calling next), we're essentially done with object. The only way to iterate through it again is to create a new instance of the object.
First we are going to look at making our next be usable in a for loop.

This idea of using __next__ and the StopIteration exception is exactly what Python does.

So, somehow we need to tell Python that the object we are dealing with can be used with next.

To do so, we create an iterator type object.

Iterators are objects that implement:

a __next__ method
an __iter__ method that simply returns the object itself
That's it - that's all there is to an iterator - two methods, __iter__ and __next__.

Let's go back to our Squares example:
    '''

class Squares:
    def __init__(self, length):
        self.length = length
        self.i = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i ** 2
            self.i += 1
            return result
#Now we can still call next:

sq = Squares(5)
print(next(sq)) #0
print(next(sq)) #1
print(next(sq)) #4
#Of course, our iterator still suffers from not being able to "reset" it - we just have to create a new instance:

sq = Squares(5)
#But now, we can also use a for loop:

for item in sq:
    print(item)
    '''
0
1
4
9
16
'''
#Now sq is exhausted, so if we try to loop through again:

for item in sq:
    print(item)
#We get nothing...

#All we need to do is create a new iterator:

sq = Squares(5)
for item in sq:
    print(item)
'''
0
1
4
9
16
'''
J#ust like Python's built-in next function calls our __next__ method, Python has a built-in function iter which calls the __iter__ method:

sq = Squares(5)
id(sq)
#1965579635736
id(sq.__iter__())
#1965579635736
id(iter(sq))
#1965579635736
#And of course we can also use a list comprehension on our iterator object:

sq = Squares(5)
[item for item in sq if item%2==0]
#[0, 4, 16]
#We can even use any function that requires an iterable as an argument (iterators are iterable):

sq = Squares(5)
list(enumerate(sq))
#[(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
#But of course we have to be careful, our iterator was exhausted, so if try that again:

list(enumerate(sq))
#[]
#we get an empty list - instead we have to create a new iterator first:

sq = Squares(5)
list(enumerate(sq))
#[(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
#We can even use the sorted method on it:

sq = Squares(5)
sorted(sq, reverse=True)
#[16, 9, 4, 1, 0]
'''
Python Iterators Summary
Iterators are objects that implement the __iter__ and __next__ methods.

The __iter__ method of an iterator just returns itself.

Once we fully iterate over an iterator, the iterator is exhausted and we can no longer use it for iteration purposes.

The way Python applies a for loop to an iterator object is basically what we saw with the while loop and the StopIteration exception.

'''
sq = Squares(5)
while True:
    try:
        print(next(sq))
    except StopIteration:
        break
'''
0
1
4
9
16
'''
#In fact we can easily see this by tweaking our iterator a bit:

class Squares:
    def __init__(self, length):
        self.length = length
        self.i = 0
        
    def __iter__(self):
        print('calling __iter__')
        return self
    
    def __next__(self):
        print('calling __next__')
        if self.i >= self.length:
            raise StopIteration
        else:
            result = self.i ** 2
            self.i += 1
            return result
sq = Squares(5)
for i in sq:
    print(i)
'''
calling __iter__
calling __next__
0
calling __next__
1
calling __next__
4
calling __next__
9
calling __next__
16
calling __next__
'''
#As you can see Python calls __next__ (and stops once a StopIteration exception is raised).

#But you'll notice that it also called the __iter__ method.

#In fact we'll see this happening in other places too:

sq = Squares(5)
[item for item in sq if item%2==0]
'''
calling __iter__
calling __next__
calling __next__
calling __next__
calling __next__
calling __next__
calling __next__
[0, 4, 16]
'''
sq = Squares(5)
list(enumerate(sq))
'''
calling __iter__
calling __next__
calling __next__
calling __next__
calling __next__
calling __next__
calling __next__
[(0, 0), (1, 1), (2, 4), (3, 9), (4, 16)]
'''
sq = Squares(5)
sorted(sq, reverse=True)
'''
calling __iter__
calling __next__
calling __next__
calling __next__
calling __next__
calling __next__
calling __next__
[16, 9, 4, 1, 0]
Why is __iter__ being called? After all, it just returns itself!
'''

#That's the topic of the next lecture!

#But let's see how we can mimic what Python is doing:

sq = Squares(5)
sq_iterator = iter(sq) #1965579704808 1965579704808
print(id(sq), id(sq_iterator))
while True:
    try:
        item = next(sq_iterator)
        print(item)
    except StopIteration:
        break
    '''
calling __iter__

calling __next__
0
calling __next__
1
calling __next__
4
calling __next__
9
calling __next__
16
calling __next__
As you can see, we first request an iterator from sq using the iter function, and then we iterate using the returned iterator. In the case of an iterator, the iter function just gets the iterator itself back.
'''
