from abc import ABC, abstractmethod

class AbstractAlgorithm(ABC):

    @abstractmethod
    def generate_points(self, dimensions, num_points):
        pass
    