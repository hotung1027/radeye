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

def apply_map(funcs:list,values:list):
    for fn,value in zip(funcs,values):
        fn(value)
        
def split_channels(array:np.ndarray,size_x:int,size_y:int)->np.ndarray:
    return np.array(
        [
            array[i:i+size_x,j:j+size_y]
            for i in range(0,array.shape[0],size_x)
            for j in range(0,array.shape[1],size_y)
        ]
    )

def findClosetFromItems(items:list[any],point:any)->int:
    diff = np.array(items - point).reshape(-1,1)
    norm = np.linalg.norm(diff,axis = 1)
    result = np.argmin(norm)
    return result