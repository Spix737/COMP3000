class Board:
    def __init__(self):
        board = [[]] * 182
        # 16
        # 16
            # 19
            # 19
                # 21
                # 21
                # 21
            # 19
            # 19
        # 16
        # 16

    vertices = [
        0,2,4,6,8,10,12, #1top
        26,28,30,32,34,36,38,40,42, #2top, 1bot
        60,62,64,66,68,70,72,74,76,78,80, #3top, 2bot
        102,104,106,108,110,112,114,116,118,120,122, #4top, 3bot
        140,142,144,146,148,150,152,154,156,158, #5top, 4bot
        170,172,174,176,178,180,182 #5bot
        ]
    
    # array of values which award a resource when rolled
    probability_array = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]

    # array of terrain which correspond to the resource types in game
    # crop fields = c forests = f, mountains = m, hills = h, pasture = p, dessert = X
    terrain_array = [
        'c','c','c','c',
        'f','f','f','f',
        'm','m','m','m',
        'h','h','h',
        'p','p','p',
        'X']

    edges = [
        1,3,5,7,9,11,
        13,17,21,25, #tileRow1
        27,29,31,33,35,37,39,41, 
        43,47,51,55,59, #tileRow2
        61,63,65,67,69,71,72,73,75,77,79,
        81,85,89,93,97,101, #tileRow3
        103,105,107,109,111,113,115,117,119,
        123,127,131,135,139, #tileRow4
        141,143,145,147,149,151,153,155,
        157,161,165,169, #tileRow5
        171,173,175,177,179,181
    ]

    #to traverse to other hexes, add 4 * number of hexes to traverse to each value
    first_hex = [0, 1, 2, 3, 4,
                13,14,15,16,17,
                28,29,30,31,32]
        
