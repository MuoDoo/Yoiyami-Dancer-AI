import matplotlib.pyplot as plt
from dancer.game import DANCER

game = DANCER()
state, _, _ = game.play(-1)
plt.imshow(state)
plt.savefig("shot.png")
