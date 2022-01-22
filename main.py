import math
import keyboard
import pygame

FPS = 30
WIDTH = 900
HEIGHT = 900
WIDTH_2 = 900 // 2
HEIGHT_2 = 900 // 2

CELLS_X = 18
CELLS_Y = 18
CELL_SIZE = 50
CELL_SIZE_2 = 25

all_towers = []
all_bullets = []
enemies = []
enemy_way = []

monsterhp = 50
MONSTERSPEED = 10
wafetime = 0
NUMBERMONSTERS = 5
wavecounter = 1
monsterreward = 10
numberofmonsters = 8
boss_hp = 30000
boss = False
bossreward = 3000

Map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 10],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [1, 2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 5, 1, 1, 1, 6, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 1, 1, 1, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


def Create_enemy_way():
    for i in range(len(Map)):
        for j in range(len(Map[0])):
            if Map[i][j] != 0:
                enemy_way.append(Way(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def Draw_Enemy_way(color):
    for way in enemy_way:
        pygame.draw.rect(screen, color, (way.x, way.y, way.size_x, way.size_y))


def draw_map():
    mouse_pos = pygame.mouse.get_pos()
    pos_x = math.floor(mouse_pos[0] / CELL_SIZE) * CELL_SIZE
    pos_y = math.floor(mouse_pos[1] / CELL_SIZE) * CELL_SIZE
    pygame.draw.rect(screen, "green", [pos_x, pos_y, CELL_SIZE, CELL_SIZE])
    for i in range(CELLS_X):
        pygame.draw.line(screen, "white", [i * CELL_SIZE, 0], [i * CELL_SIZE, HEIGHT])
    for i in range(CELLS_Y):
        pygame.draw.line(screen, "white", [0, i * CELL_SIZE], [WIDTH, i * CELL_SIZE])


class Enemy:
    def __init__(self, x, y, health, speed, size, color, reward):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.health = health
        self.point = 0
        self.speed = speed
        self.reward = reward

    def Draw(self):
        if not boss:
            image = pygame.image.load('monster.png').convert_alpha()
            screen.blit(image, (self.x - 15, self.y - 15))
        else:
            image = pygame.image.load('boss.png').convert_alpha()
            screen.blit(image, (self.x - 30, self.y - 30))

    def getdamage(self):
        if self.health <= 0:
            player.money += self.reward
            enemies.remove(self)


    def Move(self):
        a = vector(self.x, self.y, enemy_points[self.point][0], enemy_points[self.point][1])
        self.x += self.speed * a[0]
        self.y += self.speed * a[1]
        if a[2] <= self.speed:
            self.point += 1
            if self.point == len(enemy_points):
                enemies.remove(self)
                player.health -= 1


class Way:
    def __init__(self, x, y, size_x, size_y):
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y


class Player:
    def __init__(self, money, health):
        self.money = money
        self.health = health


class BasicTower:
    def __init__(self, x, y, size, damage, reload, length_of_shot, cost, color):
        self.x = x
        self.y = y
        self.size = size
        self.damage = damage
        self.reload = reload
        self.current_reload = 0
        self.cost = cost
        self.range = length_of_shot
        self.color = color

    def draw_tower(self):
        if self.color == 'red':
            image = pygame.image.load('ower1.png').convert_alpha()
            screen.blit(image, (self.x - 30, self.y - 40))
        elif self.color == 'yellow':
            image = pygame.image.load('ower2.png').convert_alpha()
            screen.blit(image, (self.x - 30, self.y - 40))
        elif self.color == 'green':
            image = pygame.image.load('ower3.png').convert_alpha()
            screen.blit(image, (self.x - 30, self.y - 40))



class MachineGun(BasicTower):
    def shot(self):
        distance = 999999999
        current = 0
        for i in range(len(enemies)):
            closest_enemy = vector(self.x + CELL_SIZE_2, self.y + CELL_SIZE_2, enemies[i].x, enemies[i].y)
            if closest_enemy[2] < distance:
                current = i
        if len (enemies) > 0:
            f_closest_enemy = vector(self.x, self.y, enemies[current].x, enemies[current].y)
            if self.current_reload <= 0 and f_closest_enemy[2] <= self.range:
               all_bullets.append(Bullet(self.x, self.y, 3, "red", self.damage, 10))
               self.current_reload = self.reload
            else:
                self.current_reload -= 1 / FPS


class Artillery(BasicTower):
    def shot(self):
        distance = 999999999
        current = 0
        for i in range(len(enemies)):
            closest_enemy = vector(self.x + CELL_SIZE_2, self.y + CELL_SIZE_2, enemies[i].x, enemies[i].y)
            if closest_enemy[2] < distance:
                current = i
        if len(enemies):
            f_closest_enemy = vector(self.x, self.y, enemies[current].x, enemies[current].y)
            if self.current_reload <= 0 and f_closest_enemy[2] <= self.range:
                all_bullets.append(Bullet(self.x, self.y, 5, "green", self.damage, 8))
                self.current_reload = self.reload
            else:
                self.current_reload -= 1 / FPS


class Lazer(BasicTower):
    def shot(self):
        distance = 999999999
        current = 0
        for i in range(len(enemies)):
            closest_enemy = vector(self.x + CELL_SIZE_2, self.y + CELL_SIZE_2, enemies[i].x, enemies[i].y)
            if closest_enemy[2] < distance:
                current = i
        if len(enemies) > 0:
            f_closest_enemy = vector(self.x, self.y, enemies[current].x, enemies[current].y)
            if self.current_reload <= 0 and f_closest_enemy[2] <= self.range:
                all_bullets.append(Bullet(self.x, self.y, 2, "yellow", self.damage, 12))
                self.current_reload = self.reload
            else:
                self.current_reload -= 1 / FPS


class Bullet:
    def __init__(self, x, y, size, color, damage, speed):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.damage = damage
        self.speed = speed
        self.closest = ""
        self.current_enemy = 0

    def moving(self):
        distance = 999999999
        current = 0
        for i in range(len(enemies)):
            closest_enemy = vector(self.x, self.y, enemies[i].x, enemies[i].y)
            if closest_enemy[2] < distance:
                current = i
                distance = closest_enemy[2]
        self.current_enemy = current
        if len(enemies) > 0:
            self.closest = vector(self.x, self.y, enemies[current].x, enemies[current].y)
        if len(self.closest) > 0:
            self.x += self.speed * self.closest[0]
            self.y += self.speed * self.closest[1]


    def draw_bullet(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def reached(self):
        if len(enemies) > 0:
            if self.closest[2] <= enemies[self.current_enemy].size + self.size:
                enemies[self.current_enemy].health -= self.damage
                all_bullets.remove(self)



def build():
    mouse_pos = pygame.mouse.get_pos()
    pos_x = math.floor(mouse_pos[0] / CELL_SIZE) * CELL_SIZE + CELL_SIZE_2
    pos_y = math.floor(mouse_pos[1] / CELL_SIZE) * CELL_SIZE + CELL_SIZE_2
    key = pygame.key.get_pressed()
    if key[pygame.K_1] and empty_slot(pos_x, pos_y) and player.money - 40 >= 0:
        all_towers.append(MachineGun(pos_x, pos_y, CELL_SIZE_2, 35, 0.2, 225, 40, "red"))
        player.money -= 40
        print(1)
    if key[pygame.K_2] and empty_slot(pos_x, pos_y) and player.money - 100 >= 0:
        all_towers.append(Artillery(pos_x, pos_y, CELL_SIZE_2, 150, 0.8, 300, 100, "green"))
        player.money -= 100
    if key[pygame.K_3] and empty_slot(pos_x, pos_y) and player.money - 75 >= 0:
        all_towers.append(Lazer(pos_x, pos_y, CELL_SIZE_2, 20, 0.05, 200, 75, "yellow"))
        player.money -= 75


def empty_slot(x, y):
    for elem in all_towers:
        if elem.x == x and elem.y == y:
            return False
    for elem in enemy_way:
        if elem.x == x and elem.y == y:
            return False
    return True


def vector(start_x, start_y, end_x, end_y):
    xx = end_x - start_x
    yy = end_y - start_y
    length = math.sqrt(xx ** 2 + yy ** 2)
    vector_x = xx / length
    vector_y = yy / length
    return (vector_x, vector_y, length)


def lost_the_game():
    if player.health <= 0:
        global running
        running = False


enemy_points = []

Create_enemy_way()


def Create_enemy_points(points_count):
    point = 2
    for k in range(points_count):
        for i in range(len(Map)):
            for j in range(len(Map[0])):
                if Map[i][j] == point:
                    enemy_points.append([j * CELL_SIZE + CELL_SIZE / 2, i * CELL_SIZE + CELL_SIZE / 2])
                    point += 1


def Creating_Enemy(health, speed, size, color, reward, numberofmonsters):
    for i in range(int(numberofmonsters)):
        x = enemy_points[0][0] - 200 - i * 20 - 5
        y = enemy_points[0][1]
        enemies.append(Enemy(x, y, health, speed, size, color, reward))


def Checking_player_death():
    if player.health <= 0:
        global running
        image = pygame.image.load('game-over.png').convert_alpha()
        screen.blit(image, (194, 194))
        running = False


Create_enemy_points(10)


def main():
    global monsterhp
    global monsterreward
    global all_bullets
    global numberofmonsters
    global boss
    global boss_hp
    global wavecounter
    global bossreward
    Draw_Enemy_way("darkgoldenrod")
    draw_map()
    pygame.draw.rect(screen, 'red', (851, 251, 49, 49))
    build()
    if len(enemies) == 0:
        wavecounter += 1
        all_bullets = []
        if wavecounter % 10 == 0:
            boss = True
            Creating_Enemy(boss_hp, 2, 10, 'midnightblue', bossreward, 1)
            bossreward += 5000
            boss_hp += 20000
        else:
            boss = False
            Creating_Enemy(monsterhp, 3, 10, 'midnightblue', monsterreward, numberofmonsters)
            numberofmonsters += 0.4
            monsterhp += 100
            monsterreward += 0.5
    for enemy in enemies:
        enemy.Move()
        enemy.Draw()
        enemy.getdamage()
    for tower in all_towers:
        tower.draw_tower()
        tower.shot()
    for bullet in all_bullets:
        bullet.moving()
        bullet.reached()
        bullet.draw_bullet()
    Checking_player_death()
    lost_the_game()


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
running = True
player = Player(100, 10)
f2 = pygame.font.SysFont('serif', 36)

key_enter = pygame.key.get_pressed()
while not key_enter[pygame.K_SPACE] and running:
    image = pygame.image.load('over-zakat.png').convert_alpha()
    screen.blit(image, (1, 1))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    key_enter = pygame.key.get_pressed()
    pygame.display.update()
    clock.tick(FPS)

timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEMOTION:
        # mouse_pos = event.pos
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #   print(board.get_cell(event.pos))
    screen.fill("forestgreen")
    main()
    timerr = f2.render(str(timer // 30), False, 'black')
    money = f2.render(str(player.money), False, "yellow")
    health = f2.render(str(player.health), False, "red")
    screen.blit(money, (10, 10))
    screen.blit(health, (10, 40))
    screen.blit(timerr, (10, 70))
    timer += 1
    pygame.display.update()
    clock.tick(FPS)
while pygame.event.wait().type != pygame.QUIT:
    pass
#КАК НАБРАТЬ СТРОКИ КОДА ПАМАГИТИ
pygame.quit()