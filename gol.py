import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from scipy.signal import convolve2d


con = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]])


def game_of_life(state):
    nghbd = convolve2d(state, con, mode='same')
    state = (state*(nghbd == 2) + (nghbd == 3))
    return state


def init(n):
    state = np.random.choice(a=[False, True], size=(n, n))*1

    def _update(frame):
        nonlocal state
        state = game_of_life(state*1)
        img.set_array(state)
        return img

    return state, _update


if __name__ == "__main__":
    fig, ax = plt.subplots()
    fig.set_figwidth(19.2)
    fig.set_figheight(10.8)

    s, update = init(100)
    img = ax.imshow(s, interpolation='nearest', cmap='gray')

    ani = animation.FuncAnimation(
        fig=fig, func=update, frames=320, interval=30, blit=True)

    #ani.save('test.mp4')
    plt.show()
