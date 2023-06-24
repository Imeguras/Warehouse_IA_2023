from ga.individual_int_vector import IntVectorIndividual
import ga.genetic_algorithm
from warehouse.pair import Pair
import random
class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int):
        super().__init__(problem, num_genes)
        self.problem = problem
        self.genome = []
        #self.genome = self.generate_genome(num_genes)
        
        # self.cost = 0
        # RETODO

    def compute_fitness(self) -> float:
      # Por agora self.fitness = obtain_all_path total cost
      self.fitness = 0.0
      palatin_matrix = self.obtain_all_path()
      for i in range(len(palatin_matrix)):
        self.fitness += len(palatin_matrix[i])

    
      return self.fitness

    def generate_genome(self, num_genes: int):
        tmpProducts = list(range(0,num_genes))
      
        for i in range(num_genes):
            randomIndex = ga.genetic_algorithm.rand.randrange(0,num_genes)
            self.genome.append(tmpProducts[randomIndex])
            tmpProducts.pop(randomIndex)
            num_genes -= 1
        return self.genome

    # Calcula os caminhos completos percorridos pelos forklifts. Devolve uma lista de listas de células(as células percorridas por cada forklift);
    # e o numero máximo de passos necessário para percorrer todos os caminhos(i.e, o numero de células do caminho mais longo percorrido por um forklift)
    
    #Adendum por agora so vai dar uma lista de listas com todas as actions para chegar do inicio até ao ponto em que ele tera de voltar ao fim

    def obtain_all_path(self):
      listPathsbyForkLifts = []
      num_forklifts = len(self.problem.agent_search.forklifts)
      for f in range(num_forklifts):
        listPathsbyForkLifts.append([])
      


      for i in range(len(self.genome)):
        currentForklift = (i % num_forklifts)
        previous_product_index = i - num_forklifts
        
        # get the last cell and the current 
        
        current_cell = self.problem.agent_search.initial_environment.products[self.genome[i]]
        if previous_product_index < 0:
          previous_cell = self.problem.agent_search.forklifts[currentForklift]
        else: 
          previous_cell = self.problem.agent_search.initial_environment.products[self.genome[previous_product_index]]

        # create a temporary pair for formalities
        tmpPair = Pair(previous_cell, current_cell)
        # hash the pair
        hash_pair = tmpPair.hash()
        #find the pair through the hash in agent_search.pairsDictionary
        print("hash é: "+hash_pair)
        print(self.problem.agent_search.pairsDictionary)
        pair = self.problem.agent_search.pairsDictionary.get(hash_pair)
        if pair is None:
          print("Pair not found")
          return None

        # get path of pair 
        path = pair.path_resolution
        # Concatenate the path to its corresponding sublist in listPathsbyForkLifts
        listPathsbyForkLifts[currentForklift] += path
      return listPathsbyForkLifts   
        


      
    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str (self.genome) + "\n\n"
        # RETODO
        return string

    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo):
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        # RETODO
        return new_instance
