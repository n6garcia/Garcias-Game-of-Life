import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os, sys, subprocess
from random import random, choice


def parse_cells(fname):
    dat = open(fname, "rb").read().decode("utf-8")
    ship = []
    for ln in dat.splitlines():
        # print(ln)
        if ln.startswith("!"):
            continue  ## comments
        if not len(ln.strip()):
            continue  ## empty line
        a = []
        for char in ln:
            if char == ".":
                a.append(0)
            else:
                a.append(1)
        ship.append(a)
    # print(ship)
    return ship


ship_names = [
    "Coe_ship",
    "Glider",
    "Lightweight_spaceship",
    "Middleweight_spaceship",
    "Heavyweight_spaceship",
    "MWSS_on_MWSS_1",
    "LWSS_on_MWSS_2",
    "LWSS_on_MWSS_3",
    "Sidecar",
    "Loafer",
    "X66",
    "Big_A",
    "Dart",
]

ships = []

for ship in ship_names:
    wiki = "https://conwaylife.com/wiki/" + ship
    # print(wiki)
    name = "%s.cells" % ship.lower().replace("_", "")
    name = (
        name.replace("light", "l")
        .replace("heavy", "h")
        .replace("weight", "w")
        .replace("middle", "m")
        .replace("spaceship", "ss")
    )
    url = "https://www.conwaylife.com/patterns/" + name
    # print(url)
    if not os.path.isfile("./" + name):
        cmd = ["wget", url]
        print(cmd)
        subprocess.check_call(cmd)

    ships.append(parse_cells("./" + name))


def initialize_grid(size, spawn=3):
    if "--10gl" in sys.argv:
        spawn = 10
    g = np.zeros((size, size), dtype=np.int8)
    for s in range(spawn):
        ship = choice(ships)
        for y, ln in enumerate(ship):
            for x, val in enumerate(ln):
                if val:
                    g[x][y] = 1
    return g


def count_neighbors(grid, x, y):
    size = len(grid)
    return sum(
        [
            grid[(x + i) % size][(y + j) % size]
            for i in [-1, 0, 1]
            for j in [-1, 0, 1]
            if (i, j) != (0, 0)
        ]
    )


def update_grid(grid):
    new_grid = np.copy(grid)
    size = len(grid)

    for x in range(size):
        for y in range(size):
            if "--odd" in sys.argv:
                # Use new_grid to count neighbors
                neighbors = count_neighbors(new_grid, x, y)
            else:
                neighbors = count_neighbors(grid, x, y)
            if grid[x][y] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[x][y] = 0  # Huilon becomes vacuumous (dies)
            else:
                if neighbors == 3:
                    new_grid[x][y] = 1  # Huilon becomes spacious (birth)
    return new_grid


def animate_grid(size, steps):
    grid = initialize_grid(size)

    fig, ax = plt.subplots()
    ax.set_axis_off()
    img = ax.imshow(grid, cmap="binary")

    def animate(i):
        nonlocal grid
        grid = update_grid(grid)
        img.set_data(grid)
        return [img]

    ani = animation.FuncAnimation(
        fig, animate, frames=steps, blit=True, interval=100, repeat=False
    )
    plt.show()


# Example usage
if "--1k-steps" in sys.argv:
    if "--2x" in sys.argv:
        animate_grid(size=100, steps=1000)
    else:
        animate_grid(size=50, steps=1000)
else:
    if "--2x" in sys.argv:
        animate_grid(size=100, steps=100)
    else:
        animate_grid(size=50, steps=100)
