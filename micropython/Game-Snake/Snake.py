from microbit import *
from random import randrange

DIR = {
    'NONE': 0,
    'U': 1,
    'D': 2,
    'L': 3,
    'R': 4,
    'U_L': 5,
    'U_R': 6,
    'D_L': 7,
    'D_R': 8
}


class JOYSTICK():
    def __init__(self):
        self.Read_X = pin1.read_analog()
        self.Read_Y = pin2.read_analog()

    def Listen_Dir(self, Dir):
        Get_Rocker = DIR['NONE']
        New_X = pin1.read_analog()
        New_Y = pin2.read_analog()

        Dx = abs(self.Read_X - New_X)
        Dy = abs(self.Read_Y - New_Y)

        Right = New_X - self.Read_X
        Left = self.Read_X - New_X
        Up = New_Y - self.Read_Y
        Down = self.Read_Y - New_Y

        # max = 1023
        Precision = 256

        if Right > Precision and Dy < Precision:
            Get_Rocker = DIR['R']
        elif Left > Precision and Dy < Precision:
            Get_Rocker = DIR['L']
        elif Up > Precision and Dx < Precision:
            Get_Rocker = DIR['U']
        elif Down > Precision and Dx < Precision:
            Get_Rocker = DIR['D']
        elif Right > Precision and Up > Precision:
            Get_Rocker = DIR['U_R']
        elif Right > Precision and Down > Precision:
            Get_Rocker = DIR['D_R']
        elif Left > Precision and Up > Precision:
            Get_Rocker = DIR['U_L']
        elif Left > Precision and Down > Precision:
            Get_Rocker = DIR['D_L']
        else:
            Get_Rocker = DIR['NONE']

        if Dir == Get_Rocker:
            return True
        else:
            return False


class Snake():
    def __init__(self):
        self.length = 2
        self.direction = "down"
        self.head = (2, 2)
        self.tail = []

    def move(self):
        # extend tail
        self.tail.append(self.head)

        # check snake size
        if len(self.tail) > self.length - 1:
            self.tail = self.tail[-(self.length - 1):]

        if self.direction == "left":
            self.head = ((self.head[0] - 1) % 5, self.head[1])
        elif self.direction == "right":
            self.head = ((self.head[0] + 1) % 5, self.head[1])
        elif self.direction == "up":
            self.head = (self.head[0], (self.head[1] - 1) % 5)
        elif self.direction == "down":
            self.head = (self.head[0], (self.head[1] + 1) % 5)

    def grow(self):
        self.length += 1

    def collides_with(self, position):
        return position == self.head or position in self.tail

    def draw(self):
        # draw head
        display.set_pixel(self.head[0], self.head[1], 9)

        # draw tail
        brightness = 8
        for dot in reversed(self.tail):
            display.set_pixel(dot[0], dot[1], brightness)
            brightness = max(brightness - 1, 5)


class Fruit():
    def __init__(self):
        # place in a random position on the screen
        self.position = (randrange(0, 5), randrange(0, 5))

    def draw(self):
        display.set_pixel(self.position[0], self.position[1], 9)


class Game():
    def __init__(self):
        self.player = Snake()
        self.place_fruit()
        self.joystick = JOYSTICK()

    def place_fruit(self):
        while True:
            self.fruit = Fruit()
            # check it's in a free space on the screen
            if not self.player.collides_with(self.fruit.position):
                break

    def handle_input(self):
        self.dir = self.player.direction
        if self.joystick.Listen_Dir(DIR['U']):
            self.dir = "up"
        elif self.joystick.Listen_Dir(DIR['D']):
            self.dir = "down"
        elif self.joystick.Listen_Dir(DIR['L']):
            self.dir = "left"
        elif self.joystick.Listen_Dir(DIR['R']):
            self.dir = "right"
        self.player.direction = self.dir

    def update(self):
        # move snake
        self.player.move()

        # game over?
        if self.player.head in self.player.tail:
            self.game_over()

        # nom nom nom
        elif self.player.head == self.fruit.position:
            self.player.grow()

            # space for more fruit?
            if self.player.length < 5 * 5:
                self.place_fruit()
            else:
                self.game_over()

    def score(self):
        return self.player.length - 2

    def game_over(self):
        display.scroll("Score: %s" % self.score())
        reset()

    def draw(self):
        display.clear()
        self.player.draw()
        self.fruit.draw()


game = Game()

# main game loop
while True:
    game.handle_input()
    game.update()
    game.draw()
    sleep(500)
