from ga.problem import Problem
from warehouse.warehouse_agent_search import WarehouseAgentSearch
from warehouse.warehouse_individual import WarehouseIndividual
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch

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
        # TODO implement a method to generate a random individual
        pass

    def __str__(self):
        string = "# of forklifts: "
        string += f'{len(self.forklifts)}'
        string = "# of products: "
        string += f'{len(self.products)}'
        return string

