## pyatomix provides a 64 bit AtomicInt class for Python

I'm pretty sure this is the only atomics library that works with Python 3.13 free-threaded.
Windows users will need to have Visual Studio installed to build this.
It uses Pybind11 and pip/setuptools will build it automatically.  It's been tested on Windows and Linux.

Under the hood it uses MSVC/GCC instrinsics or falls back to std::atomic.
Linux users will need the Python dev package installed for their Python version to install atomix, for instance: python3.13-dev

## Installation

```
pip install -U pyatomix
-or-
git clone https://github.com/0xDEADFED5/pyatomix.git
pip install -U ./pyatomix
```

## Usage

```python
from pyatomix import AtomicInt
x = AtomicInt(7) # initial value of 7
x += 1 # or
x.increment() # both are equivalent
```

all the math operators except /= are supported, so you can add/subtract/etc. and they'll be atomic.


# Performance

Depending on compiler and OS, AtomicInt increment is 4-5x slower than a standard increment, which is still pretty fast.
1 million atomic increments in a for loop takes me 160ms in Linux, while incrementing a regular int 1 million times takes 40ms.
On linux the GCC intrinsics were really close to std::atomics performance.  Intrinsics are a tiny bit faster than std::atomics on Windows.
If someone wants to create a PR for ARM intrinsics I'll add them, but I doubt there's much point.

# Note

If you use this in free-threaded Python, you will get this message:

RuntimeWarning: The global interpreter lock (GIL) has been enabled to load module 'atomix_base', which has not declared that it can run safely without the GIL. To override this behavior and keep the GIL disabled (at your own risk), run with PYTHON_GIL=0 or -Xgil=0.

I'm not sure what I need to add to this package to fix it, so in the meantime you can set the PYTHON_GIL environment variable.
Set it from powershell with this command: `$env:PYTHON_GIL = "0"`

compare_exchange_weak is unavailable in MSVC instrinsics, so if you want it in Windows you should uncomment the lines in main.cpp to force USE_ATOMIC

# To run the tests

```python
from pyatomix import AtomicTest
x = AtomicTest()
x.run()
```

# API list, all these are atomic

```python
AtomicInt.increment()                             : same as += 1
AtomicInt.decrement()                             : same as -= 1
AtomicInt.store(value)                            : assign value, doesn't return anything
AtomicInt.load()                                  : read value
AtomicInt.add(value)                              : same as += value
AtomicInt.subtract(value)                         : same as -= value
AtomicInt.exchange(value)                         : assign value. returns previous value
AtomicInt.compare_exchange(expected, value)       : if current value == expected, replace it with value. returns True on success
AtomicInt.compare_exchange_weak(expected, value)  : same as above, but use weak API if available.
```

# Overloaded operator list

`==,!=,-,~,+,+=,-=,*,*=,/,//,//=,|,|=,%,%=,**,**=,&,&=,^,^=,>>,>>=,<<,<<=,>,>=,<,<=`

