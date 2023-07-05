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
        

def map(fn, values:list):
    return [fn(value) for value in values]
        
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



""" bind actions with given arugments and variables """
# reponse :: (QObject, str) -> (fn ::  var -> fn(var)) -> None
# equivalent to QObject::signal.connect(fn)
response = lambda var, signal: lambda fn : getattr(var,signal).conect(fn)
# bind :: (QObject) , str , fn -> (connect QObject::  var -> fn(var)) -> None
bind = lambda response, prop, fn: response(fn(prop))
# call :: ((fn :: (name,value)),name,type) -> (value -> fn(name,type(value))) -> None
call = lambda fn, name,type : lambda value: fn(name,type(value))
