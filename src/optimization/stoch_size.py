import numpy as np
import sys

def h(n, m):

    #s = np.ceil(n/m)+1
    s = n/m
    d = np.power(2,m)




    return (n+m)*s + n + 2*s*m*(d+m) +1

#def h(n, m):

  #  #s = np.floor(n/m)
  #  s = n/m
  #  d = np.power(2,m)
  #  q = (1-1/d)

  #  r = (np.power(q,n) - np.power(q,n-s*m))/(np.power(q,m) - 1)

  #  return 2*n*s - m*s*(s+1) + (m-2)*d*(s-r) + n*n/2 - m*s*(m-2*m-s*m)*2.6

#def h(n, m):

 #   #s = np.floor(n/m)
  #  s = n/m
   # d = np.power(2,m)
   # q = (1-1/d)

 #   r = (np.power(q,n) - np.power(q,n-s*m))/(np.power(q,m) - 1)

  #  return 2*n*s - m*s*(s+1) + (m-2)*d*(s-r) + n*n/2 - m*s/2*(m-2*m-s*m)

def min_m(n):

    max_m = np.ceil(np.log2(n)).astype(int)
    num_gates_min = np.finfo(float).max
    m_min = np.iinfo(int).max

    for m in np.array(range(1, max_m + 1)):

        num_gates = h(n, m)

        if num_gates < num_gates_min:
            num_gates_min = num_gates
            m_min = m

    return m_min


n_vec = range(2,2000)
m_opt_vec = []

for n in np.array(n_vec):
    print(f'n={n}; m_min={min_m(n)}')



