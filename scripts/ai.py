import random


class AI:
    def __init__(self):
        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.building_ships = [([0, 0],), ([0, 0],), ([0, 0],), ([0, 0],),
                        ([0, 0], [0, 1]), ([0, 0], [0, 1]), ([0, 0], [0, 1]),
                        ([0, 0], [0, 1], [0, 2]), ([0, 0], [0, 1], [0, 2]), 
                        ([0, 0], [0, 1], [0, 2], [0, 3])]

        self.offsets = [(0, 0), (1, 1), (1, 0),
                        (1, -1), (0, -1), (-1, -1),
                        (-1, 0), (-1, 1), (0, 1)]
        
    def rotate_ship(self, ship):
        ship_orientation = self.find_ship_orientation(self.building_ships[-1])
        if ship_orientation != "Centered":
            if ship_orientation == "Vertical":
                i = ship[0][0]
                for pos in ship[1:]:
                    i += 1
                    pos[0], pos[1] = i, ship[0][1]

                if ship[-1][0] > 9:
                    offset = ship[-1][0] - 9

                    for pos in ship:
                        pos[0] -= offset
            else:
                i = ship[0][1]
                for pos in ship[1:]:
                    i += 1
                    pos[0], pos[1] = ship[0][0], i
                
                if ship[-1][1] > 9:
                    offset = ship[-1][1] - 9

                    for pos in ship:
                        pos[1] -= offset
    
    def find_ship_orientation(self, ship):
        if len(ship) == 1:
            return "Centered"
        
        if ship[1][0] > ship[0][0]:
            return "Horizontal"
        if ship[1][1] > ship[0][1]:
            return "Vertical"

    def place_ships(self):
        ship = self.building_ships[-1]
        rotate = random.choice([True, False])

        if rotate:
            self.rotate_ship(ship)
        
        ship_orientation = self.find_ship_orientation(ship)

        if ship_orientation == "Vertical":
            x_move = random.randint(0, 9)
            y_move = random.randint(0, 10 - len(ship))
            for pos in ship:
                pos[0] += x_move
                pos[1] += y_move
        else:
            x_move = random.randint(0, 10 - len(ship))
            y_move = random.randint(0, 9)
            for pos in ship:
                pos[0] += x_move
                pos[1] += y_move

        for pos in ship:
            self.grid[pos[1]][pos[0]] = "[@]"
        self.building_ships.remove(ship)
        

ai = AI()
ai.place_ships()
for row in ai.grid:
    print(row)
