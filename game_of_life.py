import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from msgbox import MsgBox


class Cell(MsgBox):
    def __init__(self, alive=False):
        super().__init__()
        self._alive = alive
        self._nb = []

    def handle(self, msg):
        if msg[0] == "add":
            self._nb.append(msg[1])
        elif msg[0] == 'alive':
            self._alive = msg[1]
        elif msg[0] == 'update':
            for
        else:
            pass


if __name__ == "__main__":
    cells = [[Cell() for y in range(100)] for x in range(100)]
    print('est')
    for x, row in enumerate(cells):
        for y, cell in enumerate(row):
            if y - 1 > 0:
                cell.post(('add', cells[x][y - 1]))
            if y + 1 < len(row):
                cell.post(('add', cells[x][y + 1]))
            if x - 1 > 0:
                cell.post(('add', cells[x - 1][y]))
            if x + 1 < len(cells):
                cell.post(('add', cells[x + 1][y]))
            if x - 1 > 0 and y - 1 > 0:
                cell.post(('add', cells[x - 1][y - 1]))
            if x + 1 < len(cells) and y + 1 < len(row):
                cell.post(('add', cells[x + 1][y + 1]))
            if x - 1 > 0 and y + 1 < len(row):
                cell.post(('add', cells[x - 1][y + 1]))
            if x + 1 < len(cells) and y - 1 > 0:
                cell.post(('add', cells[x + 1][y - 1]))

    cells[50][51].post(('alive', True))
    cells[51][51].post(('alive', True))
    cells[52][51].post(('alive', True))

    fig, ax = plt.subplots()

    scat = ax.scatter([50, 51, 52], [51, 51, 51], s=5)
    ax.xticks(range(100))
    ax.yticks(range(100))

    def update(frame):
        for x in range(100):
            for y in range(100):
                cells[x][y].post('update')
        scat.set_offsets()
        return scat


    ani = animation.FuncAnimation(fig=fig, func=update, frames=40, interval=30)

    plt.show()
