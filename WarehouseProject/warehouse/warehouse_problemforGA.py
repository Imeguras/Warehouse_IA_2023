from ga.problem import Problem
from warehouse.warehouse_agent_search import WarehouseAgentSearch
from warehouse.warehouse_individual import WarehouseIndividual
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
import ga.genetic_algorithm

class WarehouseProblemGA(Problem):
    def __init__(self, agent_search: WarehouseAgentSearch):
        # RETODO
        self.forklifts = agent_search.forklifts
        self.products = agent_search.products
        self.agent_search = agent_search
        self.heuristic = agent_search.heuristic
        self.initial_state = agent_search.initial_environment
        for i in agent_search.pairs: 
          s = WarehouseProblemSearch(agent_search.initial_environment, i)

    def generate_individual(self) -> "WarehouseIndividual":
        # cada genoma e a permutação de todos os forklifts com todos os produtos
        new_individual = WarehouseIndividual(self, len(self.products))
        # print(new_individual.genome)
        return new_individual


    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string

