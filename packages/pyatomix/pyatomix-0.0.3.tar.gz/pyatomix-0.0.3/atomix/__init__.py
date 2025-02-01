import atomix_base
__all__ = ["AtomicInt", "AtomicTest"]

class AtomicInt():
    def __init__(self, value: int) -> None:
        self.base = atomix_base.AtomicInt(value)
    def __int__(self) -> int:
        return self.base.load()
    def increment(self) -> int:
        """ return result """
        return self.base.increment()
    def decrement(self) -> int:
        """ return result """
        return self.base.decrement()
    def store(self, value: int) -> None:
        self.base.store(value)
    def load(self) -> int:
        """ return result """
        return self.base.load()
    def add(self, value: int) -> int:
        """ return result """
        return self.base.add(value)
    def subtract(self, value: int) -> int:
        """ return result """
        return self.base.subtract(value)
    def exchange(self, value: int) -> int:
        """ return previous value """
        return self.base.exchange(value)
    def compare_exchange(self, expected: int, value: int) -> bool:
        """ return True if successful """
        return self.base.compare_exchange(expected, value)
    def compare_exchange_weak(self, expected: int, value: int) -> bool:
        """ return True if successful """
        return self.base.compare_exchange_weak(expected, value)
    def __eq__(self, value: object) -> bool:
        return self.base.load().__eq__(value)
    def __neq__(self, value: object) -> bool:
        return self.base.load().__neq__(value)
    def __neg__(self) -> int:
        return -self.base.load()
    def __invert__(self) -> int:
        return ~self.base.load()
    def __add__(self, value: int) -> int:
        return self.base.load() + value
    __radd__ = __add__
    def __iadd__(self, value: int):
        self.base.add(value)
        return self
    def __sub__(self, value: int) -> int:
        return self.base.load() - value
    def __rsub__(self, value: int) -> int:
        return value - self.base.load()
    def __isub__(self, value: int):
        self.base.subtract(value)
        return self
    def __mul__(self, value: int) -> int:
        return self.base.load() * value
    __rmul__ = __mul__
    def __imul__(self, value: int):
        self.base.exchange(self.base.load() * value)
        return self
    def __truediv__(self, value: int) -> int:
        return self.base.load() / value
    def __rtruediv__(self, value: int) -> int:
        return value / self.base.load()
    def __floordiv__(self, value: int) -> int:
        return self.base.load() // value
    def __ifloordiv__(self, value: int):
        self.base.exchange(self.base.load() // value)
        return self
    def __rfloordiv__(self, value: int) -> int:
        return value // self.base.load()
    def __mod__(self, value: int) -> int:
        return self.base.load() % value
    def __rmod__(self, value: int) -> int:
        return value % self.base.load()
    def __imod__(self, value: int):
        self.base.exchange(self.base.load() % value)
        return self
    def __pow__(self, value: int) -> int:
        return self.base.load() ** value
    def __rpow__(self, value: int) -> int:
        return value ** self.base.load()
    def __ipow__(self, value: int):
        self.base.exchange(self.base.load() ** value)
        return self
    def __and__(self, value: int) -> int:
        return self.base.load() & value
    __rand__ = __and__
    def __iand__(self, value: int):
        self.base.exchange(self.base.load() & value)
        return self
    def __or__(self, value: int) -> int:
        return self.base.load() | value
    __ror__ = __or__
    def __ior__(self, value: int):
        self.base.exchange(self.base.load() | value)
        return self
    def __xor__(self, value: int) -> int:
        return self.base.load() ^ value
    __rxor__ = __xor__
    def __ixor__(self, value: int):
        self.base.exchange(self.base.load() ^ value)
        return self
    def __lshift__(self, value: int) -> int:
        return self.base.load() << value
    def __rlshift__(self, value: int) -> int:
        return value << self.base.load()
    def __ilshift__(self, value: int):
        self.base.exchange(self.base.load() << value)
        return self
    def __rshift__(self, value: int) -> int:
        return self.base.load() >> value
    def __rrshift__(self, value: int) -> int:
        return value >> self.base.load()
    def __irshift__(self, value: int):
        self.base.exchange(self.base.load() >> value)
        return self
    def __lt__(self, value: int) -> bool:
        return self.base.load() < value
    def __le__(self, value: int) -> bool:
        return self.base.load() <= value
    def __gt__(self, value: int) -> bool:
        return self.base.load() > value
    def __ge__(self, value: int) -> bool:
        return self.base.load() >= value
    def __str__(self) -> str:
        return str(self.base.load())
    def __repr__(self) -> str:
        return f"AtomicInt({self.base.load()})"
    
class AtomicTest():
    def __init__(self) -> None:
        self.base = AtomicInt(0)
    def inc_test(self) -> bool:
        self.base.store(1)
        if self.base.increment() != 2:
            return False
        return self.base.load() == 2
    def dec_test(self) -> bool:
        self.base.store(1)
        if self.base.decrement() != 0:
            return False
        return self.base.load() == 0
    def store_test(self) -> bool:
        self.base.store(1)
        return self.base.load() == 1
    def add_test(self) -> bool:
        self.base.store(1)
        if self.base.add(1) != 2:
            return False
        return self.base.load() == 2
    def sub_test(self) -> bool:
        self.base.store(1)
        if self.base.subtract(1) != 0:
            return False
        return self.base.load() == 0
    def xchg_test(self) -> bool:
        self.base.store(1)
        if self.base.exchange(2) != 1:
            return False
        return self.base.load() == 2
    def cmp_xchg_test(self) -> bool:
        self.base.store(1)
        if self.base.compare_exchange(1, 2) != True:
            return False
        return self.base.load() == 2
    def cmp_xchg_weak_test(self) -> bool:
        self.base.store(1)
        if self.base.compare_exchange_weak(1, 2) != True:
            return False
        return self.base.load() == 2
    def operators(self) -> bool:
        self.base.store(1)
        if self.base + 1 != 2:
            return False
        self.base += 1
        if self.base.load() != 2 or self.base != 2:
            return False
        if self.base - 1 != 1:
            return False
        self.base -= 1
        if self.base.load() != 1 or self.base != 1:
            return False
        self.base.store(2)
        if self.base * 2 != 4:
            return False
        self.base *= 2
        if self.base.load() != 4 or self.base != 4:
            return False
        if self.base // 2 != 2:
            return False
        self.base //= 2
        if self.base.load() != 2 or self.base != 2:
            return False
        if 2 // self.base != 1:
            return False
        if 2 * self.base != 4:
            return False
        if self.base % 2 != 0:
            return False
        self.base %= 2
        if self.base.load() != 0 or self.base != 0:
            return False
        self.base.store(2)
        if self.base ** 2 != 4:
            return False
        self.base **= 2
        if self.base.load() != 4 or self.base != 4:
            return False
        if self.base & 2 != 0:
            return False
        self.base &= 2
        if self.base.load() != 0 or self.base != 0:
            return False
        if self.base | 2 != 2:
            return False
        self.base |= 2
        if self.base.load() != 2 or self.base != 2:
            return False
        if self.base ^ 2 != 0:
            return False
        self.base ^= 2
        if self.base.load() != 0 or self.base != 0:
            return False
        self.base.store(2)
        if self.base >> 1 != 1:
            return False
        self.base >>= 1
        if self.base.load() != 1 or self.base != 1:
            return False
        if 2 >> self.base != 1:
            return False
        if 2 << self.base != 4:
            return False
        if not self.base < 3:
            return False
        if not self.base <= 2:
            return False
        if not self.base > 0:
            return False
        if not self.base >= 1:
            return False
        return True
        
    def run(self):
        fail = 0
        if not self.inc_test():
            print("Increment test failed")
            fail += 1
        if not self.dec_test():
            print("Decrement test failed")
            fail += 1
        if not self.store_test():
            print("Store test failed")
            fail += 1
        if not self.add_test():
            print("Add test failed")
            fail += 1
        if not self.sub_test():
            print("Subtract test failed")
            fail += 1
        if not self.xchg_test():
            print("Exchange test failed")
            fail += 1
        if not self.cmp_xchg_test():
            print("Compare exchange strong test failed")
            fail += 1
        if not self.cmp_xchg_weak_test():
            print("Compare exchange weak test failed")
            fail += 1
        if not self.operators():
            print("Operators test failed")
            fail += 1
        if fail == 0:
            print("All tests passed")
        else:
            print(f"{fail} tests failed")