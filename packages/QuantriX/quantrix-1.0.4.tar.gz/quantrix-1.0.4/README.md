# QA


##### Description

The QuantriX library is aimed to provide essential tools for quantitative finance analysis. It is a copyrighted software available only for direct use. 

##### Available tools

The first version allows to build binomial model, random walk and brownion motion.

##### Instalation 

For installing, run these code in terminal:

```
pip install QuantriX
```

##### Usage

Available function can be used in the following ways:

1. Import necessary functions:
```
from quantrix.modules import bin_model_simulation
```
or 

```
from quantrix.modules import *
```

In the code, just use the function:
```
paths = bin_model_simulation(N, n, S0, q, u, d)
```

2. Import all existing modules:
```
from quantrix import modules
```

Use in the code in the following way:

```
paths = modules.bin_model_simulation(N, n, S0, q, u, d)
```

3. Available functions:

- bin_model_simulation(n_paths: int, max_time: int, S0: int, q: float, u: float, d: float) -> list[np.array]

This function simulates binomial model for *n_paths* number of paths for *max_time* periods. It requiers initial stock value - *S0*, probability of going up and up and down factors.

- rw_simulations(n_paths: int, max_time: int, p: float) -> list[np.array]

The function simulates random walk: *n_paths* for *max_time* with probability *p* with step +1 or -1.

- bm_simulations(n_paths: int, granularity: int, max_time: int) -> list[np.array]

This function simulates brownion motion: *n_paths* number of paths for *max_time* periods with *granularity* scale.

- bb_simulations(n_paths: int, granularity: int, max_time: int , T: int = 1) -> list[np.array]

This function simulates brownion bridge.