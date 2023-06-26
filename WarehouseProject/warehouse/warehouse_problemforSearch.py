
import copy
import math
from agentsearch.problem import Problem
from warehouse.actions import *
from warehouse.cell import Cell
from warehouse.warehouse_state import WarehouseState


class WarehouseProblemSearch(Problem[WarehouseState]):
    
    def __init__(self, initial_state: WarehouseState, goal_position: Cell):
        super().__init__(initial_state)
        self.actions = [ActionDown(), ActionUp(), ActionRight(), ActionLeft()]
        self.goal_position = goal_position
       
    def get_actions(self, state: WarehouseState) -> list:
        valid_actions = []
        for action in self.actions:
            if action.is_valid(state):
                valid_actions.append(action)
        return valid_actions

    def get_successor(self, state: WarehouseState, action: Action) -> WarehouseState:
       
        successor = copy.deepcopy(state)
        action.execute(successor)
        return successor

  

    def is_goal(self, state: WarehouseState) -> bool:
      # if the agent is adjacent to the goal return true 
      # check euclidean distance and see if its equal or smaller than 1
      euclidean_distance = math.sqrt(pow(state.cell_forklift.line - self.goal_position.line,2) + pow(state.cell_forklift.column - self.goal_position.column,2) )
      if euclidean_distance <=1:
        return True
      return False

