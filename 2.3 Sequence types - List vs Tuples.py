### Lists vs Tuples

#Remember that both lists and tuples are considered **sequence** types.

#Remember also that we should consider tuples as data structures (position has meaning) as we saw in an earlier section on named tuples.

#However, in this context we are going to view tuples as "immutable lists".

#Generally, tuples are more efficient that lists, so, unless you need mutability of the container, prefer using a tuple over a list.

#### Creating Tuples

#We saw some of this already in the first section of this course when we looked at some of the optimizations Python implements, but let's revisit it in this context.

#Here is Wikipedia's definition of constant folding:

#Constant folding is the process of recognizing and evaluating constant expressions at compile time rather than computing them at runtime.

#To see how this works, we are going to use the `dis` module which allows to see the disassembled Python bytecode - not for the faint of heart, but can be really useful!

from dis import dis

#We want to understand what Python does when it compiles statements such as:

#(1, 2, 3)
#[1, 2, 3]

dis(compile('(1,2,3, "a")', 'string', 'eval'))
'''
  1           0 LOAD_CONST               0 ((1, 2, 3, 'a'))
              2 RETURN_VALUE
'''

dis(compile('[1,2,3, "a"]', 'string', 'eval'))
'''
 1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 (2)
              4 LOAD_CONST               2 (3)
              6 LOAD_CONST               3 ('a')
              8 BUILD_LIST               4
             10 RETURN_VALUE
'''

'''
Notice how for a tuple containing constants (such as ints and strings in this case), the values are loaded in one step, a single constant value essentially. 

Lists, on the other hand are built-up on element at a time.

So, that's one reason why tuples can "load" faster than a list.

In fact, we can easily time this:
'''

from timeit import timeit

timeit("(1,2,3,4,5,6,7,8,9)", number=10_000_000) #0.199016600032337 secs
 
timeit("[1,2,3,4,5,6,7,8,9]", number=10_000_000) #1.3908247000072151 secs

#As you can see creating a tuple was faster.

#Now this changes if the tuple elements are not constants, such as lists or functions for example

def fn1():
    pass

dis(compile('(fn1, 10, 20)', 'string', 'eval'))
'''
  1           0 LOAD_NAME                0 (fn1)
              2 LOAD_CONST               0 (10)
              4 LOAD_CONST               1 (20)
              6 BUILD_TUPLE              3
              8 RETURN_VALUE
'''

dis(compile('[fn1, 10, 20]', 'string', 'eval'))
'''
  1           0 LOAD_NAME                0 (fn1)
              2 LOAD_CONST               0 (10)
              4 LOAD_CONST               1 (20)
              6 BUILD_LIST               3
              8 RETURN_VALUE
'''
or

dis(compile('([1,2], 10, 20)', 'string', 'eval'))
'''
  1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 (2)
              4 BUILD_LIST               2
              6 LOAD_CONST               2 (10)
              8 LOAD_CONST               3 (20)
             10 BUILD_TUPLE              3
             12 RETURN_VALUE
'''

dis(compile('[[1,2], 10, 20]', 'string', 'eval'))
'''
  1           0 LOAD_CONST               0 (1)
              2 LOAD_CONST               1 (2)
              4 BUILD_LIST               2
              6 LOAD_CONST               2 (10)
              8 LOAD_CONST               3 (20)
             10 BUILD_LIST               3
             12 RETURN_VALUE
'''

#And of course this is reflected in the timings too:

timeit("([1, 2], 10, 20)", number=1_000_000) #0.16698719997657463

timeit("[[1, 2], 10, 20]", number=1_000_000) #0.19448509998619556

#### Copying Lists and Tuples

#Let's look at creating a copy of both a list and a tuple:

l1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
t1 = (1, 2, 3, 4, 5, 6, 7, 8, 9)

id(l1), id(t1) #(1841575445120, 1841574951280)

l2 = list(l1)
t2 = tuple(t1)

#Let's time this:

timeit('tuple((1,2,3,4,5,6,7,8,9))', number=1_000_000) #0.1729234000085853

timeit('list([1,2,3,4,5,6,7,8,9])', number=1_000_000) #0.3323229000088759

#That's another win for tuples. But why?

#Let's look at the id's of the copies:

id(l1), id(l2), id(t1), id(t2) #(1841575445120, 1841575108800, 1841574951280, 1841574951280)

#in other words:

l1 is l2, t1 is t2 #(False, True)

#Notice how the `l1` and `l2` are **not** the same objects, whereas as `t1` and `t2` are!

#So for lists, the elements had to be copied (shallow copy, more on this later), but for tuples it did not.

#Note that this is the case even if the tuple contains non constant elements:

t1 = ([1,2], fn1, 3)
t2 = tuple(t1)
t1 is t2 #True

#### Storage Efficiency
'''
When mutable container objects such as lists, sets, dictionaries, etc are  created, and during their lifetime, the allocated capacity of these containers (the number of items they can contain) is greater than the number of elements in the container. This is done to make adding elements to the collection more efficient, and is called over-allocating.

Immutable containers on the other hand, since their item count is fixed once they have been created, do not need this overallocation - so their storage efficiency is greater.

Let's look at the size (memory) of lists and tuples as they get larger:
'''

import sys

prev = 0
for i in range(10):
    c = tuple(range(i+1))
    size_c = sys.getsizeof(c)
    delta, prev = size_c - prev, size_c
    print(f'{i+1} items: {size_c}, delta={delta}')
    '''
    1 items: 48, delta=48
2 items: 56, delta=8
3 items: 64, delta=8
4 items: 72, delta=8
5 items: 80, delta=8
6 items: 88, delta=8
7 items: 96, delta=8
8 items: 104, delta=8
9 items: 112, delta=8
10 items: 120, delta=8
    '''

prev = 0
for i in range(10):
    c = list(range(i+1))
    size_c = sys.getsizeof(c)
    delta, prev = size_c - prev, size_c
    print(f'{i+1} items: {size_c}, delta={delta}')
    
'''
1 items: 64, delta=64
2 items: 72, delta=8
3 items: 80, delta=8
4 items: 88, delta=8
5 items: 96, delta=8
6 items: 104, delta=8
7 items: 112, delta=8
8 items: 120, delta=8
9 items: 128, delta=8
10 items: 136, delta=8
'''

#As you can see the size delta for tuples as they get larger, remains a constant 8 bytes (the pointer to the element), but not so for lists which will over-allocate space (this is done to achieve better performance when appending elements to a list).

#Let's see what happens to the same list when we keep appending elements to it:

c = []
prev = sys.getsizeof(c)
print(f'0 items: {sys.getsizeof(c)}')
for i in range(255):
    c.append(i)
    size_c = sys.getsizeof(c)
    delta, prev = size_c - prev, size_c
    print(f'{i+1} items: {size_c}, delta={delta}')
    
'''
0 items: 56
1 items: 88, delta=32
2 items: 88, delta=0
3 items: 88, delta=0
4 items: 88, delta=0
5 items: 120, delta=32
6 items: 120, delta=0
7 items: 120, delta=0
8 items: 120, delta=0
9 items: 184, delta=64
10 items: 184, delta=0
11 items: 184, delta=0
12 items: 184, delta=0
13 items: 184, delta=0
14 items: 184, delta=0
15 items: 184, delta=0
16 items: 184, delta=0
17 items: 256, delta=72
18 items: 256, delta=0
19 items: 256, delta=0
20 items: 256, delta=0
21 items: 256, delta=0
22 items: 256, delta=0
23 items: 256, delta=0
24 items: 256, delta=0
25 items: 256, delta=0
26 items: 336, delta=80
27 items: 336, delta=0
28 items: 336, delta=0
29 items: 336, delta=0
30 items: 336, delta=0
31 items: 336, delta=0
32 items: 336, delta=0
33 items: 336, delta=0
34 items: 336, delta=0
35 items: 336, delta=0
36 items: 424, delta=88
37 items: 424, delta=0
38 items: 424, delta=0
39 items: 424, delta=0
40 items: 424, delta=0
41 items: 424, delta=0
42 items: 424, delta=0
43 items: 424, delta=0
44 items: 424, delta=0
45 items: 424, delta=0
46 items: 424, delta=0
47 items: 520, delta=96
48 items: 520, delta=0
49 items: 520, delta=0
50 items: 520, delta=0
51 items: 520, delta=0
52 items: 520, delta=0
53 items: 520, delta=0
54 items: 520, delta=0
55 items: 520, delta=0
56 items: 520, delta=0
57 items: 520, delta=0
58 items: 520, delta=0
59 items: 632, delta=112
60 items: 632, delta=0
61 items: 632, delta=0
62 items: 632, delta=0
63 items: 632, delta=0
64 items: 632, delta=0
65 items: 632, delta=0
66 items: 632, delta=0
67 items: 632, delta=0
68 items: 632, delta=0
69 items: 632, delta=0
70 items: 632, delta=0
71 items: 632, delta=0
72 items: 632, delta=0
73 items: 760, delta=128
74 items: 760, delta=0
75 items: 760, delta=0
76 items: 760, delta=0
77 items: 760, delta=0
78 items: 760, delta=0
79 items: 760, delta=0
80 items: 760, delta=0
81 items: 760, delta=0
82 items: 760, delta=0
83 items: 760, delta=0
84 items: 760, delta=0
85 items: 760, delta=0
86 items: 760, delta=0
87 items: 760, delta=0
88 items: 760, delta=0
89 items: 904, delta=144
90 items: 904, delta=0
91 items: 904, delta=0
92 items: 904, delta=0
93 items: 904, delta=0
94 items: 904, delta=0
95 items: 904, delta=0
96 items: 904, delta=0
97 items: 904, delta=0
98 items: 904, delta=0
99 items: 904, delta=0
100 items: 904, delta=0
101 items: 904, delta=0
102 items: 904, delta=0
103 items: 904, delta=0
104 items: 904, delta=0
105 items: 904, delta=0
106 items: 904, delta=0
107 items: 1064, delta=160
108 items: 1064, delta=0
109 items: 1064, delta=0
110 items: 1064, delta=0
111 items: 1064, delta=0
112 items: 1064, delta=0
113 items: 1064, delta=0
114 items: 1064, delta=0
115 items: 1064, delta=0
116 items: 1064, delta=0
117 items: 1064, delta=0
118 items: 1064, delta=0
119 items: 1064, delta=0
120 items: 1064, delta=0
121 items: 1064, delta=0
122 items: 1064, delta=0
123 items: 1064, delta=0
124 items: 1064, delta=0
125 items: 1064, delta=0
126 items: 1064, delta=0
127 items: 1240, delta=176
128 items: 1240, delta=0
129 items: 1240, delta=0
130 items: 1240, delta=0
131 items: 1240, delta=0
132 items: 1240, delta=0
133 items: 1240, delta=0
134 items: 1240, delta=0
135 items: 1240, delta=0
136 items: 1240, delta=0
137 items: 1240, delta=0
138 items: 1240, delta=0
139 items: 1240, delta=0
140 items: 1240, delta=0
141 items: 1240, delta=0
142 items: 1240, delta=0
143 items: 1240, delta=0
144 items: 1240, delta=0
145 items: 1240, delta=0
146 items: 1240, delta=0
147 items: 1240, delta=0
148 items: 1240, delta=0
149 items: 1440, delta=200
150 items: 1440, delta=0
151 items: 1440, delta=0
152 items: 1440, delta=0
153 items: 1440, delta=0
154 items: 1440, delta=0
155 items: 1440, delta=0
156 items: 1440, delta=0
157 items: 1440, delta=0
158 items: 1440, delta=0
159 items: 1440, delta=0
160 items: 1440, delta=0
161 items: 1440, delta=0
162 items: 1440, delta=0
163 items: 1440, delta=0
164 items: 1440, delta=0
165 items: 1440, delta=0
166 items: 1440, delta=0
167 items: 1440, delta=0
168 items: 1440, delta=0
169 items: 1440, delta=0
170 items: 1440, delta=0
171 items: 1440, delta=0
172 items: 1440, delta=0
173 items: 1440, delta=0
174 items: 1664, delta=224
175 items: 1664, delta=0
176 items: 1664, delta=0
177 items: 1664, delta=0
178 items: 1664, delta=0
179 items: 1664, delta=0
180 items: 1664, delta=0
181 items: 1664, delta=0
182 items: 1664, delta=0
183 items: 1664, delta=0
184 items: 1664, delta=0
185 items: 1664, delta=0
186 items: 1664, delta=0
187 items: 1664, delta=0
188 items: 1664, delta=0
189 items: 1664, delta=0
190 items: 1664, delta=0
191 items: 1664, delta=0
192 items: 1664, delta=0
193 items: 1664, delta=0
194 items: 1664, delta=0
195 items: 1664, delta=0
196 items: 1664, delta=0
197 items: 1664, delta=0
198 items: 1664, delta=0
199 items: 1664, delta=0
200 items: 1664, delta=0
201 items: 1664, delta=0
202 items: 1920, delta=256
203 items: 1920, delta=0
204 items: 1920, delta=0
205 items: 1920, delta=0
206 items: 1920, delta=0
207 items: 1920, delta=0
208 items: 1920, delta=0
209 items: 1920, delta=0
210 items: 1920, delta=0
211 items: 1920, delta=0
212 items: 1920, delta=0
213 items: 1920, delta=0
214 items: 1920, delta=0
215 items: 1920, delta=0
216 items: 1920, delta=0
217 items: 1920, delta=0
218 items: 1920, delta=0
219 items: 1920, delta=0
220 items: 1920, delta=0
221 items: 1920, delta=0
222 items: 1920, delta=0
223 items: 1920, delta=0
224 items: 1920, delta=0
225 items: 1920, delta=0
226 items: 1920, delta=0
227 items: 1920, delta=0
228 items: 1920, delta=0
229 items: 1920, delta=0
230 items: 1920, delta=0
231 items: 1920, delta=0
232 items: 1920, delta=0
233 items: 1920, delta=0
234 items: 2208, delta=288
235 items: 2208, delta=0
236 items: 2208, delta=0
237 items: 2208, delta=0
238 items: 2208, delta=0
239 items: 2208, delta=0
240 items: 2208, delta=0
241 items: 2208, delta=0
242 items: 2208, delta=0
243 items: 2208, delta=0
244 items: 2208, delta=0
245 items: 2208, delta=0
246 items: 2208, delta=0
247 items: 2208, delta=0
248 items: 2208, delta=0
249 items: 2208, delta=0
250 items: 2208, delta=0
251 items: 2208, delta=0
252 items: 2208, delta=0
253 items: 2208, delta=0
254 items: 2208, delta=0
255 items: 2208, delta=0
'''
'''
As you can see the size of the list doesn't grow every time we append an element - it only does so occasionally. Resizing a list is expensive, so not resizing every time an item is added helps out, so this method called *overallocation* is used that creates a larger container than required is used - on the other hand you don't want to overallocate too much as this has a memory cost.

If you're interested in learning more about why over-allocating is done and how it works (amortization), Wikipedia also has an excellent article on it: https://en.wikipedia.org/wiki/Dynamic_array

The book "Introduction to Algorithms", by "Cormen, Leiserson, Rivest and Stein" has a thorough discussion on it (under dynamic tables).

#### Retrieving Elements

Let's time retrieving an element from a tuple and a list:
    '''

t = tuple(range(100_000))
l = list(t)

timeit('t[99_999]', globals=globals(), number=10_000_000) #0.9043440999812447

timeit('l[99_999]', globals=globals(), number=10_000_000) #0.8595969000016339

#As you can see, retrieving elements from a tuple is very slightly faster than from a list. But consideting how small the difference really is, I'm not sure I would worry about it too much.

#There is a reason why this should be true, and it has to do with how tuples and lists are implemented in CPython. Tuples have direct access (pointers) to their elements, while lists need to first access another array that contains the pointers to the elements of the list.
