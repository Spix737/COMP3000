class Board:
    def __init__(self):
        self.board = [[]] * 183
        # 13
        # 13
            # 17
            # 17
                # 21
                # 21
                # 21
            # 17
            # 17
        # 13
        # 13

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
        ]
        # 'X']
    
    desert_coord = -1

    vertices = [
        0,2,4,6,8,10,12, #1top
        26,28,30,32,34,36,38,40,42, #2top, 1bot
        60,62,64,66,68,70,72,74,76,78,80, #3top, 2bot
        102,104,106,108,110,112,114,116,118,120,122, #4top, 3bot
        140,142,144,146,148,150,152,154,156, #5top, 4bot
        170,172,174,176,178,180,182 #5bot
        ] #54 vertices?

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

    tile_value_left = [
            14,18,22, #tileRow1
          44,48,52,56, #tileRow2
        82,86,90,94,98, #tileRow3
          124,128,132,136, #tileRow4
            158,162,166 #tileRow5
    ]

    tile_types_center = [
            15,19,23, #tileRow1
          45,49,53,57, #tileRow2
        83,87,91,95,99, #tileRow3
          125,129,133,137, #tileRow4
           159,163,167 #tileRow5
    ]

    is_robber_right = [
            16,20,24, #tileRow1
          46,50,54,58, #tileRow2
        84,88,92,96,100, #tileRow3
          126,130,134,138, #tileRow4
            160,164,168 #tileRow5
    ]

    current_robber_pos = 0

    #to traverse to other hexes, add 4 * number of hexes to traverse to each value
    first_hex = [0, 1, 2, 3, 4,
                13,14,15,16,17,
                28,29,30,31,32]
        
    perimeter_vertices = [
        0,2,4,6,8,10,12, #1top
        26,28,30,32,34,36,38,40,42, #2top, 1bot
        60,62,64,66,68,70,72,74,76,78,80, #3top, 2bot
        102,104,106,108,110,112,114,116,118,120,122, #4top, 3bot
        140,142,144,146,148,150,152,154,156, #5top, 4bot
        170,172,174,176,178,180,182 #5bot
        ]
    
    ports_vertices = [
        0,2,
        6,8,
        26,62,
        40,42,
        80,122,
        104,140,
        154,156,
        170,172,
        176,178
    ]

    port_types = [
        'wh',
        'wo',
        'or',
        'cl',
        'sh',
        '3',
        '3',
        '3',
        '3',
    ]

    # port map dict
    # object that holds each port type for each port vertex
    # OR object that holds each vertex pair for each port
    

    def display_board(self):
        '''display the board intuitively'''
        # print(self.board[0:13])
        print(self.board[13:26])
        # print(self.board[26:43])
        print(self.board[43:60])
        # print(self.board[60:81])
        print(self.board[81:102])
        # print(self.board[102:123])
        print(self.board[123:140])
        # print(self.board[140:157])
        print(self.board[157:174])
        # print(self.board[174:183])
    