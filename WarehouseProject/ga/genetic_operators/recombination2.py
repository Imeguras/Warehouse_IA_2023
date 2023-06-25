from ga.individual import Individual
from ga.genetic_operators.recombination import Recombination
from ga.genetic_algorithm import GeneticAlgorithm

class Recombination2(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = len(ind1.genome)
        cut1 = GeneticAlgorithm.rand.randint(0,num_genes -1)
        cut2 = GeneticAlgorithm.rand.randint(cut1, num_genes)

        child1 = [-1] * num_genes
        child1[cut1:cut2] = ind1.genome[cut1:cut2]
        current_index = cut2 % num_genes
        for gene in ind2.genome:
            if gene not in child1:
                child1[current_index] = gene
                current_index = (current_index + 1) % num_genes

        child2 = [-1] * len(ind1.genome)
        child2[cut1:cut2] = ind2.genome[cut1:cut2]
        current_index = cut2 % num_genes
        for gene in ind1.genome:
            if gene not in child2:
                child2[current_index] = gene
                current_index = (current_index + 1) % num_genes

        ind1.genome = child2
        ind2.genome = child1

    def __str__(self):
        return "Recombination 2 (" + f'{self.probability}' + ")"
