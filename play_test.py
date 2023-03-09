import matplotlib.pyplot as plt
from dancer.game import DANCER

game = DANCER()
state, _, _ = game.play(-1)

for i in range(10):
    pos = i - i//4*4
    game.play(pos+1)


# game.play(1)
# game.play(2)
# game.play(3)
# game.play(4)
# game.play(0)
