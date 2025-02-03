import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# Fixing random state for reproducibility
np.random.seed(19680801)

mpl.rcParams.update({
        # NOTE: don't call tight_layout manually anymore. See warning here:
        # https://matplotlib.org/stable/users/explain/axes/constrainedlayout_guide.html
        "figure.constrained_layout.use": True,
        #"savefig.bbox": "tight",
})

def randrange(n, vmin, vmax):
    """
    Helper function to make an array of random numbers having shape (n, )
    with each number distributed Uniform(vmin, vmax).
    """
    return (vmax - vmin)*np.random.rand(n) + vmin

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

n = 100

# For each set of style and range settings, plot n random points in the box
# defined by x in [23, 32], y in [0, 100], z in [zlow, zhigh].
for m, zlow, zhigh in [('o', -50, -25), ('^', -30, -5)]:
    xs = randrange(n, 23, 32)
    ys = randrange(n, 0, 100)
    zs = randrange(n, zlow, zhigh)
    ax.scatter(xs, ys, zs, marker=m)

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.savefig("bla.png")

#plt.show()
