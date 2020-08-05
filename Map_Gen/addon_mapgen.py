import noise
import numpy as np
import scipy
from PIL import Image




def noise_generation():
    global shape = (1920, 1080)
    scale= 100.0
    octs = 6
    persistence = 0.5
    lanc = 2.0

    world = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            world[i][j] = noise.pnoise2(i/scale, j/scale, octaves=octs, persistence=persistence, lacunarity=lanc,
                                        repeatx= 1920, repeaty = 1080, base=0)
    Image.fromarray(world).show()
    return world

def add_colour():
    blue = [65, 105, 225]
    green = [34, 139, 34]
    beach = [238, 214, 175]

    def add_color(world):
        color_world = np.zeros(world.shape + (3,))
        for i in range(shape[0]):
            for j in range(shape[1]):
                if world[i][j] < -0.05:
                    color_world[i][j] = blue
                elif world[i][j] < 0:
                    color_world[i][j] = beach
                elif world[i][j] < 1.0:
                    color_world[i][j] = green

        return color_world

noise_generation()
