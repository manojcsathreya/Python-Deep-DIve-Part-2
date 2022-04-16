'''Custom Sequences (Part 2b/c)
For this example we'll re-use the Polygon class from a previous lecture on extending sequences.

We are going to consider a polygon as nothing more than a collection of points (and we'll stick to a 2-dimensional space).

So, we'll need a Point class, but we're going to use our own custom class instead of just using a named tuple.

We do this because we want to enforce a rule that our Point co-ordinates will be real numbers. We would not be able to use a named tuple to do that and we could end up with points whose x and y coordinates could be of any type.

First we'll need to see how we can test if a type is a numeric real type.

We can do this by using the numbers module.
'''

import numbers
#This module contains certain base types for numbers that we can use, such as Number, Real, Complex, etc.

isinstance(10, numbers.Number) #True
isinstance(10.5, numbers.Number) #True
isinstance(1+1j, numbers.Number) #True
#We will want out points to be real numbers only, so we can do it this way:

isinstance(1+1j, numbers.Real)
#False
isinstance(10, numbers.Real)
#True
isinstance(10.5, numbers.Real)
#True
#So now let's write our Point class. We want it to have these properties:

#The x and y coordinates should be real numbers only
#Point instances should be a sequence type so that we can unpack it as needed in the same way we were able to unpack the values of a named tuple.
class Point:
    def __init__(self, x, y):
        if isinstance(x, numbers.Real) and isinstance(y, numbers.Real):
            self._pt = (x, y)
        else:
            raise TypeError('Point co-ordinates must be real numbers.')
            
    def __repr__(self):
        return f'Point(x={self._pt[0]}, y={self._pt[1]})'
    
    def __len__(self):
        return len(self._pt)
    
    def __getitem__(self, s):
        return self._pt[s]
#Let's use our point class and make sure it works as intended:

p = Point(1, 2)
p #Point(x=1, y=2)
len(p) #2
p[0], p[1] #(1, 2)
x, y = p
x, y #(1, 2)
#Now, we can start creatiung our Polygon class, that will essentially be a mutable sequence of points making up the verteces of the polygon.

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        return f'Polygon({self._pts})'
#Let's try it and see if everything is as we expect:

p = Polygon()
p #Polygon([])
p = Polygon((0,0), [1,1])
p #Polygon([Point(x=0, y=0), Point(x=1, y=1)])
p = Polygon(Point(0, 0), [1, 1])
p #Polygon([Point(x=0, y=0), Point(x=1, y=1)])
#That seems to be working, but only one minor thing - our representation contains those square brackets which technically should not be there as the Polygon class init assumes multiple arguments, not a single iterable.

#So we shoudl fix that:

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join(self._pts)
        return f'Polygon({pts_str})'
#But that still won't work, because the join method expects an iterable of strings - here we are passing it an iterable of Point objects:

p = Polygon((0,0), (1,1))
p
'''
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
D:\Users\fbapt\Anaconda3\envs\deepdive\lib\site-packages\IPython\core\formatters.py in __call__(self, obj)
    691                 type_pprinters=self.type_printers,
    692                 deferred_pprinters=self.deferred_printers)
--> 693             printer.pretty(obj)
    694             printer.flush()
    695             return stream.getvalue()

D:\Users\fbapt\Anaconda3\envs\deepdive\lib\site-packages\IPython\lib\pretty.py in pretty(self, obj)
    378                             if callable(meth):
    379                                 return meth(obj, self, cycle)
--> 380             return _default_pprint(obj, self, cycle)
    381         finally:
    382             self.end_group()

D:\Users\fbapt\Anaconda3\envs\deepdive\lib\site-packages\IPython\lib\pretty.py in _default_pprint(obj, p, cycle)
    493     if _safe_getattr(klass, '__repr__', None) is not object.__repr__:
    494         # A user-provided repr. Find newlines and replace them with p.break_()
--> 495         _repr_pprint(obj, p, cycle)
    496         return
    497     p.begin_group(1, '<')

D:\Users\fbapt\Anaconda3\envs\deepdive\lib\site-packages\IPython\lib\pretty.py in _repr_pprint(obj, p, cycle)
    691     """A pprint that just redirects to the normal repr function."""
    692     # Find newlines and replace them with p.break_()
--> 693     output = repr(obj)
    694     for idx,output_line in enumerate(output.splitlines()):
    695         if idx:

<ipython-input-28-aa1e7e862518> in __repr__(self)
      7 
      8     def __repr__(self):
----> 9         pts_str = ', '.join(self._pts)
     10         return f'Polygon(pts_str)'

TypeError: sequence item 0: expected str instance, Point found

So, let's fix that:
'''

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
p = Polygon((0,0), (1,1))
p #Polygon(Point(x=0, y=0), Point(x=1, y=1))
#Ok, so now we can start making our Polygon into a sequence type, by implementing methods such as __len__ and __getitem__:

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]

#Notice how we are simply delegating those methods to the ones supported by lists since we are storing our sequence of points internally using a list!

p = Polygon((0,0), Point(1,1), [2,2])
p #Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2))
p[0] #Point(x=0, y=0)
p[::-1] #[Point(x=2, y=2), Point(x=1, y=1), Point(x=0, y=0)]
N#ow let's implement concatenation (we'll skip repetition - wouldn't make much sense anyway):

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, other):
        if isinstance(other, Polygon):
            new_pts = self._pts + other._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')

p1 = Polygon((0,0), (1,1))
p2 = Polygon((2,2), (3,3))
print(id(p1), p1)
print(id(p2), p2)
'''
1869044255880 Polygon(Point(x=0, y=0), Point(x=1, y=1))
1869044253528 Polygon(Point(x=2, y=2), Point(x=3, y=3))
'''
result = p1 + p2
print(id(result), result)
'''
1869044256552 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3))

Now, let's handle in-place concatenation. Let's start by only allowing the RHS of the in-place concatenation to be another Polygon:
'''
class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, other):
        if isinstance(other, Polygon):
            new_pts = self._pts + other._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
            
    def __iadd__(self, pt):
        if isinstance(pt, Polygon):
            self._pts = self._pts + pt._pts
            return self
        else:
            raise TypeError('can only concatenate with another Polygon')
p1 = Polygon((0,0), (1,1))
p2 = Polygon((2,2), (3,3))
print(id(p1), p1)
print(id(p2), p2)
'''
1869044255600 Polygon(Point(x=0, y=0), Point(x=1, y=1))
1869044255656 Polygon(Point(x=2, y=2), Point(x=3, y=3))
'''
p1 += p2
print(id(p1), p1)
#1869044255600 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3))
#So that worked, but this would not:

p1 = Polygon((0,0), (1,1))
p1 += [(2,2), (3,3)]
'''
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-76-0170f97bf2ba> in <module>()
----> 1 p1 += [(2,2), (3,3)]

<ipython-input-71-0441976a8455> in __iadd__(self, pt)
     28             return self
     29         else:
---> 30             raise TypeError('can only concatenate with another Polygon')

TypeError: can only concatenate with another Polygon

As you can see we get that type error. But we really should be able to handle appending any iterable of Points - and of course Pointsd could also be specified as just iterables of length 2 containing numbers:
'''
class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
            
    def __iadd__(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
        return self
p1 = Polygon((0,0), (1,1))
p1 += [(2,2), (3,3)]
p1 #Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3))
#Now let's implement some methods such as append, extend and insert:

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
            
    def __iadd__(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
        return self
    
    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
            
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
#Notice how we used almost the same code for __iadd__ and extend? The only difference is that __iadd__ returns the object, while extend does not - so let's clean that up a bit:

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
​
    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
#Now let's give all this a try:

p1 = Polygon((0,0), Point(1,1))
p2 = Polygon([2, 2], [3, 3])
print(id(p1), p1)
print(id(p2), p2)
'''
1869044425392 Polygon(Point(x=0, y=0), Point(x=1, y=1))
1869044427464 Polygon(Point(x=2, y=2), Point(x=3, y=3))
'''
p1 += p2
print(id(p1), p1)
#1869044425392 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3))
#That worked still, now let's see append:

p1 #Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3))
p1.append((4, 4))
p1 #Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4))
p1.append(Point(5,5))
print(id(p1), p1)
#1869044425392 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4), Point(x=5, y=5), Point(x=6, y=6), Point(x=7, y=7))
#append seems to be working, now for extend:

p3 = Polygon((6,6), (7,7))
p1.extend(p3)
print(id(p1), p1)
#1869044425392 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4), Point(x=5, y=5), Point(x=6, y=6), Point(x=7, y=7))
p1.extend([(8,8), Point(9,9)])
print(id(p1), p1)
#1869044425392 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4), Point(x=5, y=5), Point(x=6, y=6), Point(x=7, y=7), Point(x=8, y=8), Point(x=9, y=9))
#Now let's see if insert works as expected:

p1 = Polygon((0,0), (1,1), (2,2))
print(id(p1), p1)
#1869044022576 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2))
p1.insert(1, (100, 100))
print(id(p1), p1)
#1869044022576 Polygon(Point(x=0, y=0), Point(x=100, y=100), Point(x=1, y=1), Point(x=2, y=2))
p1.insert(1, Point(50, 50))
print(id(p1), p1)
#1869044022576 Polygon(Point(x=0, y=0), Point(x=50, y=50), Point(x=100, y=100), Point(x=1, y=1), Point(x=2, y=2))
#Now that we have that working, let's turn our attention to the __setitem__ method so we can support index and slice assignments:

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # value could be a single Point (or compatible type) for s an int
        # or it could be an iterable of Points if s is a slice
        # let's start by handling slices only first
        self._pts[s] = [Point(*pt) for pt in value]
            
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
​
    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
#So, we are only handling slice assignments at this point, not assignments such as p[0] = Point(0,0):

p = Polygon((0,0), (1,1), (2,2))
print(id(p), p)
#1869044422304 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2))
p[0:2] = [(10, 10), (20, 20), (30, 30)]
print(id(p), p)
#1869044422304 Polygon(Point(x=10, y=10), Point(x=20, y=20), Point(x=30, y=30), Point(x=2, y=2))
#So this seems to work fine. But this won't yet:

p[0] = Point(100, 100)
'''
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-120-9794a9715789> in <module>()
----> 1 p[0] = Point(100, 100)

<ipython-input-114-5972696942b0> in __setitem__(self, s, value)
     20         # or it could be an iterable of Points if s is a slice
     21         # let's start by handling slices only first
---> 22         self._pts[s] = [Point(*pt) for pt in value]
     23 
     24     def __add__(self, pt):

<ipython-input-114-5972696942b0> in <listcomp>(.0)
     20         # or it could be an iterable of Points if s is a slice
     21         # let's start by handling slices only first
---> 22         self._pts[s] = [Point(*pt) for pt in value]
     23 
     24     def __add__(self, pt):

TypeError: type object argument after * must be an iterable, not int

If we look at the precise error, we see that our list comprehension is the cause opf the error - we fail to correctly handle the case where the value passed in is not an iterable of Points...
'''
class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # value could be a single Point (or compatible type) for s an int
        # or it could be an iterable of Points if s is a slice
        # we could do this:
        if isinstance(s, int):
            self._pts[s] = Point(*value)
        else:
            self._pts[s] = [Point(*pt) for pt in value]
            
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
​
    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
#This will now work as expected:

p = Polygon((0,0), (1,1), (2,2))
print(id(p), p)
#1869044254368 Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2))
p[0] = Point(10, 10)
print(id(p), p)
#1869044254368 Polygon(Point(x=10, y=10), Point(x=1, y=1), Point(x=2, y=2))
#What happens if we try to assign a single Point to a slice:

p[0:2] = Point(10, 10)
'''
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-128-7031fa70fb2b> in <module>()
----> 1 p[0:2] = Point(10, 10)

<ipython-input-124-63cbbf5cccab> in __setitem__(self, s, value)
     23             self._pts[s] = Point(*value)
     24         else:
---> 25             self._pts[s] = [Point(*pt) for pt in value]
     26 
     27     def __add__(self, pt):

<ipython-input-124-63cbbf5cccab> in <listcomp>(.0)
     23             self._pts[s] = Point(*value)
     24         else:
---> 25             self._pts[s] = [Point(*pt) for pt in value]
     26 
     27     def __add__(self, pt):

TypeError: type object argument after * must be an iterable, not int

As expected this will not work. What about assigning an iterable of points to an index:
'''
p[0] = [Point(10, 10), Point(20, 20)]
'''
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-130-db4d01cbd125> in <module>()
----> 1 p[0] = [Point(10, 10), Point(20, 20)]

<ipython-input-124-63cbbf5cccab> in __setitem__(self, s, value)
     21         # we could do this:
     22         if isinstance(s, int):
---> 23             self._pts[s] = Point(*value)
     24         else:
     25             self._pts[s] = [Point(*pt) for pt in value]

<ipython-input-8-aacef18bb1a4> in __init__(self, x, y)
      4             self._pt = (x, y)
      5         else:
----> 6             raise TypeError('Point co-ordinates must be real numbers.')
      7 
      8     def __repr__(self):

TypeError: Point co-ordinates must be real numbers.

This works fine, but the error messages are a bit misleading - we probably shoudl do something about that:
'''
class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # we first should see if we have a single Point
        # or an iterable of Points in value
        try:
            rhs = [Point(*pt) for pt in value]
            is_single = False
        except TypeError:
            # not a valid iterable of Points
            # maybe a single Point?
            try:
                rhs = Point(*value)
                is_single = True
            except TypeError:
                # still no go
                raise TypeError('Invalid Point or iterable of Points')
        
        # reached here, so rhs is either an iterable of Points, or a Point
        # we want to make sure we are assigning to a slice only if we 
        # have an iterable of points, and assigning to an index if we 
        # have a single Point only
        if (isinstance(s, int) and is_single) \
            or isinstance(s, slice) and not is_single:
            self._pts[s] = rhs
        else:
            raise TypeError('Incompatible index/slice assignment')
                
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
​
    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
#So now let's see if we get better error messages:

p1 = Polygon((0,0), (1,1), (2,2))
p1[0:2] = (10,10)
'''
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-155-ed6b2e4597f7> in <module>()
----> 1 p1[0:2] = (10,10)

<ipython-input-153-5b38eea0109d> in __setitem__(self, s, value)
     39             self._pts[s] = rhs
     40         else:
---> 41             raise TypeError('Incompatible index/slice assignment')
     42 
     43     def __add__(self, pt):

TypeError: Incompatible index/slice assignment
'''

p1[0] = [(0,0), (1,1)]
'''
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-156-77ef903111fc> in <module>()
----> 1 p1[0] = [(0,0), (1,1)]

<ipython-input-153-5b38eea0109d> in __setitem__(self, s, value)
     39             self._pts[s] = rhs
     40         else:
---> 41             raise TypeError('Incompatible index/slice assignment')
     42 
     43     def __add__(self, pt):

TypeError: Incompatible index/slice assignment

And the allowed slice/index assignments work as expected:
    '''

p[0] = Point(100, 100)
p #Polygon(Point(x=100, y=100), Point(x=1, y=1), Point(x=2, y=2))
p[0:2] = [(0,0), (1,1), (2,2)]
p #Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=2, y=2))
#And if we try to replace with bad Point data:

p[0] = (0, 2+2j)
'''
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-161-37ccf6d72caa> in <module>()
----> 1 p[0] = (0, 2+2j)

<ipython-input-124-63cbbf5cccab> in __setitem__(self, s, value)
     21         # we could do this:
     22         if isinstance(s, int):
---> 23             self._pts[s] = Point(*value)
     24         else:
     25             self._pts[s] = [Point(*pt) for pt in value]

<ipython-input-8-aacef18bb1a4> in __init__(self, x, y)
      4             self._pt = (x, y)
      5         else:
----> 6             raise TypeError('Point co-ordinates must be real numbers.')
      7 
      8     def __repr__(self):

TypeError: Point co-ordinates must be real numbers.
'''

#We also get a better error message.

#Lastly let's see how we would implement the del keyword and the pop method.

#Recall how the del keyword works for a list:

l = [1, 2, 3, 4, 5]
del l[0] 
l #[2, 3, 4, 5]
del l[0:2]
l #[4, 5]
del l[-1]
l #[4]
#So, del works with indices (positive or negative) and slices too. We'll do the same:

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # we first should see if we have a single Point
        # or an iterable of Points in value
        try:
            rhs = [Point(*pt) for pt in value]
            is_single = False
        except TypeError:
            # not a valid iterable of Points
            # maybe a single Point?
            try:
                rhs = Point(*value)
                is_single = True
            except TypeError:
                # still no go
                raise TypeError('Invalid Point or iterable of Points')
        
        # reached here, so rhs is either an iterable of Points, or a Point
        # we want to make sure we are assigning to a slice only if we 
        # have an iterable of points, and assigning to an index if we 
        # have a single Point only
        if (isinstance(s, int) and is_single) \
            or isinstance(s, slice) and not is_single:
            self._pts[s] = rhs
        else:
            raise TypeError('Incompatible index/slice assignment')
                
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
​
    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
        
    def __delitem__(self, s):
        del self._pts[s]
p = Polygon(*zip(range(6), range(6)))
p #Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4), Point(x=5, y=5))
del p[0]
p #Polygon(Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4), Point(x=5, y=5))
del p[-1]
p #Polygon(Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4))
del p[0:2]
p #Polygon(Point(x=3, y=3), Point(x=4, y=4))
#Now, we just have to implement pop:

class Polygon:
    def __init__(self, *pts):
        if pts:
            self._pts = [Point(*pt) for pt in pts]
        else:
            self._pts = []
            
    def __repr__(self):
        pts_str = ', '.join([str(pt) for pt in self._pts])
        return f'Polygon({pts_str})'
    
    def __len__(self):
        return len(self._pts)
    
    def __getitem__(self, s):
        return self._pts[s]
    
    def __setitem__(self, s, value):
        # we first should see if we have a single Point
        # or an iterable of Points in value
        try:
            rhs = [Point(*pt) for pt in value]
            is_single = False
        except TypeError:
            # not a valid iterable of Points
            # maybe a single Point?
            try:
                rhs = Point(*value)
                is_single = True
            except TypeError:
                # still no go
                raise TypeError('Invalid Point or iterable of Points')
        
        # reached here, so rhs is either an iterable of Points, or a Point
        # we want to make sure we are assigning to a slice only if we 
        # have an iterable of points, and assigning to an index if we 
        # have a single Point only
        if (isinstance(s, int) and is_single) \
            or isinstance(s, slice) and not is_single:
            self._pts[s] = rhs
        else:
            raise TypeError('Incompatible index/slice assignment')
                
    def __add__(self, pt):
        if isinstance(pt, Polygon):
            new_pts = self._pts + pt._pts
            return Polygon(*new_pts)
        else:
            raise TypeError('can only concatenate with another Polygon')
​
    def append(self, pt):
        self._pts.append(Point(*pt))
        
    def extend(self, pts):
        if isinstance(pts, Polygon):
            self._pts = self._pts + pts._pts
        else:
            # assume we are being passed an iterable containing Points
            # or something compatible with Points
            points = [Point(*pt) for pt in pts]
            self._pts = self._pts + points
    
    def __iadd__(self, pts):
        self.extend(pts)
        return self
    
    def insert(self, i, pt):
        self._pts.insert(i, Point(*pt))
        
    def __delitem__(self, s):
        del self._pts[s]
        
    def pop(self, i):
        return self._pts.pop(i)
p = Polygon(*zip(range(6), range(6)))
p #Polygon(Point(x=0, y=0), Point(x=1, y=1), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4), Point(x=5, y=5))
p.pop(1)
Point(x=1, y=1)
p #Polygon(Point(x=0, y=0), Point(x=2, y=2), Point(x=3, y=3), Point(x=4, y=4), Point(x=5, y=5))
