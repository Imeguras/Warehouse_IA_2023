from ga.genetic_operators.recombination import Recombination
from ga.individual import Individual


class Recombination3(Recombination):

    def __init__(self, probability: float):
        super().__init__(probability)

    # Recombination Cycle
    def recombine(self, ind1: Individual, ind2: Individual) -> None:
        num_genes = len(ind1.genome)
        child1 = [-1] * num_genes
        child2 = [-1] * num_genes

        start = 0
        index = start
        while True:
            # Copiar o elemento do pai para o filho
            child1[index] = ind1.genome[index]
            child2[index] = ind2.genome[index]

            # Encontrar o elemento correspondente dos pais
            element1 = ind2.genome[index]
            element2 = ind1.genome[index]

            # Encontrar os indices
            index1 = ind1.genome.index(element1)
            index2 = ind2.genome.index(element2)

            # Ir para o proximo elemento
            index = index1

            # Se o ciclo acabo, break
            if index == start:
                break

        # Completar o resto dos elementos
        for i in range(num_genes):
            if child1[i] == -1:
                child1[i] = ind2.genome[i]
            if child2[i] == -1:
                child2[i] = ind1.genome[i]

        ind1.genome = child2
        ind2.genome = child1

    def __str__(self):
        return "Recombination 3 (" + f'{self.probability}' + ")"
