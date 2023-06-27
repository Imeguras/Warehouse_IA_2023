import numpy as np
from PIL.ImageEnhance import Color
from numpy import ndarray
from collections import defaultdict
import constants
from agentsearch.state import State
from agentsearch.action import Action
from warehouse.cell import Cell




class WarehouseState(State[Action]):
    
    
    def __init__(self, matrix: ndarray, rows, columns, cell_forklift=Cell(0,0)):
        super().__init__()
        
        self.rows = rows
        self.columns = columns
        self.products = []
        self.cell_forklift = cell_forklift

        #this one is just to make the products array start at index 1
        self.products.append(Cell(0,0))
        self.matrix = np.full([self.rows, self.columns], fill_value=0, dtype=int)
      
        for i in range(self.rows):
          for j in range(self.columns):
                self.matrix[i][j] = matrix[i][j]
                if self.matrix[i][j] == constants.PRODUCT:
                  self.products.append(Cell(i, j)) 
                if self.matrix[i][j] == constants.FORKLIFT:
                  if cell_forklift.line == 0 and cell_forklift.column == 0: 
                    self.cell_forklift = Cell(i, j)

                if self.matrix[i][j] == constants.EXIT:
                    self.line_exit = i
                    self.column_exit = j
                
                  
    

    #@cached(max_size=1024)
    #checks if a robot can go to a certain position
    def is_passageway(self, x, y) -> bool: 
      point = self.matrix[x][y]
      if(point is not None and (point == constants.FORKLIFT or  point == constants.EMPTY)):
        return True
      return False

    #Great Language Moment: cant even method overload...    
    def is_passageway_(self, cell: Cell)-> bool:
      return self.is_passageway(cell.line, cell.column)
    def overflows(self, x, y) -> bool:
      if x < 0 or x >= self.rows or y < 0 or y >= self.columns:
        return True
      return False
      
    def overflows_ (self, cell: Cell) -> bool:
      return self.overflows(cell.line, cell.column)

    def can_move_down(self) -> bool:
      _is_passageway= lambda: self.is_passageway(self.cell_forklift.line + 1, self.cell_forklift.column)
      if self.cell_forklift.line + 1 < self.rows and _is_passageway() : 
        return True 
      return False

    def can_move_up(self) -> bool:
      _is_passageway= lambda: self.is_passageway(self.cell_forklift.line - 1, self.cell_forklift.column)
      if self.cell_forklift.line - 1 >= 0 and _is_passageway() : 
        return True 
      return False

   
    
    def can_move_right(self) -> bool:
      _is_passageway = lambda: self.is_passageway(self.cell_forklift.line , self.cell_forklift.column + 1) 
      if self.cell_forklift.column + 1 < self.columns and _is_passageway(): 
        return True 
      return False

    def can_move_left(self) -> bool:
      _is_passageway = lambda: self.is_passageway(self.cell_forklift.line, self.cell_forklift.column - 1)
      if self.cell_forklift.column - 1 >= 0 and _is_passageway(): 
        return True 
      return False
    #this tipically should be used with forklifts
    def move_object(self, x, y, x1, y1): 
      #this will need to change in case of colisions 
      previousOcuppier = self.matrix[x][y]
      self.matrix[x][y] = constants.EMPTY
      self.matrix[x1][y1]= previousOcuppier
      if self.matrix[x1][y1] == constants.FORKLIFT:
        self.cell_forklift.line = x1
        self.cell_forklift.column = y1

    def move_down(self) -> None:
      if self.can_move_down():
        axis = self.cell_forklift.line + 1
        self.move_object(self.cell_forklift.line,self.cell_forklift.column, axis, self.cell_forklift.column)


    def move_up(self) -> None:
      if self.can_move_up():
        axis = self.cell_forklift.line -1
        self.move_object(self.cell_forklift.line,self.cell_forklift.column, axis,self.cell_forklift.column)
        

   
    def move_right(self) -> None:
      if self.can_move_right():
        axis = self.cell_forklift.column + 1
        self.move_object(self.cell_forklift.line,self.cell_forklift.column, self.cell_forklift.line, axis)

    def move_left(self) -> None:
      if self.can_move_left(): 
        axis = self.cell_forklift.column - 1
        self.move_object(self.cell_forklift.line,self.cell_forklift.column, self.cell_forklift.line , axis)

    def get_cell_color(self, row: int, column: int) -> Color:
        if row == self.line_exit and column == self.column_exit and (
                row != self.cell_forklift.line or column != self.cell_forklift.column):
            return constants.COLOREXIT

        if self.matrix[row][column] == constants.PRODUCT_CATCH:
            return constants.COLORSHELFPRODUCTCATCH

        if self.matrix[row][column] == constants.PRODUCT:
            return constants.COLORSHELFPRODUCT

        switcher = {
            constants.FORKLIFT: constants.COLORFORKLIFT,
            constants.SHELF: constants.COLORSHELF,
            constants.EMPTY: constants.COLOREMPTY
        }
        return switcher.get(self.matrix[row][column], constants.COLOREMPTY)

    def __str__(self):
        matrix_string = str(self.rows) + " " + str(self.columns) + "\n"
        for row in self.matrix:
            for column in row:
                matrix_string += str(column) + " "
            matrix_string += "\n"
        return matrix_string

    def __eq__(self, other):
        if isinstance(other, WarehouseState):
            return np.array_equal(self.matrix, other.matrix)
        return NotImplemented

    # def __deepcopy__(self, memo={}):
    #   constSizeMax=25
    #   if self in memo:
    #     print("cache hit")
    #     return memo[self]
    #   else:

    #     new_state = WarehouseState(self.matrix, self.rows, self.columns, self.cell_forklift)
    #     if len(memo) < constSizeMax:
    #       memo[self] = new_state
    #     # TODO: seria engraçado implementar FIFO ou frequencia cache
          
    #     return new_state

    def __hash__(self):
        return hash(self.matrix.tostring())
