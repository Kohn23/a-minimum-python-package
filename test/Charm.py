import timeit
from random import randint
from mypkg._Charm import harmonic_mean

numbers = [randint(1, 1_000_000) for _ in range(1_000_000)]

t_ext = timeit.timeit(
    lambda: harmonic_mean(numbers),
    number=10  
)
print(f"mypkg._Charm.harmonic_mean: {t_ext/10:.4f} s")
