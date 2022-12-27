import noise
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
import random
from matplotlib.colors import ListedColormap
from datetime import datetime

# PARAMETERS
sea_level = -0.05                                                               # Upper bound: Sea level on map
beach_level = 0                                                                 # Upper bound: Beach level on map
land_level = .35                                                                # Upper bound: Land level on map
mountain_level = .55                                                            # Upper bound: Mountain level on map
snow_level = mountain_level                                                     #            : Snow level equals all above Mountain level

octaves=15                                                                      # Read noise package documentation for elaboration
persistence=.5                                                                  # Read noise package documentation for elaboration
lacunarity=2.0                                                                  # Read noise package documentation for elaboration

SIZE = 1000                                                                     # Size of output
ZOOM = SIZE/2                                                                   # Zoom of output

N = 10                                                                          # Number of maps to generate

cmap = ListedColormap(['dodgerblue', 'moccasin', 'green', 'grey', 'white'])     # Colormap for map creation

class Map(object):
    def __init__(self, sea_level, beach_level, land_level, mountain_level, map=None):
        self.sea_level = sea_level
        self.beach_level = beach_level
        self.land_level = land_level
        self.mountain_level = mountain_level
        self.snow_level = self.mountain_level
    
    def generateMap(self, SIZE, ZOOM, octaves, persistence, lacunarity, seed=123, randomSeed=False):
        shape = (SIZE,SIZE)
        scale = ZOOM

        if randomSeed:
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
                if world[i][j] < self.sea_level:
                    world[i][j] = -3
                #Beach
                elif world[i][j] >= self.sea_level and world[i][j] < self.beach_level:
                    world[i][j] = -1
                #Land
                elif world[i][j] >= self.beach_level and world[i][j] < self.land_level:
                    world[i][j] = 0
                #Mountain
                elif world[i][j] >= self.land_level and world[i][j] < self.mountain_level:
                    world[i][j] = 1
                #Snow
                elif world[i][j] >= self.snow_level:
                    world[i][j] = 3

        self.map = world

    def vizMap(self, cmap, viz=False, save=False):
        fig = plt.figure(frameon=False)
        fig.set_size_inches(10,10)
        ax = plt.Axes(fig, [0., 0., 1., 1.])
        ax.set_axis_off()
        fig.add_axes(ax)
        ax.imshow(self.map, cmap=cmap, aspect='auto')

        if save:
            now = datetime.now().strftime("%H_%M_%S_%f")
            plt.savefig(f"data/{now}.png")

rootMap = Map(sea_level=sea_level, beach_level=beach_level, land_level=land_level, mountain_level=mountain_level)

for i in range(N):
    rootMap.generateMap(SIZE=SIZE, ZOOM=ZOOM, octaves=octaves, persistence=persistence, lacunarity=lacunarity, randomSeed=True)
    rootMap.vizMap(cmap=cmap, save=True)