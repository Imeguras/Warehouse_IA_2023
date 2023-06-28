import math

from agentsearch.heuristic import Heuristic
from warehouse.warehouse_problemforSearch import WarehouseProblemSearch
from warehouse.warehouse_state import WarehouseState


class HeuristicWarehouse(Heuristic[WarehouseProblemSearch, WarehouseState]):

    def __init__(self):
        super().__init__()

    def compute(self, state: WarehouseState) -> float:
        goal = self.problem.goal_position
        h = math.sqrt((state.cell_forklift.line - goal.line)**2 + (state.cell_forklift.column - goal.column)**2)
        return h

    def __str__(self):
        return "Euclidian Distance Heuristic"

