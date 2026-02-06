from typing import List

def harmonic_mean(numbers: List[float]) -> float:
    if not numbers:
        return 0.0
    
    return float(len(numbers)) / sum(1.0 / x for x in numbers)
    