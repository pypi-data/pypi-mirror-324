import numpy as np
import random

def bin_model_simulation(n_paths: int, max_time: int, S0: int, q: float, u: float, d: float) -> list[np.array]:
    '''
    This function simulates binomial model for *n_paths* number of paths for *max_time* periods. 
    It requiers initial stock value - *S0*, probability of going up and up and down factors.
    '''
    paths = []
    for _ in range(0, n_paths):
        xs = np.array(random.choices([d, u], weights = [1-q, q], k = max_time))
        path = xs.cumprod()
        path = S0*np.insert(path, 0, 1)
        paths.append(path)
        
    return np.array(paths)

def rw_simulations(n_paths: int, max_time: int, p: float) -> list[np.array]:
    '''The function simulates random walk: *n_paths* for *max_time* with probability *p* with step +1 or -1.'''
    paths = []
    for _ in range(0, n_paths):
        bern = random.choices([-1, 1], weights = [1-p, p], k = max_time)
        path = np.cumsum(bern)
        path = np.insert(path,0,0)
        paths.append(path)
    return paths

def bm_simulations(n_paths: int, granularity: int, max_time: int) -> list[np.array]:
    '''This function simulates brownion motion: *n_paths* number of paths for *max_time* periods with *granularity* scale.'''
    n_steps = granularity*max_time

    paths = []
    for _ in range(0, n_paths):
        seq = np.array(random.choices([-1, 1], weights = [0.5, 0.5], k = n_steps))
        path = np.cumsum(seq)/np.sqrt(granularity)
        path = np.insert(path,0,0)
        paths.append(path)    
   
    return paths
def bb_simulations(n_paths: int, granularity: int, max_time: int , T: int = 1) -> list[np.array]:
    '''
    This function simulates brownion bridge. It returns *n_paths* which follows Gaussian process s.t. B(t) = W(t) - t/T*W(T), 
    where W(t) is a Winer process. By defolt, T is fixed and equals to 1. 
    Function uses bm_simulation in it.

    Test version.
    '''
    n_steps = granularity*max_time
    w = np.array(bm_simulations(n_paths, granularity, max_time))
    t = np.linspace(0,T,n_steps+1)
    bridge = [w[i] - t/T*w[i][-1] for i in range(n_paths)]
    return bridge

if __name__ == '__main__':
    print("okay")