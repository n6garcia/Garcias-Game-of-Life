import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import os, sys, subprocess


def initialize_grid(size):
    return np.random.choice([0, 1], size=(size, size))


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


def update_grid_odd(grid):
    size = len(grid)
    new_grid = np.copy(grid)

    for x in range(size):
        for y in range(size):
            neighbors = count_neighbors(
                new_grid, x, y
            )  # Use new_grid to count neighbors
            if grid[x][y] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[x][y] = 0  # Huilon becomes vacuumous (dies)
            else:
                if neighbors == 3:
                    new_grid[x][y] = 1  # Huilon becomes spacious (birth)
    return new_grid


def update_grid(grid):
    new_grid = np.copy(grid)
    size = len(grid)

    for x in range(size):
        for y in range(size):
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
        if "--odd" in sys.argv:
            grid = update_grid_odd(grid)
        else:
            grid = update_grid(grid)
        img.set_data(grid)
        return [img]

    ani = animation.FuncAnimation(
        fig, animate, frames=steps, blit=True, interval=100, repeat=False
    )
    plt.show()


# Example usage
animate_grid(size=50, steps=100)
