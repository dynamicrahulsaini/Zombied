# todo: documentation
from os import system, name
import re
import time
import pandas as pd
import random
import requests
import pyfiglet


def is_dead(bag):
    """checks if any of the items that the player is carrying can be used to kill the zombie
    :return: False if player has a weapon which can be used to kill the zombie, else returns True
    """
    for x in ['bat', 'glass', 'gun']:
        for y in bag:
            if x == y:
                print("save with the help of  " + y)
                return False
    return True


def clear():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def print_file(file_loc):
    """
    prints the file in proper format according to player location
    :param file_loc: location of the file to be read and printed
    :return: None
    """
    try:
        file = open(file_loc, 'r')
    except FileNotFoundError:
        return
    file = file.readlines()
    for line in file:
        print(line, end='')
    print()


def findIndex(df, to_find, column_name, column_number):
    """
    find all locations of item to be searched in a specific column in a pandas.DataFrame
    
    :param df: dataframe form which the data needs to be read
    :param to_find: the value to search for
    :param column_name: the column of dataframe in which the searching will be done
    :param column_number: total number of columns in the dataframe
    :return: list of indices where the value is found, else returns an empty list
    """
    index_list = []
    for i in range(int(df.size / column_number)):
        if df[column_name][i] == to_find:
            index_list.append(i)
    return index_list


# currency convertor for a puzzle in game which depends on realtime value of a specific currency
class currencyConvertor:
    rate = {}
    API_ACCESS_KEY = '9e73de2326e1968be7acc730c4dbf81f'
    url = str.__add__('http://data.fixer.io/api/latest?access_key=', API_ACCESS_KEY)

    def __init__(self):
        data = requests.get(self.url).json()
        self.rates = data["rates"]

    def convert(self, from_currency, to_currency, amount):
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]
            amount = round(amount * self.rates[to_currency])
            return amount


def locker_puzzle(bag):
    """a locker with a dynamic password"""
    try:
        password = int(input("Enter Password  : "))
    except ValueError:
        print("locked")
        return
    c = currencyConvertor()
    if password == c.convert('USD', 'INR', 20):
        print("unlocked ")
        return 1
    else:
        print("Locked")
        return 0


def decipher_door(bag):
    """simple encryption based puzzle"""

    print("Enter secret key to enter the next room")
    print("Message : " + "A T K K B L")
    password = input("Enter the password: ").lower()
    if password == 'harris':
        print("unlocked!")
        return 1
    else:
        print("Locked")
        return 0

def monty_hall(bag):
    """monty hall problem which will be used as a final challenge to escape the house"""
    
    game_state = 0
    outcomes = [1, 0, 0]
    random.shuffle(outcomes)
    doors = dict(zip(['A', 'B', 'C'], outcomes))
    user_choice = ''
    while user_choice not in doors.keys():
        user_choice = input("Choose the door : ").upper()
        
        # It gives the players one second to make a choice or it will be made for them
        time.sleep(1)
        if user_choice != 'A' and doors['A'] == 0:
            return MontyHall_interior('A', doors, bag)
        elif user_choice != 'B' and doors['B'] == 0:
            return MontyHall_interior('B', doors, bag)
        elif user_choice != 'C' and doors['C'] == 0:
            return MontyHall_interior('C', doors, bag)
        else:
            print("INVALID OPTION!")
    # return game_state

# algorithm for after the first choice 
def MontyHall_interior(option, doors, bag):
    temp = option
    print("OMG!!!! ")
    print("You waited too long to choose....")
    print("Zombie from Door " + option + " JUST walked into the room!\n")
    # kill()
    if is_dead(bag) is False:
        while 1:
            option = input("Think Wisely! Which door you are going with now?  \n").upper()
            if option in doors.keys():
                if option == temp:
                    print(" That door is already opened and it doesnt lead to another room...\n\n")
                else:
                    if doors[option] == 0:
                        print("dead")
                        return 0
                    else:
                        print("entering into another room........")
                        return 1
            else:
                print("Invalid ")
    else:
        return False


def getRoomNumber(location):
    """initiate proper room according to the current location of the player"""
    loc = ord(location) - 97
    print(loc)
    room_n = 0
    if 0 <= loc < 12:
        room_n = loc // 6 + 1
    elif 12 <= loc < 18:
        room_n = 3
    elif 22 <= loc:
        room_n = 4
    elif 18 <= loc < 22:
        room_n = 5
    return room_n

# 
class Room:
    visited = 0
    room = None
    room_number = 1
    i, j, elements = 2, 0, 0
    pos = (0, 0)
    items_in_room = []

    # key: current location, value: (direction in which door is, next location)
    door = {'c': ('a', 's', 5), 'e': ('w', 'h', 2), 'j': ('w', 'm', 3), 'n': ('w', 'w', 4),
            's': ('d', 'c', 1), 'h': ('s', 'e', 1), 'm': ('s', 'j', 2), 'w': ('s', 'n', 3), 'x': ('w', '', 6)}

    # key: current location, value: (direction in which door is, file to be read)
    des = {'f': ('a', 'locker.txt'), 'i': ('a', 'hint.txt'), 'k': ('w', 'sofa.txt'), 'l': ('w', 'table.txt'),
           'u': ('w', 'u.zombie.txt'), 'b': ('s', 'fam.txt')}

    # key: current location, value: function object for the location
    puzzle = {'f': locker_puzzle, 'j': decipher_door, 'n': monty_hall}
    
    # initializing room properly accoring to player location and assigning proper 
    # alphabetical value to each position in the room which represent the location
    # which player can access with total N x M locations available in the room
    def createRoom(self, player_name, location, read=True):
        """get room number and exact coordinates form location alphabet of the player"""

        self.room_number = getRoomNumber(location)
        if 0 < self.room_number < 3:
            self.j = 3
            self.elements = 6 * (self.room_number - 1)
        elif self.room_number == 4:
            self.j = 1
            self.elements = 22
        elif self.room_number == 5:
            self.j = 2
            self.elements = 18
        if self.room_number == 3:
            self.i = 1
            self.j = 2
            self.elements = 12
        else:
            self.i = 2
        locate = ord(location) - self.elements - 97
        self.pos = (locate // self.j, locate % self.j)
        self.room = []
        for x in range(self.i):
            self.room.append([(chr(self.elements + 97 + (x * self.j) + y)) for y in range(self.j)])
        e, w = self.pos
        print()
        loc = r'game_data\\room_data\\room' + str(self.room_number) + '\\' + str(self.room[e][w]) + '.txt'
        print_file(loc)

        if read is True:
            print('done')
            self.items_in_room = []
            self.getItems(player_name)

        if len(self.items_in_room) > 0:
            for x, y in self.items_in_room:
                if y == location:
                    print(x, end=" ")
            print()

    def getItems(self, player_name, visited=1):
        """get items which are in the room form the external data file"""

        loc = r'player_data\\items_loc\\' + player_name + '.csv'

        if visited == 1:
            items = pd.read_csv(loc)
        else:
            items = pd.read_csv(r'game_data/items/items_loc.csv')
            items.to_csv(loc, index=False)
        size = items.size // 2

        for index in range(size):
            for i in range(self.i):
                if items.location[index] in self.room[i]:
                    self.items_in_room.append([items.item[index], items.location[index]])

    def saveItems(self, player_name):
        """save items which are in the room from the data frame to external for persistence"""

        loc = r'player_data\\items_loc\\' + player_name + '.csv'
        items = pd.read_csv(loc)

        for item in range(len(self.items_in_room)):
            index = items[items['item'] == self.items_in_room[0][item]].index.values
            items.location[index] = self.items_in_room[1][item]

        items.to_csv(loc, index=False)


class Player(Room):
    """this class holds all the information about the player"""

    dead = None
    Win = False
    player_name = ""
    c_location = ''
    rooms_visited = []
    rooms_unlocked = []
    bag = []
    password = ""

    def __init__(self):
        """initialise the rooms_visited and rooms_unlocked lists"""

        while 1:
            new_player = input("new player? (y/n):").lower()
            if new_player == 'y':
                new = True
                break
            elif new_player == 'n':
                new = False
                break
            else:
                print("Invalid input!!")

        info = pd.read_csv(r'player_data\info.csv')
        while 1:
            self.player_name = input("Enter player name: ")
            if new is False:
                username = [i for i in info.username]
                if self.player_name in username:
                    self.password = input("enter password: ")
                    index = findIndex(info, self.player_name, "username", 5)
                    if self.password == str(info.password[index[0]]):
                        print("Login successful")
                        self.c_location = info.location[index[0]]
                        # split and integer conversion in one
                        self.rooms_visited = [int(i) for i in re.split(',', info.room[index[0]])]
                        self.rooms_unlocked = [int(i) for i in re.split(',', info.status[index[0]])]
                        break
                    else:
                        print("incorrect password")
                else:
                    print("user not found. making new entry....")
                    new = True
            if new is True:
                if self.player_name in info.username:
                    print("user already exists, try different name!")
                else:
                    self.password = input("set password: ")
                    info = open(r'player_data\\info.csv', 'a')
                    info.write(self.player_name + "," + self.password + ",\"1,0,0,0,0\",a,\"1,0,0,0,0\"\n")
                    info.close()
                    pd.read_csv(r'game_data\\items\\items_loc.csv').to_csv(r'player_data\\items_loc\\'
                                                                           + self.player_name + '.csv', index=False)
                    
                    self.c_location = 'a'
                    self.rooms_unlocked = [1, 0, 0, 0, 0]
                    self.rooms_visited = [1, 0, 0, 0, 0]
                    self.visited = 1

                    self.createRoom(self.player_name, self.c_location, False)
                    self.getItems(self.player_name, 0)
                    
                    print_file(r'game_data\\misc\\intro.txt')
                    break

    def start_game(self):
        """creating the room according to the player by checking if the player is new or not"""

        self.createRoom(self.player_name, self.c_location, False)
        self.visited = self.rooms_visited[self.room_number - 1]

    def reset_progress(self):
        """reset the player's game progress"""

        self.room_number = 1
        self.c_location = 'a'
        self.rooms_unlocked = [1, 0, 0, 0, 0]
        self.rooms_visited = [1, 0, 0, 0, 0]
        self.visited = 1
        self.dead = False
        self.bag = []
        self.pos = (0, 0)
        self.items_in_room = []
        pd.read_csv(r'game_data\\items\\items_loc.csv').to_csv(r'player_data\\items_loc\\' + self.player_name + '.csv',
                                                               index=False)
        self.save_progress()

    def getBagItems(self):
        """get items form player specific"""

        items = pd.read_csv(r'player_data\\items_loc\\' + self.player_name + ".csv")
        index = findIndex(items, 'bag', 'location', 2)
        for i in index:
            try:
                self.bag.append(items.item[i])
            except IndexError:
                break

    def get_items_at_loc(self):
        list_item = []
        self.getItems(self.player_name)
        for item, loc in self.items_in_room:
            if loc == self.c_location:
                list_item.append(item)
        return list_item

    def save_progress(self):
        players_data = pd.read_csv(r'player_data\\info.csv')
        index = findIndex(players_data, self.player_name, 'username', 5)[0]

        visited, unlocked = '', ''
        for i in range(5):
            visited = visited + str(self.rooms_visited[i]) + ','
            unlocked = unlocked + str(self.rooms_unlocked[i]) + ','
        visited = visited[:-1]
        unlocked = unlocked[:-1]

        players_data['room'][index] = visited
        players_data['status'][index] = unlocked
        players_data['location'][index] = self.c_location
        players_data.to_csv(r'player_data\\info.csv', index=False)

    def motion(self, direction):
        """defines proper movement of the player according to room, current location and surrounding objects"""

        temp_i, temp_j = self.pos

        if direction == 'w':
            temp_i = temp_i + 1
        elif direction == 's':
            temp_i = temp_i - 1
        elif direction == 'd':
            temp_j = temp_j - 1
        elif direction == 'a':
            temp_j = temp_j + 1

        # room data
        if -1 < temp_i < self.i and -1 < temp_j < self.j:
            # room location files
            self.pos = temp_i, temp_j
            self.c_location = self.room[temp_i][temp_j]
            if (self.room_number == 3 or self.room_number == 5) and not self.dead:
                print_file(r'game_data\room_data\room' + str(self.room_number) + "\\" +
                           self.c_location + 'z.txt')
            else:
                print_file(r'game_data\room_data\room' + str(self.room_number) + "\\" +
                           self.c_location + '.txt')
            # print_file(r'game_data\room_data\room' + str(self.room_number) + "\\" +
            #            self.c_location + '.txt')
            list_item = self.get_items_at_loc()

            if len(list_item) > 0:
                print("\n Items nearby are as follows :")
                print(list_item)
            print()
        # every other data around
        else:
            key = self.c_location
            found = False
            dire, loc, room_n = None, None, 0

            if key in self.des.keys():
                dire, info = self.des[key]
                if dire == direction:
                    found = True
                    if key == 'f':
                        dire, loc, room_n = self.door['e']
                    print_file(r'game_data\\room_data\\des\\' + info)
            elif key in self.door.keys():
                dire, loc, room_n = self.door[key]
                if dire == direction:
                    found = True
                    any_room, room3 = False, False
                    if room_n == 3:
                        if 'torch' in self.bag:
                            room3 = True
                    else:
                        any_room = True
                    if room_n != 6:
                        if self.rooms_unlocked[room_n - 1] == 1 and (any_room or room3):
                            print("unlocked")
                            self.rooms_visited[room_n - 1] = 1
                            self.c_location = loc
                            self.createRoom(self.player_name, loc)
                            self.save_progress()
                            self.dead = None
                            return
                        else:
                            if self.room_number > room_n and (any_room or room3):
                                self.c_location = loc
                                self.createRoom(self.player_name, loc)
                                self.visited = 1
                                self.save_progress()
                            else:
                                if any_room or room3:
                                    print("door is locked!! Find a way in.")
                                else:
                                    print("its too dark. find a torch.")
                    else:
                        if self.Win is False:
                            print("Door locked. Find the exit door key")
            try:
                if found is True and self.rooms_unlocked[room_n - 1] == 0:
                    if key in self.puzzle.keys():
                        if self.puzzle[key](self.bag):
                            self.rooms_unlocked[room_n - 1] = 1
                        else:
                            if self.room_number == 3:
                                self.dead = True
                else:
                    if self.room_number == 3:
                        print("movement blocked!")
                    else:
                        print("Wall ahead!")
            except IndexError:
                if room_n == 6:
                    self.Win = self.win()
            if (self.c_location == 'u' or self.c_location == 'v') and self.dead is False:
                self.dead = is_dead(self.bag)
            if self.dead:
                print("you were killed !!!!")
                self.reset_progress()
        # .......................................................................

    def pickup(self, item_list):
        """proper mechanism of picking items with limiting max number of items at one time to 3"""

        length = len(item_list)
        while 1:
            [print(str(x + 1) + ": " + y, end="  ") for x, y in zip(range(length), item_list)]
            print()
            try:
                num_item = int(input("enter item number to pick?"))
                if 0 < num_item <= length:
                    if len(self.bag) < 3:
                        self.bag.append(item_list[num_item - 1])

                        loc = r'player_data\\items_loc\\' + self.player_name + '.csv'
                        player_items = pd.read_csv(loc)
                        index = findIndex(player_items, item_list[num_item - 1], 'item', 2)[0]
                        player_items.location[index] = 'bag'
                        player_items.to_csv(loc, index=False)
                        print(player_items.location[index], player_items.item[index])

                        # room 5 and exit door key
                        if item_list[num_item - 1] == 'room 5 key':
                            self.rooms_unlocked[4] = 1
                        return
                else:
                    raise ValueError("Sorry! ")
            except ValueError:
                print("invalid item number")

    def win(self):
        if 'exit door key' in self.bag:
            return True
        return False

    def drop(self):
        """proper mechanism for dropping items from bag"""

        length = len(self.bag)
        [print(str(x + 1) + ": " + y, end="  ") for x, y in zip(range(length), self.bag)]
        print()
        while 1:
            try:
                num_item = int(input("enter item number to pick?"))
                if 0 < num_item <= length:
                    item = self.bag.pop(num_item - 1)
                    self.items_in_room.append((item, self.c_location))
                    # todo: self.loc <optional>
                    loc = r'player_data\\items_loc\\' + self.player_name + '.csv'
                    item_file = pd.read_csv(loc)
                    index = findIndex(item_file, item, 'item', 2)[0]
                    item_file.location[index] = self.c_location
                    item_file.to_csv(loc, index=False)

                    if 'room 5 key' == item_file.item[index]:
                        self.rooms_unlocked[4] = 0

                    break
                else:
                    raise ValueError
            except ValueError:
                print("invalid item number")


# main game running code
print(pyfiglet.figlet_format("Zombied!"))
print("Co-powered by 19BCS6010 & 19BCS6026")

# initializing player
player = Player()

# game loop until player exits or wins the game
while 1:
    print("1. Start/Continue Game")
    print("2. Reset progress")
    print("3. Exit")
    try:
        action = int(input("choice (1/2/3): "))
        clear()
        if action == 1:
            print("\nYou can give following commands:"
                  "\nh for help"
                  "\nx to exit"
                  "\n[w,a,s,d] for movement"
                  "\np to pickup item"
                  "\nb to see items in bag"
                  "\n enter nothing to see info about current location")
            player.start_game()
            motion = ['w', 'a', 's', 'd']
            while player.Win is False:
                action = input("action: ")
                clear()
                if action in motion:
                    player.motion(action)
                elif action == 'h':
                    print(pyfiglet.figlet_format("Help"))
                    print_file(r'game_data\\misc\\help.txt')
                elif action == 'p':
                    items_list = player.get_items_at_loc()
                    if len(items_list) == 0:
                        print("nothing to pick")
                    else:
                        print()
                        if len(player.bag) < 3:
                            player.pickup(items_list)
                        else:
                            print("Bag is already full. remove items to pick something.")
                elif action == 'b':
                    print(pyfiglet.figlet_format("Bag"))
                    print(player.bag)
                    while 1:
                        choice = input("Want to drop any item?(y/n)").lower()
                        if choice == 'y':
                            # drop
                            if len(player.bag) == 0:
                                print("bag is empty")
                            else:
                                player.drop()
                            break
                        elif choice == 'n':
                            break
                        else:
                            print("invalid input")
                elif action == 'x':
                    print("Thank you for playing the game!")
                    break
                elif action == '':
                    print_file(r'game_data\room_data\room' + str(player.room_number) + "\\" +
                               player.c_location + '.txt')
            if player.Win is True:
                print(pyfiglet.figlet_format("Congratulations"))
                print_file(r'game_data\\misc\\congrats.txt')
                break
        elif action == 2:
            player.reset_progress()
        elif action == 3:
            print(pyfiglet.figlet_format("Bye!"))
            print("Thank you for playing")
            break
        else:
            print("invalid input")
    except ValueError:
        print("Invalid input")
input("press anything to exit")
# todo: if item_loc.csv in game_data not found create the file
