from random import randint
import pygame  # pour installer le module pygame: pip3 install pygame ou pip3 install -r requirements.txt
import sys
from math import sin, cos, pi


# Experience1: Plaquette (c'est long)
# wid = 3
# ro = 0.37
# N = 52 #taille horisontale
# M = 172 #taille verticale
# kappa = 0.003
# alpha = 0.08
# beta = 1.37
# theta = 0.025
# gamma = 0.0005
# mu = 0.07


# Experience2: plaquette sectorisée (un peu plus rapide)
# wid = 3
# ro = 0.48
# N = 52
# M = 172
# kappa = 0.003
# alpha = 0.08
# beta = 1.37
# theta = 0.025
# gamma = 0.0005
# mu = 0.07


# Experience3: Dendritique (rapide)
wid = 3
ro = 0.9
N = 70
M = 220
kappa = 0.003
alpha = 0.08
beta = 1.37
theta = 0.025
gamma = 0.0005
mu = 0.07


# Experience4: stellaire avec des terminaisons plates (un peu long parce que sur un grand écran)
# wid = 3
# ro = 0.36
# N = 90
# M = 240
# kappa = 0.0001
# alpha = 0.01
# beta = 1.09
# theta = 0.0745
# gamma = 0.00001
# mu = 0.14


def init(x, y):
    grid = []
    for r in range(x):
        row = []
        for c in range(y):
            row.append({'a': 0, 'b': 0, 'c': 0, 'd': ro})
        grid.append(row)
    grid[x//2][y//2]['a'] = 1
    grid[x//2][y//2]['c'] = 1
    grid[x//2][y//2]['d'] = 0
    return grid


def make_empty_grid(x, y):
    grid = []
    for r in range(x):
        row = []
        for c in range(y):
            row.append({'a': 0, 'b': 0, 'c': 0, 'd': ro})
        grid.append(row)
    return grid


def voisins(i, j):
    if not j % 2:
        return [(i, j-1), (i, j+1), (i, j+2), (i, j-2), (i-1, j-1), (i-1, j+1)]
    else:
        return [(i, j-1), (i, j+1), (i, j+2), (i, j-2), (i+1, j-1), (i+1, j+1)]


def compte_voisins(i, j):
    vois = voisins(i, j)
    bound = 0
    for x, y in vois:
        if world[x][y]['a'] == 1:
            bound += 1
    return bound


def vapo_voisins(i, j):
    vois = voisins(i, j)
    dif = world[i][j]['d']
    for x, y in vois:
        if world[x][y]['a'] == 1:
            dif += world[i][j]['d']
        else:
            dif += world[x][y]['d']
    return dif


def somme_voisins(i, j):
    vois = voisins(i, j)
    dif = world[i][j]['d']
    for x, y in vois:
        dif += world[x][y]['d']
    return dif


def diffusion(grid, i, j):
    new = dict.copy(grid[i][j])
    if grid[i][j]['a'] == 0:
        dif = vapo_voisins(i, j)
        new['d'] = dif/7
    return (new)


def diffuse_world(grid):
    x = N
    y = M
    new_grid = make_empty_grid(x, y)
    for r in range(2, x-2):
        for c in range(2, y-2):
            new_grid[r][c] = diffusion(grid, r, c)
    return new_grid


def freeze(grid, i, j):
    new = dict.copy(grid[i][j])
    bound = compte_voisins(i, j)
    if bound != 0 and grid[i][j]['a'] == 0:
        new['b'] = grid[i][j]['b'] + (1 - kappa) * grid[i][j]['d']
        new['c'] = grid[i][j]['c'] + kappa * grid[i][j]['d']
        new['d'] = 0
    return new


def freeze_world(grid):
    x = N
    y = M
    new_grid = make_empty_grid(x, y)
    for r in range(2, x-2):
        for c in range(2, y-2):
            new_grid[r][c] = freeze(grid, r, c)
    return new_grid


def attachement(grid, i, j):
    new = dict.copy(grid[i][j])
    dif = somme_voisins(i, j)
    bound = compte_voisins(i, j)
    if (bound == 1 or bound == 2) and grid[i][j]['b'] >= beta:
        new['a'] = 1
        new['b'] = 0
        new['c'] = grid[i][j]['c'] + grid[i][j]['b']
    elif bound == 3:
        if (grid[i][j]['b'] >= 1) or (dif < theta and grid[i][j]['b'] > alpha):
            new['a'] = 1
            new['b'] = 0
            new['c'] = grid[i][j]['c'] + grid[i][j]['b']
    elif bound >= 4:
        new['a'] = 1
        new['b'] = 0
        new['c'] = grid[i][j]['c'] + grid[i][j]['b']
    return new


def attache_world(grid):
    x = N
    y = M
    new_grid = make_empty_grid(x, y)
    for r in range(2, x-2):
        for c in range(2, y-2):
            new_grid[r][c] = attachement(grid, r, c)
    return new_grid


def melting(grid, i, j):
    new = dict.copy(grid[i][j])
    if grid[i][j]['a'] == 0:
        bound = compte_voisins(i, j)
        if bound != 0:
            new['b'] = (1-mu)*grid[i][j]['b']
            new['c'] = (1-gamma)*grid[i][j]['c']
            new['d'] = grid[i][j]['d'] + mu * \
                grid[i][j]['b'] + gamma*grid[i][j]['c']
    return new


def melting_world(grid):
    x = N
    y = M
    new_grid = make_empty_grid(x, y)
    for r in range(2, x-2):
        for c in range(2, y-2):
            new_grid[r][c] = melting(grid, r, c)
    return new_grid


BLACK = (0, 0, 0)
BLEU = (176, 196, 222)
ROUGE = (240, 128, 128)
BLANC = (255, 255, 255)


def draw_block1(x, y, color):
    xp = x * 3.4 * wid
    yp = y * wid
    pygame.draw.polygon(screen, color,
                        [
                            (xp + wid * cos(2 * pi * i / 6),
                             yp + wid * sin(2 * pi * i / 6))
                            for i in range(6)
                        ], 0)


def handleInputEvents():
    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN):
            if event.key == pygame.K_s:
                pygame.image.save(screen, 'ro='+str(ro)+'k='+str(kappa) + 'alp=' +
                                  str(alpha)+'be='+str(beta)+'th='+str(theta)+'ga='+str(gamma)+'mu='+str(mu)+'.jpeg')
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
        if (event.type == pygame.QUIT):
            print("quitting")
            sys.exit(0)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    global screen
    screen = pygame.display.set_mode((N * wid * 3.4, M * wid))
    pygame.display.set_caption("Flocon")
    cell_number = 0
    xlen = N
    ylen = M
    global world
    world = init(xlen, ylen)
    global snow
    up = 0
    while True:
        handleInputEvents()
        clock.tick(20)
        for x in range(xlen):
            for y in range(ylen):
                ice = world[x][y]
                cell_number += 1
                if ice['a'] == 1:
                    cell_color = (80 - ice['a']*33,
                                  160-ice['c']*66, 255-ice['c']*100)
                else:
                    cell_color = BLANC
                if not y % 2:
                    draw_block1(x, y, cell_color)
                else:
                    draw_block1(x+1/2, y, cell_color)
        up += 1
        pygame.display.flip()
        world = diffuse_world(world)
        world = freeze_world(world)
        world = attache_world(world)
        world = melting_world(world)
        cell_number = 0
        print(up)


if __name__ == '__main__':
    main()
