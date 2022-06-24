# =============================================================================
# Sorting Iterables
# There's nothing really new here - we have seen the sorted() function before when we looked at sorting sequences.
# 
# The sorted() function will in fact work with any iterable, not just sequences.
# 
# Let's try this by creating a custom iterable and then sorting it.
# 
# For this example, we'll create an iterable of random numbers, and then sort it.
# =============================================================================

import random
random.seed(0)
for i in range(10):
    print(random.randint(1, 10))
'''
10
4
9
3
5
3
2
10
5
9
'''
import random
​
class RandomInts:
    def __init__(self, length, *, seed=0, lower=0, upper=10):
        self.length = length
        self.seed = seed
        self.lower = lower
        self.upper = upper
        
    def __len__(self):
        return self.length
    
    def __iter__(self):
        return self.RandomIterator(self.length, 
                                   seed = self.seed, 
                                   lower = self.lower,
                                   upper=self.upper)
    
    
    class RandomIterator:
        def __init__(self, length, *, seed, lower, upper):
            self.length = length
            self.lower = lower
            self.upper = upper
            self.num_requests = 0
            random.seed(seed)
            
        def __iter__(self):
            return self
        
        def __next__(self):
            if self.num_requests >= self.length:
                raise StopIteration
            else:
                result = random.randint(self.lower, self.upper)
                self.num_requests += 1
                return result
randoms = RandomInts(10)
for num in randoms:
    print(num)
'''
6
6
0
4
8
7
6
4
7
5
We can now sort our iterable using the sorted() method:
'''
sorted(randoms)
#[0, 4, 4, 5, 6, 6, 6, 7, 7, 8]
sorted(randoms, reverse=True)
#[8, 7, 7, 6, 6, 6, 5, 4, 4, 0]
