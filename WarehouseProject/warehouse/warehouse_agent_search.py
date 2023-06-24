from typing import TypeVar

import numpy as np

import constants
from agentsearch.agent import Agent
from agentsearch.state import State
from warehouse.cell import Cell
from warehouse.heuristic_warehouse import HeuristicWarehouse
from warehouse.pair import Pair
from collections import defaultdict

class WarehouseAgentSearch(Agent):
    S = TypeVar('S', bound=State)

    
    def __init__(self, environment: S):
        super().__init__()
        self.initial_environment = environment
        self.heuristic = HeuristicWarehouse()
        self.forklifts = []
        self.products = []
        self.exit = None
        self.pairs = []
        self.pairsDictionary = defaultdict(Pair)
        for i in range(environment.rows):
            for j in range(environment.columns):
                if environment.matrix[i][j] == constants.FORKLIFT:
                    self.forklifts.append(Cell(i, j))
                elif environment.matrix[i][j] == constants.EXIT:
                    self.exit = Cell(i, j)
                elif environment.matrix[i][j] == constants.PRODUCT:
                    self.products.append(Cell(i, j))
        self.fetch_pairs()
    def fetch_pairs(self)->list:
      #Isto e so para limpar o codigo 
      def pair_raw_manager(target_list, cellOrigin, cellDestiny):
        pair = Pair(cellOrigin, cellDestiny)
        index_pair = len(self.pairs)
        target_list.append(pair)
        self.pairsDictionary[pair.hash()] = pair

      def pair_product_manager(target_list, cellOrigin, cellDestiny): 
        pair_raw_manager(target_list, cellOrigin, cellDestiny)
        pair_raw_manager(target_list, cellDestiny, cellOrigin)
      
      for a in self.forklifts:
        for p in self.products:
          pair_raw_manager(self.pairs, a, p)
      
      for i in range(len(self.products) - 1):
        for j in range(i + 1, len(self.products)): 
          pair_product_manager(self.pairs, self.products[i], self.products[j])

      for p in self.products:
        pair_raw_manager(self.pairs, p, self.exit)

      for a in self.forklifts:
        pair_raw_manager(self.pairs, a, self.exit)          

    def __str__(self) -> str:
        str = "Pairs:\n"
        for p in self.pairs:
            str += f"{p}\n"
        return str

def read_state_from_txt_file(filename: str):
    with open(filename, 'r') as file:
        num_rows, num_columns = map(int, file.readline().split())
        float_puzzle = np.genfromtxt(file, delimiter=' ')
        return float_puzzle, num_rows, num_columns

# returns all pairs

   