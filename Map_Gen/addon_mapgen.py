from opensimplex import OpenSimplex

def get_noise():
    tmp = OpenSimplex()
    print(tmp.noise2d(x=10, y=10))

get_noise()