import pygame, sys
import random
import math

FPS = 30
WIDTH = 900
HEIGHT = 900
WIDTH_2 = 900 // 2
HEIGHT_2 = 900 // 2

CELLS_X = 18
CELLS_Y = 18
CELL_SIZE = 50

class Enemy():
    def init(self, x, y, health, speed, size, color, reward):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.health = health
        self.speed = speed
        self.start = 0
        self.reward = reward

    def draw(self):
        pygame.draw.circle(screen, self.color, [self.x, self.y,], self.size)

    def moving(self):
        pass

class Player():
    def init(self, money, health):
        self.money = money
        self.health = health

class BasicTower():
    def init(self, x, y, size, damage, reload, range, cost, color):
        self.x = x
        self.y = y
        self.size = size
        self.damage = damage
        self.reload = reload
        self.current_reload = 0
        self.cost = cost
        self.range = range
        self.color = color

    def draw_tower(self):
        pygame.draw.circle(screen, self.color, [self.x, self.y], self.size)


class MachineGun(BasicTower):
    pass

class Artillery(BasicTower):
    pass

class Lazer(BasicTower):
    pass

class Bullet():
    def init(self, x, y, size, color, damage, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage
        self.speed = speed

    def moving(self, vec_x, vec_y):
        self.x += self.speed * vec_x
        self.y += self.speed * vec_y

def draw_map():
    for i in range(CELLS_X):
        pygame.draw.line(screen, "white", [i * CELL_SIZE, 0], [i * CELL_SIZE, HEIGHT])
    for i in range(CELLS_Y):
        pygame.draw.line(screen, "white", [0, i * CELL_SIZE], [WIDTH, i * CELL_SIZE])

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True

def draw_map():
    mouse_pos = pygame.mouse.get_pos()
    pos_x = math.floor(mouse_pos[0] / CELL_SIZE) * CELL_SIZE
    pos_y = math.floor(mouse_pos[1] / CELL_SIZE) * CELL_SIZE
    pygame.draw.rect(screen, "green", [pos_x, pos_y, CELL_SIZE, CELL_SIZE])
    for i in range(CELLS_X):
        pygame.draw.line(screen, "white", [i * CELL_SIZE, 0], [i * CELL_SIZE, HEIGHT])
    for i in range(CELLS_Y):
        pygame.draw.line(screen, "white", [0, i * CELL_SIZE], [WIDTH, i * CELL_SIZE])

def Main():
    draw_map()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #if event.type == pygame.MOUSEMOTION:
            # mouse_pos = event.pos
        #if event.type == pygame.MOUSEBUTTONDOWN:
            #   print(board.get_cell(event.pos))
    screen.fill("black")
    Main()
    pygame.display.update()
    clock.tick(FPS)

while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
pygame.quit()
