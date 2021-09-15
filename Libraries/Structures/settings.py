
CLEARED_ROW_INDEX       = 0
MAX_COLUMN_INDEX        = 1
SUM_HEIGHT_INDEX        = 2
SUM_HOLES_INDEX         = 3
AVG_HEIGHT_INDEX        = 4
BUMPINESS_INDEX         = 5
BIG_WHEEL_INDEX         = 6
H_TRANSITIONS_INDEX     = 7
V_TRANSITIONS_INDEX     = 8
FULL_SQUARES_INDEX      = 9
DIFF_COLUMN_INDEX       = 10
SUM_WHEELS_INDEX        = 11
MIN_COLUMN_INDEX        = 12
SUM_HOLES2_INDEX        = 13
BUMPINESS_HEIGHT_INDEX  = 14
TETRIMINO_POSITION      = 15

HEURYSTIC_LIST = [
    [ False, 1 ], #clearedRow
    [ True, -1 ], #maxColumn
    [ True, -1 ], #sumHeight
    [ True, -1 ], #sumHoles
    [ True, -1 ], #avgHeight
    [ True, -1 ], #bumpiness
    [ True, -1 ], #biggestWheel
    [ True, -1 ], #hTransitions
    [ True, -1 ], #vTransitions
    [ True, -1 ], #fullSquares
    [ True, -1 ], #sumWheel
    [ True, -1 ], #diffColumn
    [ True, -1 ], #minColumn
    [ True, -1 ], #sumHoles2
    [ True, -1 ], #bumpinessHeight
]

class Params:
    MAX_POINTS                 = 0
    NUMBER_OF_GAMES            = 0
    GENERATOR                  = 0
    HEURYSTIC_AMOUNT           = 0
    HEURYSTIC                  = []

    POPULATION_SIZE            = 0
    MUTATION_RATE              = 0
    ELITARY_SELECT             = 0
    PARENTS_SELECT             = 0
    REPLACE_IN_POPULATION_TYPE = 0
    SELECTION_TYPE             = 0
    LIMIT_NOT_IMPROVE          = 0

    SELECTION_LIMIT            = 0
    RANKING_RATE               = 0

    C1                         = 0
    C2                         = 0
    W                          = 0

    NET_CONFIGURATION          = []
    NET_OPTIMIZERS             = []
    LOSS                       = ""
    BACH_SIZE                  = 0
    OPTIMIZER                  = ""
    EPOCH                      = 0

    LEARNING_STATUS            = ""

    def set_up(self, line) : 
        tab = line.replace(" ","").split(",")

        self.MAX_POINTS                 = int(tab[3])
        self.NUMBER_OF_GAMES            = int(tab[4])
        self.GENERATOR                  = int(tab[5])

        if int(tab[2]) == 0:
            self.POPULATION_SIZE            = int(tab[6])
            self.MUTATION_RATE              = int(tab[7])
            self.ELITARY_SELECT             = int(tab[8])
            self.PARENTS_SELECT             = int(tab[9])
            self.REPLACE_IN_POPULATION_TYPE = int(tab[10])
            self.SELECTION_TYPE             = int(tab[11])
            if(self.SELECTION_TYPE == 1):
                self.SELECTION_LIMIT        = int(tab[16])
                self.RANKING_RATE           = float(tab[17])
            if(self.SELECTION_TYPE == 2):
                self.SELECTION_LIMIT        = int(tab[16])

            self.LIMIT_NOT_IMPROVE          = int(tab[12])

        if int(tab[2]) == 1:
            self.POPULATION_SIZE            = int(tab[6])
            self.C1                         = float(tab[13])
            self.C2                         = float(tab[14])
            self.W                          = float(tab[15])
            self.LIMIT_NOT_IMPROVE          = int(tab[12])

        if int(tab[2]) == 2 or int(tab[2]) == 3 :
            tab2 = tab[6].split(":")
            tab2 = tab2[1:len(tab2)-1]
            
            self.NET_CONFIGURATION = []
            for tak in range(len(tab2)):
                #print(tak, tab2[tak])
                self.NET_CONFIGURATION.append(int(tab2[tak]))

            tab2 = tab[7].split(":")
            tab2 = tab2[1:len(tab2)-1]
            
            self.NET_OPTIMIZERS = []
            for tak in range(len(tab2)):
                #print(tak, tab2[tak])
                self.NET_OPTIMIZERS.append(tab2[tak])

            self.LOSS = tab[8]
            self.OPTIMIZER = tab[9]
            self.BACH_SIZE = int(tab[10])
            self.EPOCH     = int(tab[11])

        tab2 = tab[1].split(":")
        tab2 = tab2[1:len(tab2)-1]
        
        self.HEURYSTIC = []
        for tak in range(len(tab2)):
            #print(tak, tab2[tak])
            self.HEURYSTIC.append(int(tab2[tak]))

        self.HEURYSTIC_AMOUNT           = len(tab2)
        return int(tab[2])


PARAMS = Params()

