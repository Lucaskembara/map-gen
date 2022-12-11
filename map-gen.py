import noise
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap

# PARAMETERS
sea_level = -0.05
beach_level = 0
land_level = .35
mountain_level = .55
snow_level = mountain_level

SIZE = 1000
ZOOM = SIZE/2

cmap = ListedColormap(['dodgerblue', 'moccasin', 'green', 'grey', 'white'])

def generate_map(SIZE, ZOOM, octaves=15, persistence=.5, lacunarity=2.0):
    shape = (SIZE,SIZE)
    scale = ZOOM
    seed = random.random()

    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.snoise2(i/scale, 
                                    j/scale, 
                                    octaves=octaves, 
                                    persistence=persistence, 
                                    lacunarity=lacunarity, 
                                    base=seed)
    
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            #Sea
            if world[i][j] < sea_level:
                world[i][j] = -3
            #Beach
            elif world[i][j] >= sea_level and world[i][j] < beach_level:
                world[i][j] = -1
            #Land
            elif world[i][j] >= beach_level and world[i][j] < land_level:
                world[i][j] = 0
            #Mountain
            elif world[i][j] >= land_level and world[i][j] < mountain_level:
                world[i][j] = 1
            #Snow
            elif world[i][j] >= snow_level:
                world[i][j] = 3

    return world

map = generate_map(SIZE=SIZE, ZOOM=ZOOM)
plt.imshow(map, cmap=cmap)
plt.savefig('map.png')