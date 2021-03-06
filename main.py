import sys
import math
# Files
from functions import toBin, lruPolicy, time

# Constants
addr_size = 32
KB = 1024


cache_size = int(sys.argv[1]) # Between 32 and 128, in KB
block_size = int(sys.argv[2]) # Between 32 and 128, in bytes
associativity = int(sys.argv[3]) # Number of ways, between 4 and 16
input_file = sys.argv[4]

offset = math.log(block_size, 2)
index = math.log(cache_size * KB / (block_size * associativity), 2)
tag = addr_size - offset - index

print("Cache size:", cache_size, "KB")
print("Block size:", block_size , "bytes")
print("Associativity:", associativity)

file = open(input_file, "r")

start = time.time()

cache = []
for i in range(associativity):
    way = []
    for j in range(int(2**index)):
        # Set structure: valid, tag, LRU value
        way.append([0, 0, 0])
    cache.append(way)

hits = 0
misses = 0
evictions = 0
time_optimized = 0
time_not_optimized = 0

for line in file:
    addr = toBin(int(line[4], 16), 4).replace("0b", "") + toBin(int(line[5], 16), 4).replace("0b", "") + \
           toBin(int(line[6], 16), 4).replace("0b", "") + toBin(int(line[7], 16), 4).replace("0b", "") + \
           toBin(int(line[8], 16), 4).replace("0b", "") + toBin(int(line[9], 16), 4).replace("0b", "") + \
           toBin(int(line[10], 16), 4).replace("0b", "") + toBin(int(line[11], 16), 4).replace("0b", "")

    addr_tag = addr[0 : int(tag)]
    addr_index = addr[int(tag) : int(tag)+int(index)]
    addr_offset = addr[int(tag)+int(index) : int(tag)+int(index)+int(offset)]
    
    index_int = int(addr_index, 2)
    offset_int = int(addr_offset, 2)

    result, t1, t2, eviction = lruPolicy(cache, index_int, addr_tag, associativity, offset_int, block_size)
    
    if result:
        hits += 1
    else:  
        misses += 1    
    
    time_optimized += t1
    time_not_optimized += t2
    evictions += eviction

print("\nHits:", hits)
print("Misses:", misses)
print("Hit rate: {:.3f} %\n".format(hits/(hits+misses)*100) )
print("Evictions: {:.3f}".format(evictions))
print('Time optimized: {:.3f} seconds'.format(time_optimized))
print('Time not optimized:  {:.3f} seconds.'.format(time_not_optimized))
print("Optimized version is  {:.3f} times faster.".format(time_not_optimized/time_optimized))

end = time.time()    

print("Execution time:  {:.3f} minutes".format((end-start)/60))

