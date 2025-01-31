from dataclasses import dataclass
import numpy as np

@dataclass
class Clusters:
    entities: np.array
    labels: np.array
    centroids: np.array

    def get_data(self):
        return (self.entities, self.labels, self.centroids)
    
def max_n_subvectors(d):
    divisors = [m for m in range(1, d + 1) if d % m == 0]
    return max([m for m in divisors if m <= 64])