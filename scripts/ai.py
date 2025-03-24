import random
import copy


class AI:
    def __init__(self, game_scene, data):
        self.game = game_scene
        self.data = data

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

        self.ship_under_attack = []
        self.first_ship_in_chain = []

        self.attack_offsets = [[0, 1], [0, -1], [1, 0], [-1, 0]]
        self.current_attack_offsets = [[0, 1], [0, -1], [1, 0], [-1, 0]]

    def reset(self):
        self.grid = [ ["[ ]" for j in range(10)] for i in range(10)]

        self.building_ships = [[[0, 0],], [[0, 0],], [[0, 0],], [[0, 0],],
                        [[0, 0], [0, 1]], [[0, 0], [0, 1]], [[0, 0], [0, 1]],
                        [[0, 0], [0, 1], [0, 2]], [[0, 0], [0, 1], [0, 2]], 
                        [[0, 0], [0, 1], [0, 2], [0, 3]]]
        
        self.init_ships = []
        self.ships = []

        self.ship_under_attack = []
        self.first_ship_in_chain = []

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
                if 0 <= x < 10 and 0 <= y < 10 and self.grid[y][x] == self.data.ship_marker:
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
                        self.grid[pos[1]][pos[0]] = self.data.ship_marker

                    self.ships.append(temp_ship)

                    self.building_ships.remove(self.building_ships[-1])

                    ship_placed = True
        self.init_ships = copy.deepcopy(self.ships)

    def attack(self, player_grid, ships_collection, init_ships_collection):
        if self.ship_under_attack:
            while True:
                random.shuffle(self.current_attack_offsets)
                for offset in self.current_attack_offsets:
                    x = self.ship_under_attack[0] + offset[0]
                    y = self.ship_under_attack[1] + offset[1]
                    if 0 <= x <= 9 and 0 <= y <= 9:
                        if player_grid[y][x] == self.data.ship_marker:
                            player_grid[y][x] = self.data.hit_marker
                            res = self.game.ship_destroyed(x, y, ships_collection, init_ships_collection)
                            if res:
                                self.game.destroy_ship(player_grid, res)
                                self.ship_under_attack = []
                                self.current_attack_offsets = copy.deepcopy(self.attack_offsets)
                                return "Destroyed!"
                            self.current_attack_offsets = [offset]
                            self.ship_under_attack = [x, y]
                            return "Hit!"
                        elif player_grid[y][x] == "[ ]":
                            player_grid[y][x] = self.data.miss_marker
                            return "Miss!"
                self.current_attack_offsets[0][0] = -self.current_attack_offsets[0][0]
                self.current_attack_offsets[0][1] = -self.current_attack_offsets[0][1]
                self.ship_under_attack = copy.deepcopy(self.first_ship_in_chain)
                break
        else:
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                if player_grid[y][x] != self.data.miss_marker and player_grid[y][x] != self.data.hit_marker and player_grid[y][x] != self.data.destroyed_marker:
                    if player_grid[y][x] == self.data.ship_marker:
                        player_grid[y][x] = self.data.hit_marker
                        res = self.game.ship_destroyed(x, y, ships_collection, init_ships_collection)
                        if res:
                            self.game.destroy_ship(player_grid, res)
                            return "Destroyed!"
                        self.ship_under_attack = [x, y]
                        self.first_ship_in_chain = [x, y]
                        return "Hit!"
                    else:
                        player_grid[y][x] = self.data.miss_marker
                        return "Miss!"
