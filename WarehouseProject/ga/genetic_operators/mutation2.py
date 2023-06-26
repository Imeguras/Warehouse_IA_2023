from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation
from ga.genetic_algorithm import GeneticAlgorithm

# Swap mutation
class Mutation2(Mutation):
    def __init__(self, probability):
        super().__init__(probability)

    # Swap mutation
    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes-1)
        cut2 = cut1

        while (cut2==cut1):
            cut2 = GeneticAlgorithm.rand.randint(0, num_genes-1)

        ind.genome[cut1], ind.genome[cut2] = ind.genome[cut2], ind.genome[cut1]

    def __str__(self):
        return "Swap mutation (" + f'{self.probability}' + ")"
