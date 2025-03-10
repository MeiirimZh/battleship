import random
import copy


class AI:
    def __init__(self):
        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.building_ships = [[[0, 0],], [[0, 0],], [[0, 0],], [[0, 0],],
                        [[0, 0], [0, 1]], [[0, 0], [0, 1]], [[0, 0], [0, 1]],
                        [[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]], 
                        [[0, 0], [0, 1], [0, 2], [0, 3]]]

        self.offsets = [(0, 1), (1, 0), (0, -1),
                        (-1, 0), (0, 0), (1, 1),
                        (1, -1), (-1, -1), (-1, 1)]
        
        self.init_ships = []
        self.ships = []

        self.ship_under_attack = None
        self.attack_offsets = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        self.current_attack_offsets = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        
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

    def ship_contacts(self, ship):
        for pos in ship:
            for offset in self.offsets:
                x = pos[0] + offset[0]
                y = pos[1] + offset[1]
                if 0 <= x < 10 and 0 <= y < 10 and self.grid[y][x] == "[@]":
                    return True

    def place_ships(self):
        while len(self.building_ships) != 0:
            ship_placed = False
            while not ship_placed:
                temp_ship = copy.deepcopy(self.building_ships[-1])
                rotate = random.choice([True, False])

                if rotate:
                    self.rotate_ship(temp_ship)

                ship_orientation = self.find_ship_orientation(temp_ship)

                if ship_orientation == "Vertical":
                    x_move = random.randint(0, 9)
                    y_move = random.randint(0, 10 - len(temp_ship))
                    for pos in temp_ship:
                        pos[0] += x_move
                        pos[1] += y_move
                else:
                    x_move = random.randint(0, 10 - len(temp_ship))
                    y_move = random.randint(0, 9)
                    for pos in temp_ship:
                        pos[0] += x_move
                        pos[1] += y_move

                if not self.ship_contacts(temp_ship):
                    for pos in temp_ship:
                        self.grid[pos[1]][pos[0]] = "[@]"

                    self.ships.append(temp_ship)

                    self.building_ships.remove(self.building_ships[-1])

                    ship_placed = True
        self.init_ships = copy.deepcopy(self.ships)

    def find_ship(self, x, y):
        for ship in self.init_ships:
            for pos in ship:
                if pos[0] == x and pos[1] == y:
                    return ship

    def ship_destroyed(self, x, y):
        for ship in self.ships:
            for pos in ship:
                if pos[0] == x and pos[1] == y:
                    ship.remove(pos)
                    if len(ship) == 0:
                        return self.find_ship(x, y)

    def attack(self, player_grid):
        if self.ship_under_attack:
            attacked = False
            while not attacked:
                attack_offset = random.choice(self.attack_offsets)
                x, y = attack_offset
                x += self.ship_under_attack[0]
                y += self.ship_under_attack[1]
                if 0 <= x <= 9 and 0 <= y <= 9:
                    if player_grid[y][x] == "[@]":
                        player_grid[y][x] = "[#]"
                        self.ship_under_attack = (x, y)
                        return "Hit!"
                    elif player_grid[y][x] == "[#]" or player_grid[y][x] == "[o]":
                        continue
                    else:
                        self.current_attack_offsets.remove(attack_offset)

                        player_grid[y][x] = "[o]"
                        attacked = True
                        return "Miss"
        else:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if player_grid[y][x] == "[@]":
                player_grid[y][x] = "[#]"
                self.ship_under_attack = (x, y)
                return "Hit!"
            else:
                player_grid[y][x] = "[o]"
                return "Miss!"
