class cyclic:
    def __init__(self,dir_):
        self.dir_ = dir_
        self.index = 0
        
    def __iter__(self):
        return self
    
    def __next__(self):
        res = self.dir_[self.index% len(self.dir_)]
        self.index+=1
        return res
    
c= cyclic('nsew')
for _ in range(10):
    print(next(c))
    
a = range(10)
for i in a:
    print(str(i)+next(c))
    '''
    0e
1w
2n
3s
4e
5w
6n
7s
8e
9w
    '''
    
#how to do it using in-builts
import itertools

n = 10
iter_cycle = itertools.cycle('NSWE')
items = [f'{i}{next(iter_cycle)}' for i in range(1,n+1)]
print(items)#['1N', '2S', '3W', '4E', '5N', '6S', '7W', '8E', '9N', '10S']

