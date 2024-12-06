# Example of using icecream for debugging
# source: https://www.geeksforgeeks.org/debugging-with-ice-cream-in-python/

from icecream import ic 
  
a = 3
b = 11
c = 42
  
for i in range(80,83): 
    a = a*i 
    b = b*i 
    c = c*i 
    ans = (ic(a)+ic(b)+ic(c))/3
    ic(int(ans))