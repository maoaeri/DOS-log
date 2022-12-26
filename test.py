import plotext as plt
import numpy as np

n = 2
frames = 18
l = 30 * frames
f = 2 * np.pi / l
x = np.arange(0, l)
xticks = np.arange(0, l + l / (2 * n), l / (2 * n))
xlabels = [str(i) + "π" for i in range(2*(n+1))]
for i in range(frames):
    y = np.sin(n * f * x + 2 * np.pi / frames * i)
    plt.clear_terminal()
    plt.clear_data()
    plt.scatter(x, y)
    plt.ylim(-1, 1)
    # plt.canvas_size(150, 40)
    plt.title("plotting streaming data using plotext")
    plt.ticks_color("blue")
    plt.xticks(xticks, xlabels)
    plt.sleep(1)
    plt.show()