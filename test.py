import plotext as plt
import numpy as np
from datetime import datetime, timedelta
import random

n = 2
frames = 18
l = 30 * frames
f = 2 * np.pi / l
x = np.arange(0, 19)
# xticks = np.arange(0, l + l / (2 * n), l / (2 * n))
time_now = datetime.now()
xticks = np.arange(0, 19, 1)
xlabels = [str((time_now - timedelta(seconds=i)).strftime("%H:%M:%S")) for i in range(20,0, -1)]
# xlabels = [str(i) + "π" for i in range(2*(n+1))]
# for i in range(frames):
while True:
    # y = np.sin(n * f * x + 2 * np.pi / frames * i)
    y = [random.randint(1, 10) for i in range(len(x))]
    plt.clear_terminal()
    plt.clear_data()
    xlabels.pop(0)
    xlabels.append(datetime.now().strftime("%H:%M:%S"))
    plt.plot(x, y)
    plt.ylim(0, 11)
    # plt.canvas_size(150, 40)
    plt.title("plotting streaming data using plotext")
    plt.ticks_color("blue")
    plt.xticks(xticks, xlabels)
    plt.sleep(1)
    plt.show()