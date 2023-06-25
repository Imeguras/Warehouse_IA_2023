
from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_operators.mutation import Mutation
from ga.genetic_algorithm import GeneticAlgorithm


class MutationInsert(Mutation):
    def __init__(self, probability):
        super().__init__(probability)


    def mutate(self, ind: IntVectorIndividual) -> None:
        num_genes = len(ind.genome)
        cut1 = GeneticAlgorithm.rand.randint(0, num_genes - 1)
        cut2 = cut1
        while (cut1 == cut2):
            cut2 = GeneticAlgorithm.rand.randint(0, num_genes - 1)

        if cut1 > cut2:
            cut1, cut2 = cut2, cut1

        aux = ind.genome[cut2]
        for i in range(cut2-1, cut1, -1):
            ind.genome[i+1] = ind.genome[i]
        ind.genome[cut1+1] = aux


    def __str__(self):
        return "Insert Mutation (" + f'{self.probability}' + ")"
