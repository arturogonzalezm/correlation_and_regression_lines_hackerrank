import math
from abc import ABC, abstractmethod


# Strategy interface
class CorrelationStrategy(ABC):
    @abstractmethod
    def calculate(self, x, y):
        pass


# Pearson's implementation
class PearsonCorrelationStrategy(CorrelationStrategy):
    def calculate(self, x, y):
        mx = sum(x) / len(x)
        my = sum(y) / len(y)
        num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
        sx = sum((xi - mx) ** 2 for xi in x)
        sy = sum((yi - my) ** 2 for yi in y)
        return num / math.sqrt(sx * sy)


# Context that uses a correlation strategy
class CorrelationContext:
    def __init__(self, strategy):
        self._strategy = strategy

    def execute(self, x, y):
        return self._strategy.calculate(x, y)
