import math
from random import uniform, randint

class Matrix:

    _r = 0
    _c = 0
    m = []

    def __init__( self, column, rows):
        self._r = rows
        self._c = column
        self.m = []

        for i in range( self._r ):
            self.m.append([])
            for j in range( self._c ): self.m[i].append(0)

    def __repr__( self ):
        to_string = "|"
        for i in range( self._r):
            for j in range( self._c ):
                to_string +=  str(self.m[i][j])[:5] + ", "
            to_string =  to_string[0:len(to_string)-2] + "|\n|"
        to_string = to_string[0:len(to_string)-2]
        return to_string

    def rand( self ):
        for i in range( self._r ):
            for j in range( self._c):
                self.m[i][j] = uniform(-1, 1)
                if j == self._c-1: self.m[i][j] = 1
        
    def copy(self):
        new_m = Matrix(self._c, self._r)
        new_m.m = self.m.copy()
        return new_m

    def get_row(self, row):
        return self.m[row]

    def get_column( self, column):
        col = []
        for i in range( self._r ): col.append(self.m[i][column])
        return col

    def __add__(self, m):
        if type(m) == Matrix: return self._matrix_sum(m)
        if type(m) == float : return self._number_sum(m)
        return self

    def __mul__(self, m):
        if type(m) == Matrix: return self._matrix_mul(m)
        if type(m) == float : return self._number_mul(m)
        return self

    def _matrix_mul(self, m):
        new_m = Matrix( self._r, self._c)
        for i in range( self._r):
            for j in range( self._c):
                new_m.m[i][j] = self.m[i][j] * m.m[i][j]
        return new_m

    def _number_mul(self, m):
        new_m = Matrix( self._r, self._c)
        for i in range( self._r):
            for j in range( self._c):
                new_m.m[i][j] = self.m[i][j] * m
        return new_m

    def _matrix_sum(self, m):
        new_m = Matrix( self._r, self._c)
        for i in range( self._r):
            for j in range( self._c):
                new_m.m[i][j] = self.m[i][j] + m.m[i][j]
        return new_m

    def _number_sum(self, m):
        new_m = Matrix( self._r, self._c)
        for i in range( self._r):
            for j in range( self._c):
                new_m.m[i][j] = self.m[i][j] + m
        return new_m 

    def mutate(self, rate):
        for i in range( self._r ):
            for j in range( self._c):
                if uniform(0,1) < rate : self.m[i][j] = uniform(-1, 1)

class NeuralNetwork:
    layers = []
    numb_layers = 0

    def __init__(self, input_size, hiden_layers, hiden_layers_size, output_size ):
        self.layers = []
        self.numb_layers = hiden_layers
        self.layers.append( NeuralNetworkLayer( input_size + 1, hiden_layers_size ) )
        for i in range(self.numb_layers - 1): self.layers.append( NeuralNetworkLayer( hiden_layers_size + 1, hiden_layers_size) )
        self.layers.append( NeuralNetworkLayer( hiden_layers_size + 1, output_size) )

    def _normalize_input(self, i):
        tre = i.copy()
        nrom = max(tre)
        for i in range(len(tre)):
            tre[i] = tre[i]/nrom
        return tre

    def copy(self):
        new_network = NeuralNetwork(1,len(self.layers)-1,1,1)
        for i in range(len(self.layers)):
            new_network.layers[i] = self.layers[i].copy()
        return new_network 

    def fit(self, incoming):

    #    tre = self._normalize_input(incoming)
        tre = incoming.copy()
        for layer in self.layers:
            out = layer.process(tre)
            tre = out
        return out

    def mutate(self, rate):
        for layer in self.layers:
            layer.mutate(rate) 


    def improve(self, error, output ):
        enda = [0.1, 0.99]
        last_layer = len(self.layers)-1

        for r in range( self.layers[last_layer].weight._r ):
            for c in range( self.layers[last_layer].weight._c ):
                E1 = self.layers[last_layer].m.m[r][c]*output[r]*(1-output[r])*(output[r]-enda[r])
                self.layers[last_layer].weight.m[r][c] = self.layers[last_layer].weight.m[r][c] - 0.5*E1

        last_layer -= 1
        for r in range( self.layers[last_layer].weight._r ):
            for c in range( self.layers[last_layer].weight._c ):
                p = []
                for i in range( self.layers[last_layer].weight._r ):
                    p.append( self.layers[last_layer].m.m[r][c]*output[r]*(1-output[r])*(output[r]-enda[i]) ) 
                self.layers[last_layer].weight.m[r][c] = self.layers[last_layer].weight.m[r][c] - 0.5*sum(p)

class NeuralNetworkLayer:
    weight   = []
    bias     = []
    neuron_v = []
    active_v = []    

    t        = []

    def __init__(self, input_size, output_size):
        self.weight = Matrix(input_size, output_size)
        self.t = [input_size, output_size]
        self.weight.rand()
        self.bias   = 1

    def process(self, inc):
        output = []
        inc.append(self.bias)

        self.m = Matrix(self.weight._c,self.weight._r)

#        print( self.weight._r, self.weight._c, len(inc))

        for r in range( self.weight._r ):
            summ = 0.0
            row = self.weight.get_row(r)
#            print( len(inc), len(row) )
            for i in range( len(inc) ):
                if len( inc  ) != len(row): print( len(inc), len(row), i )
#                self.m.m[r][i] = inc[i]
#                print( "input=",inc[i],"weight=" , row[i],"result=", inc[i] * row[i], "\n" )
                summ += inc[i] * row[i]
            output.append(summ)

    #    self.neuron_v = output
    #    print(" Layer Outpu=", output )
        self.active_v = self.sigmoid_output(output)
    #    print(" Layer Activ=", self.active_v )

        return self.active_v

    def mutate( self, rate):
#        print( self.weight._r, self.weight._c)
        self.weight.mutate(rate)

    def copy(self):
    #    print( self.t[0], self.t[1] )
        new_layer = NeuralNetworkLayer( self.t[0], self.t[1])
        new_layer.weight = self.weight.copy()
        new_layer.bias   = float(self.bias)
        return new_layer

    def sigmoid_output(self, tab):
        out = []
        for i in tab: out.append(self.sigmoid(i))
        return out

    def sigmoid(self, x):
        return 1.0/ ( 1.0 + math.exp(-x) ) 

def calc_error( end ):
    enda = [0.01, 0.99]
    e1 = 0.5 *(enda[0] - end[0] )*(enda[0] - end[0])
    e2 = 0.5 *(enda[1] - end[1] )*(enda[1] - end[1])
    et = e1 + e2
    previous_layer = 0
    current_neuron = 0

    delta = nn.layers[previous_layer].active_v[0] * end[current_neuron]*(1-end[current_neuron]) * -( enda[current_neuron] - end[current_neuron])

#    print( "Calculated Error=", delta, " W5=", nn.layers[previous_layer+1].weight.m[0][0] - 0.5 * delta )
    return [e1,e2]

#def calculate_errors(end):pass

#for i in range( 10000 ):
#    out = nn.fit( [0.05, 0.10] )
#    dd  = calc_error(out)
#    nn.improve(dd, out)
#    print( sum(dd) )
#print( nn.layers[1].weight, "\n" )
##print( nn.layers[0].weight, "\n" )


#def crossover( nn1, nn2  )



def layer_crossover( layer1, layer2):
    new_layer = NeuralNetworkLayer( layer1.t[0], layer2.t[1] )
    new_layer.weight = matrix_crossover( layer1.weight, layer2.weight )
    return new_layer

def matrix_crossover( m1, m2):
    new_matrix = Matrix(m1._c, m2._r)

    rand_c = randint(0, m1._c)
    rand_r = randint(0, m2._r)
    for r in range(m2._r):
        for c in range( m1._c):
            if r < rand_r or ( r == rand_r and c <= rand_c ): new_matrix.m[r][c] = m1.m[r][c]
            else: new_matrix.m[r][c] = m2.m[r][c]
    return new_matrix
