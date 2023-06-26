
from agentsearch.action import Action
from warehouse.warehouse_state import WarehouseState
from warehouse.cell import Cell



class ActionDown(Action[WarehouseState]):

    def __init__(self):
        Action.__init__(self, 1)

    def execute(self, state: WarehouseState) -> None:
        state.move_down()
        state.action = self

    def is_valid(self, state: WarehouseState) -> bool:
        return state.can_move_down()
    def rev_action(self, cell: Cell) -> Cell:
        return Cell(cell.line - 1, cell.column)
    def __str__(self):
        return "DOWN"
  
class ActionUp(Action[WarehouseState]):

    def __init__(self):
        Action.__init__(self, 1)

    def execute(self, state: WarehouseState) -> None:
        state.move_up()
        state.action = self

    def is_valid(self, state: WarehouseState) -> bool:
        return state.can_move_up()
         
    
    def rev_action(self, cell: Cell) -> Cell:
        return Cell(cell.line + 1, cell.column)

    def __str__(self):
        return "UP"
class ActionRight(Action[WarehouseState]):

    def __init__(self):
        Action.__init__(self, 1)

    def execute(self, state: WarehouseState) -> None:
        state.move_right()
        state.action = self

    def is_valid(self, state: WarehouseState) -> bool:
        return state.can_move_right()

    def rev_action(self, cell: Cell) -> Cell:
        return Cell(cell.line, cell.column - 1)
    def __str__(self):
        return "RIGHT"
        
class ActionLeft(Action[WarehouseState]):

    def __init__(self):
        Action.__init__(self, 1)

    def execute(self, state: WarehouseState) -> None:
        state.move_left()
        state.action = self

    def is_valid(self, state: WarehouseState) -> bool:
        return state.can_move_left()

    def rev_action(self, cell: Cell) -> Cell:
        return Cell(cell.line, cell.column + 1)

    def __str__(self):
        return "LEFT"
    



    
    




    