from ga.individual_int_vector import IntVectorIndividual
from ga.genetic_algorithm import GeneticAlgorithm
from warehouse.pair import Pair
from warehouse.cell import Cell
from agentsearch.action import Action
import random
import copy
class WarehouseIndividual(IntVectorIndividual):

    def __init__(self, problem: "WarehouseProblem", num_genes: int, collisionPunishment: float=10.0):
        super().__init__(problem, num_genes)
        self.problem = problem
        self.genome = []
        self.collisionPunishment = collisionPunishment
        

    def compute_fitness(self) -> float:
      # Por agora self.fitness = obtain_all_path total cost
      #TODO tomar em conta colisões 
      self.fitness = 0.0
      (palatin_matrix, _max ) = self.obtain_all_path()
      # count the forklif
      
      for i in range(len(palatin_matrix)):
        #spawnar o forklift não conta como passo e para a animação não bugar precisa de spawnar 
        self.fitness += len(palatin_matrix[i])-1
      # contar colisoes
      # percorrer palatin_matrix e ver se ha colisoes
      for j in range(_max): 
        temp = []
        for i in range(len(palatin_matrix)):
          #check if palatin_matrix[i][j] is in bounds
          if j < len(palatin_matrix[i]) and palatin_matrix[i][j] is not None:

            if palatin_matrix[i][j] is not None and palatin_matrix[i][j] in temp:
              #print("colisao"+palatin_matrix[i][j].__str__())
              self.fitness += self.collisionPunishment
            temp.append(palatin_matrix[i][j])
      


      

      return self.fitness

    def generate_genome(self, num_genes: int):
        tmpProducts = list(range(1,num_genes+1))

        for i in range(0,num_genes):
            randomIndex = GeneticAlgorithm.rand.randrange(0,num_genes)
            self.genome.append(tmpProducts[randomIndex])
            tmpProducts.pop(randomIndex)
            num_genes -= 1
        #print ("Genoma Criado"+self.genome.__str__())
        return self.genome
    def get_real_pair_references(self, pair: Pair)-> Pair:
      hash_pair = pair.hash()
      ret = self.problem.agent_search.pairsDictionary.get(hash_pair)
      if ret is None:
        print("Error: pair not found in dictionary| "+ pair.__str__())
      return ret
    # Calcula os caminhos completos percorridos pelos forklifts. Devolve uma lista de listas de células(as células percorridas por cada forklift);
    # e o numero máximo de passos necessário para percorrer todos os caminhos(i.e, o numero de células do caminho mais longo percorrido por um forklift)
    
    #Adendum por agora so vai dar uma lista de listas com todas as actions para chegar do inicio até ao ponto em que ele tera de voltar ao fim
    def obtain_all_path(self):
      def simulate_actions(path: list, initial_cell: Cell):
        out_list = []
        for action in path:
          out_list.append(action.sim_action(initial_cell))
          initial_cell = out_list[-1]
        return out_list
        
      cellListofLists = []
      num_forklifts = len(self.problem.agent_search.forklifts)
      for f in range(num_forklifts):
        cellListofLists.append([
          self.problem.agent_search.forklifts[f]
        ])
      
      for i in range(len(self.genome)):
        currentForklift = (i % num_forklifts)
        if len(cellListofLists[currentForklift]) > 0:
          previous_cell = cellListofLists[currentForklift][-1]
        else: 
          previous_cell = self.problem.agent_search.forklifts[currentForklift]
        
        current_cell = self.problem.agent_search.initial_environment.products[self.genome[i]]

        # Fetch the pair from the dictionary
        pair = self.get_real_pair_references(Pair(previous_cell, current_cell))
        # get path of pair
        path = pair.path_resolution

        real_deal = simulate_actions(path, previous_cell)
        # Concatenate the path to its corresponding sublist in actionListForklift
        cellListofLists[currentForklift] += real_deal
      
      # now lets force everyone back to the exit
      for i in range(num_forklifts):
        if len(cellListofLists[i]) > 0:
          previous_cell = cellListofLists[i][-1]
        else:
          previous_cell = self.problem.agent_search.forklifts[i]
        
        pair_to_exit = self.get_real_pair_references(Pair(previous_cell, self.problem.agent_search.exit))
        path_to_exit = pair_to_exit.path_resolution
        real_deal = simulate_actions(path_to_exit, previous_cell)
        cellListofLists[i] += real_deal
        
      return (cellListofLists, len(max(cellListofLists, key=len)))
      
      
    def __str__(self):
        string = 'Fitness: ' + f'{self.fitness}' + '\n'
        string += str (self.genome) + "\n\n"
        # RETODO
        return string
    #def __hash__(self):
    #  return hash(tuple(self.genome))
    def better_than(self, other: "WarehouseIndividual") -> bool:
        return True if self.fitness < other.fitness else False

    # __deepcopy__ is implemented here so that all individuals share the same problem instance
    def __deepcopy__(self, memo={}):
        if self in memo:
          return memo[self]
        new_instance = self.__class__(self.problem, self.num_genes)
        new_instance.genome = self.genome.copy()
        new_instance.fitness = self.fitness
        # RETODO
        return new_instance

    
        