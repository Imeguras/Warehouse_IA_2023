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
        self.pairsDictionary = defaultdict(list)
        for i in range(environment.rows):
            for j in range(environment.columns):
                if environment.matrix[i][j] == constants.FORKLIFT:
                    self.forklifts.append(Cell(i, j))
                elif environment.matrix[i][j] == constants.EXIT:
                    self.exit = Cell(i, j)
                elif environment.matrix[i][j] == constants.PRODUCT:
                    self.products.append(Cell(i, j))

        # TODO: clean this sh*t
        for a in self.forklifts:
            for p in self.products:
              pair = Pair(a, p)
              
              # gets the index of future appended pair
              index_pair = len(self.pairs)
              self.pairs.append(pair)
              self.pairsDictionary[pair.hash] = index_pair
                

        for i in range(len(self.products) - 1):
            for j in range(i + 1, len(self.products)):
              pair = Pair(self.products[i], self.products[j])
              index_pair = len(self.pairs)
              self.pairs.append(pair)
              self.pairsDictionary[pair.hash] = index_pair

        for p in self.products:
          pair  = Pair(p, self.exit)
          index_pair = len(self.pairs)
          self.pairs.append(pair)
          self.pairsDictionary[pair.hash] = index_pair

        for a in self.forklifts:
          pair = Pair(a, self.exit)
          index_pair = len(self.pairs)
          self.pairs.append(pair )
          self.pairsDictionary[pair.hash] = index_pair

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

