'''
SLICING

We've used slicing in this course before, but now it's time to dive deeper into slicing

Slicing relies on indexing →only works with sequence types

Mutable Sequence Types          Immutable Sequence Types

extract data                    extract data
assign data

Example l = [1, 2, 3, 4, 5]

        l[0:2] = ('a', 'b', 'c')

        l[0:2] → ['a', 'b', 'c', 3, 4, 5]

        l[0:2] → [1, 2]
-------------------------------------------------------------------------------------------
The Slice Type
Although we usually slice sequences using the more conventional notation:
my_list[i:j]

slice definitions are actually objects →of type slice

s = slice(0, 2) type(s) →slice  s.start → 0    s.end → 2
l = [1, 2, 3, 4, 5] l[s] → [1, 2]

This can be useful because we can name slices and use symbols 
instead of a literal subsequently

Similar to how you can name ranges in Excel…
-------------------------------------------------------------------------------------------
Slice Start and Stop Bounds

[i:j] start at i(including i) stop at j(excluding j)

all integers k where i <= k < j

also remember that indexing is zero-based

It can be convenient to think of slice bounds this way

a b c d e f
0 1 2 3 4 5 6
[1:4]
-------------------------------------------------------------------------------------------
Effective Start and Stop Bounds

Interestingly the following works: l = ['a', 'b', 'c', 'd', 'e', 'f']
                                   l[3:100] → ['d', 'e', 'f'] No error!
                                   we can specify slices that are "out of bounds"
                                   
In fact, negative indices work too: l[-1] → 'f'
                                    l[-3: -1] → ['d', 'e']
-------------------------------------------------------------------------------------------
Step Value
Slices also support a third argument – the step value [i:j:k]
                                                        slice(i, j, k)  (a.k.a stride)
When not specified, the step value defaults to 1

l = ['a', 'b', 'c', 'd', 'e', 'f']

l[0:6:2]            0, 2, 4        → ['a', 'c', 'e']

l[1:6:3]            1, 4           → ['b', 'e']

l[1:15:3]           1, 4           → ['b', 'e']

l[-1:-4:-1]         -1, -2, -3     → ['f', 'e', 'd']
-------------------------------------------------------------------------------------------
Range Equivalence

Any slice essentially defines a sequence of indices that is used to select elements for another 
sequence

In fact, any indices defined by a slice can also be defined using a range

The difference is that slices are defined independently of the sequence being sliced

The equivalent range is only calculated once the length of the sequence being sliced is known

Example
[0:100] l sequence of length 10 →range(0, 10)
        l sequence of length 6  →range(0, 6)
-------------------------------------------------------------------------------------------
Transformations [i:j]
The effective indices "generated" by a slice are actually dependent on the length of the 
sequence being sliced
Python does this by reducing the slice using the following rules: 

seq[i:j]         l = ['a', 'b', 'c', 'd', 'e', 'f']  length = 6

if i > len(seq)  →len(seq)
if j > len(seq)  →len(seq)       [0:100] → range(0, 6)


if i < 0 → max(0, len(seq) + i)     [-5:3] → range(1, 3)
if j < 0 → max(0, len(seq) + j)    [-10:3] → range(0, 3)



i omitted or None → 0               [:100] → range(0, 6)
j omitted or None → len(seq)        [3:] → range(3, 6)
                                    [:] → range(0, 6)

-------------------------------------------------------------------------------------------
Transformations [i:j:k], k > 0

With extended slicing things change depending on whether k is negative or positive
[i:j:k] = {x = i + n * k  0 <= n < (j-i)/k}

the indices are: i, i+k, i+2k, i+3k, …, < j stopping when j is reached or exceeded,
                                             but never including jitself
                                             
                                             l = ['a', 'b', 'c', 'd', 'e', 'f']  length = 6


if i, j > len(seq) →len(seq)          [0:100:2] → range(0, 6, 2)
if i, j < 0 →max(0, len(seq) + i/j)   [-10:100:2] → range(0, 6, 2)




i omitted or None →0          [:6:2] → range(0, 6, 2)   
j omitted or None →len(seq)   [1::2] → range(1, 6, 2)
                              [::2] → range(0, 6, 2)

same rules as [i:j]– makes sense, since that would be the same as [i:j:1]

-------------------------------------------------------------------------------------------
Transformations [i:j:k], k < 0
[i:j:k] = {x = i + n * k  0 <= n < (j-i)/k}
k < 0 the indices are: i, i+k, i+2k, i+3k, …, > j

l = ['a', 'b', 'c', 'd', 'e', 'f']

if i, j > len(seq) →len(seq) - 1       [5:2:-1] → range(5, 2, -1)
                                       [10:2:-1] → range(5, 2, -1)

if i, j < 0 →max(-1, len(seq) + i/j)    [5:-2:-1] → range(5, 4, -1)
                                        [-2:-5:-1] → range(4, 1, -1)
                                        [-2:-10:-1] → range(4, -1, -1)

i omitted or None →len(seq) - 1         [:-2:-1] → range(5, 4, -1)
jomitted or None →-1                    [5::-1] → range(5, -1, -1)
                                        [::-1] → range(5, -1, -1)
-------------------------------------------------------------------------------------------
Summary

[i:j]                       [i:j:k] k > 0                 [i:j:k] k < 0

i > len(seq)                len(seq)                        len(seq)-1
j > len(seq)                len(seq)                        len(seq)-1

i < 0                       max(0, len(seq)+i)              max(-1, len(seq)+i)
j < 0                       max(0, len(seq)+j)              max(-1, len(seq)+j)

i omitted / None            0                               len(seq)-1
j omitted / None            len(seq)                        -1
-------------------------------------------------------------------------------------------
      0    1    2    3    4    5
l = ['a', 'b', 'c', 'd', 'e', 'f']
    -6    -5   -4   -3    -2    -1

length = 6

[-10:10:1] -10 → 0
            10 → 6
            → range(0, 6)

[10:-10:-1] 10 → 5
        -10 → max(-1, 6-10) → max(-1, -4) → -1
        → range(5, -1, -1)
        
We can of course easily define empty slices!
[3:-1:-1] 3 → 3
          -1 → max(-1, 6-1) → 5
          → range(3, 5, -1)

seq= sequence of length 6

seq[::-1] iis omitted →len(seq) – 1 → 5
          jis omitted →-1
→ range(5, -1, -1) → 5, 4, 3, 2, 1, 0

seq = 'python'

seq[::-1] → 'nohtyp'
-------------------------------------------------------------------------------------------
If you get confused…

The sliceobject has a method, indices, that returns the equivalent range start/stop/step
for any slice given the length of the sequence being sliced:

slice(start, stop, step).indices(length) → (start, stop, step)

the values in this tuple can be used to generate a list of indices using the rangefunction

slice(10, -5, -1) with a sequence of length 6
i=10 > 6 → 6-1 → 5
j=-5 < 0 → max(-1, 6+-5) → max(-1, 1) → 1 → range(5, 1, -1)
→ 5, 4, 3, 2
slice(10, -5, -1).indices(6) → (5, 1, -1)
list(range(*slice(10,-5,-1).indices(6))) → [5, 4, 3, 2]

'''

s = slice(0,2)
s.start #0
s.stop #2
l = [1,2,3,4,5]
l[s] #[1, 2]
l[0:2] #[1, 2]

print(s) #slice(0, 2, None)

data = []
for row in data:
    first_name = row[0:51]
    last_name = row[51:101]
    ssn = row[101:111]

#insted of doing this we can do 

range_first_name = slice(0,51)
range_last_name = slice(51,101)
range_ssn = slice(101,111)
data = []
for row in data:
    first_name = row[range_first_name]
    last_name = row[range_last_name]
    ssn = row[range_ssn]
    
l = 'python'
l[0:1]#p
l[1:1]#''
l[0:600] #'python'
l[0:6:2] #'pto'
s1 = slice(0,6,2)
l[s1]#'pto'

l[:4] #'pyth'
#same as
l[None:4] #'pyth'
#or
s1 = slice(None,4)
l[s1]#'pyth'
#or
startt = None
l[startt:4] #'pyth'

l[3:] #'hon'
l[3:None] #'hon'
eend = None
l[3:eend] #'hon'


l[3:None:-1] #'htyp'
l[3::-1] #'htyp'

l[3:-1:-1]#''
l[3:-100:-1] #'htyp'

s = slice(1,5)
s.start #1
s.stop #5

s.indices(10) #(1, 5, 1)
#indicies method is used to find the range and it takes the length of the sequence as argument
s.indices(4) #(1, 4, 1)

slice(0,100,2).indices(10)#(0, 10, 2)
list(range(0, 10, 2)) #[0, 2, 4, 6, 8]

t = slice(0,100,2).indices(10)
t #(0, 10, 2)
list(range(*t)) #[0, 2, 4, 6, 8]

Start = 0
Stop = 10
step = 2
list(range(*slice(Start,Stop,step).indices(20))) # [0, 2, 4, 6, 8]

Start = 3
Stop = -1
step = -1
list(range(*slice(Start,Stop,step).indices(20))) # []

