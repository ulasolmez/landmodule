
class ArrayStack:
    def __init__(self):
        self._data = []
    def __len__(self):
        return len(self._data)
    def is_empty(self):
        return len(self._data) == 0
    def push(self,e):
        self._data.append(e)
    def top(self):
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data[-1]
    def pop(self):
        if self.is_empty():
            raise Empty("Stack is empty")
        return self._data.pop() 
class Empty(Exception):
    pass

class Land:
    def __init__(self, land_list):
        self.land_list = land_list
        self.land_structure_validator(land_list)

    def land_structure_rules(self, land_list):

        for i in range(len(land_list)):
            if not (isinstance(land_list[i], list) and len(land_list[i]) > 3 and len(land_list) > 3 and len(land_list[i]) == len(land_list[i-1])):
                return False
            for j in range(len(land_list[i])):
                if not (isinstance(land_list[i][j], str) and len(land_list[i][j]) == 1 and land_list[i][j] in ('0', '1')):
                    return False
        return True

    def land_structure_validator(self, land_list):
        if self.land_structure_rules(land_list):
            pass
        else:
            raise InvalidLandException
    def get_start(self):
        return (0,0)    

class InvalidLandException(Exception):
    pass

class IslandFinder:

    def __init__(self,path):
        
        self._land = self.text_to_array(path)
        self._cellstack = ArrayStack()
        self._explored = []

    def text_to_array(self,path):
        
        path_file = open(path,"r")
        
        land_array = [list(line.strip()) for line in path_file] #one line of code that converts the string file into list of lists.
        
        return Land(land_array)
    

    
    """def get_a_neighbor(self,a_tuple):
        row_index, column_index = a_tuple
        neighbors = [(row_index-1,column_index),(row_index,column_index-1),(row_index,column_index+1),(row_index+1,column_index)]
        m = len(self._land.land_list)
        n = len(self._land.land_list[0])
        for neighbor in neighbors:
            if 0 <= neighbor[0] < m and 0 <= neighbor[1] < n: 
                if self._land.land_list[neighbor[0]][neighbor[1]] == '1' and neighbor not in self._explored:
                    
                    
        return False   """

    def binary_insert_explored(self, cell): #binary insert algorithm behaving similar to binary search instead it is inserting tuples into our list without breaking the order.
        if len(self._explored) == 0:
            self._explored.append(cell)
        elif len(self._explored) == 1:
            if self._explored[0] < cell:
                self._explored.append(cell)
            else:
                self._explored = [cell] + self._explored    
        else:
            left = 0 
            right = len(self._explored) - 1
            while left <= right:
                mid = (left + right) // 2
                if self._explored[mid] <= cell <= self._explored[mid+1]:
                    self._explored.insert(mid+1,cell)
                    return self._explored
                elif self._explored[mid+1] < cell:
                    left = mid + 1
                elif self._explored[mid] > cell:
                    right = mid - 1 
                if self._explored[0] > cell:                        # handling edge cases
                    self._explored = [cell] + self._explored
                if self._explored[-1] < cell:
                    self._explored.append(cell)            

    def binary_search_explored(self, element):
        low = 0
        high = len(self._explored) - 1

        while low <= high:
            mid = (low + high) // 2
            mid_element = self._explored[mid]

            if mid_element == element:
                return True
            elif mid_element < element:
                low = mid + 1
            else:
                high = mid - 1

        return False
  
    def get_a_neighbor(self, current_cell):
        row_index, column_index = current_cell
        m, n = len(self._land.land_list), len(self._land.land_list[0])
        _area = 0

        if 0 <= row_index < m and 0 <= column_index < n and self._land.land_list[row_index][column_index] == '1' and current_cell not in self._explored:
            self.binary_insert_explored(current_cell)
            _area += 1
            neighbors = [
                (row_index - 1, column_index),
                (row_index, column_index - 1),
                (row_index, column_index + 1),
                (row_index + 1, column_index),
            ]

            for neighbor in neighbors:
                _area += self.get_a_neighbor(neighbor) #recursive dfs algorithm that searches through all connected neigbours and backtracks to find the max area.

        return _area

    def find_island(self):
        self._cellstack = ArrayStack()
        self._explored = []
        _maxArea = 0

        for i in range(len(self._land.land_list)):
            for j in range(len(self._land.land_list[0])):
                cell_coord = (i, j)
                if self._land.land_list[i][j] == '1' and cell_coord not in self._explored:
                    _area = self.get_a_neighbor(cell_coord)
                    _maxArea = max(_area, _maxArea)
        print(_maxArea)
        print(f"{_maxArea} is maximum island")
        return _maxArea
    
    
    """def find_island(self):
            self._cellstack = ArrayStack()
            self._explored = []
            _maxArea = 0
            for i in range(len(self._land.land_list)):
                for j in range(len(self._land.land_list[0])):
                    cell_coord = (i,j)
                    if self._land.land_list[i][j] == '1' and self.binary_search_explored(cell_coord) == False:
                        self._cellstack.push(cell_coord)
                        _area = 0 
                        while not self._cellstack.is_empty():
                            c = self._cellstack.top()
                            if not self.binary_search_explored(c):
                    
                                self.binary_insert_explored(c)
                                _area += 1
                                unvisited_neighbor = self.get_a_neighbor(c)
                                if unvisited_neighbor:
                                    self._cellstack.push(unvisited_neighbor)
                                else:
                                    self._cellstack.pop()    
                            else:
                                self._cellstack.pop()
                        _maxArea = max(_maxArea,_area)
            print(_maxArea)
            return _maxArea                            """