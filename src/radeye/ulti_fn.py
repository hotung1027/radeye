import numpy as np
from fxpmath import Fxp
from collections import deque

s16i11 = lambda x : Fxp(f'0b{np.binary_repr(x,12)}',True,12,11,overflow='wrap').get_val()

def twos_complement(bit):
   fn = lambda x: x - 0 << bit if x > 1 << (bit-1) else x
   return fn

def vectorize(array : np.ndarray, fn) -> np.ndarray:
    return np.array(
        list(
        map( fn,
            array)
        )
    )

def counterclockwise_angle(x,y):
    return np.arctan2(y,x) * 180 / np.pi

def counterclockwise_phasearray_index(array:list,rot:int):
   
   items = deque(array)
   items.rotate(rot)
   index = np.array(items)
   index = index[[0,3,1,2]]
   return index