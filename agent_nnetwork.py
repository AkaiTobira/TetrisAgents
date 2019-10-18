
from neural_network import NeuralNetwork
from tetiomers      import O,L,N,Z,T,I,J
from consts         import get_color, Colors

class NeuralNetworkAi:
    nn = None

    def __init__(self):
        self.nn = NeuralNetwork( 227, 4, 300, 32)

    def __convert_tetromino_to_array(self, tetromino):
        if type(tetromino) == O : return [1,0,0,0,0,0,0]
        if type(tetromino) == L : return [0,1,0,0,0,0,0]
        if type(tetromino) == J : return [0,0,1,0,0,0,0]
        if type(tetromino) == N : return [0,0,0,1,0,0,0]
        if type(tetromino) == Z : return [0,0,0,0,1,0,0]
        if type(tetromino) == T : return [0,0,0,0,0,1,0]
        if type(tetromino) == I : return [0,0,0,0,0,0,1]

    def __convert_grid_to_binary(self, grid):
        binary_grid = []
        for row in grid:
            for cell in row:
                binary_grid.append(0) if cell == get_color(Colors.BLACK) else binary_grid.append(1)
        return binary_grid 

    def __interpret_output(self, tetromino , output):
        best = -1.0
        for i in range( tetromino.max_rotate ):
            rng = tetromino.get_position_range()[1] - tetromino.get_position_range()[0]
            for j in range(rng):
                if output[ i*8 + j ] > best:
                    best = output[ i*8 + j ]
                    while( tetromino.current_rotate != i): tetromino.rotate_left()
                    tetromino.position = [ j + tetromino.get_position_range()[0], tetromino.position[1] ]

    def select_bestMove(self, tetromino, grid ) : 
    #    print(  self.__convert_grid_to_binary(grid) + self.__convert_tetromino_to_array(tetromino)  )
        self.__interpret_output( tetromino, self.nn.fit( self.__convert_grid_to_binary(grid) + self.__convert_tetromino_to_array(tetromino) ) )
        return 0

    def set_score(self, score, number_of_tetrominos): 
        error =  100 - (number_of_tetrominos/5)
        learning_rate = 0.001
        Q = 1/2 * error * error


from alg_nevolution import NeuralEvolution

class NeuralEvolutionAi:
    ne = None
    current_net = None
    
    def __init__(self):
        self.ne = NeuralEvolution()
        self.current_net = self.ne.get_next_active()

    def __convert_tetromino_to_array(self, tetromino):
        if type(tetromino) == O : return [1,0,0,0,0,0,0]
        if type(tetromino) == L : return [0,1,0,0,0,0,0]
        if type(tetromino) == J : return [0,0,1,0,0,0,0]
        if type(tetromino) == N : return [0,0,0,1,0,0,0]
        if type(tetromino) == Z : return [0,0,0,0,1,0,0]
        if type(tetromino) == T : return [0,0,0,0,0,1,0]
        if type(tetromino) == I : return [0,0,0,0,0,0,1]

    def __convert_grid_to_binary(self, grid):
        binary_grid = []
        for row in grid:
            for cell in row:
                binary_grid.append(0) if cell == get_color(Colors.BLACK) else binary_grid.append(1)
        return binary_grid 

    def __interpret_output(self, tetromino , output):
        best = -1.0
        for i in range( tetromino.max_rotate ):
            rng = tetromino.get_position_range()[1] - tetromino.get_position_range()[0]
            for j in range(rng):
                if output[ i*8 + j ] > best:
                    best = output[ i*8 + j ]
                    while( tetromino.current_rotate != i): tetromino.rotate_left()
                    tetromino.position = [ j + tetromino.get_position_range()[0], tetromino.position[1] ]

    def select_bestMove(self, tetromino, grid ) :
        enviroment = self.__convert_grid_to_binary(grid) + self.__convert_tetromino_to_array(tetromino)        
        self.__interpret_output( tetromino, self.current_net.fit( enviroment ) )

    def return_score(self, score, number_of_tetrominos):
        self.ne.add_score(score, number_of_tetrominos)
        self.current_net = self.ne.get_next_active()