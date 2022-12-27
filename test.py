import plotext as plt
import numpy as np
from datetime import datetime, timedelta
import random
import log_analyze
import threading, time

def draw_plot():
    # n = 2
    # frames = 18
    # l = 30 * frames
    # f = 2 * np.pi / l

    x = np.arange(0, 19)
    n = 20
    # xticks = np.arange(0, l + l / (2 * n), l / (2 * n))
    time_now = datetime.now()
    xticks = np.arange(0, n - 1, 1)
    xlabels = [str((time_now - timedelta(seconds=i)).strftime("%H:%M:%S")) for i in range(n+1, 1, -1)]
    y = [0]*n
    # xlabels = [str(i) + "π" for i in range(2*(n+1))]
    # for i in range(frames):
    while True:
        # y = np.sin(n * f * x + 2 * np.pi / frames * i)
        # print(datetime.now(), log_analyze.times)
        time_now = datetime.now()
        y.pop(0)
        y.append(log_analyze.times.get((time_now - timedelta(seconds=1)).strftime("%H:%M:%S"), 0))
        plt.clear_terminal()
        plt.clear_data()
        xlabels.pop(0)
        xlabels.append((time_now - timedelta(seconds=1)).strftime("%H:%M:%S"))
        plt.plot(x, y)
        plt.ylim(0, max(y) + 10)
        # plt.canvas_size(150, 40)
        plt.title("plotting streaming data using plotext")
        plt.ticks_color("blue")
        plt.xticks(xticks, xlabels)
        plt.sleep(1)
        plt.show()

if __name__ == "__main__":

    print("hi")
    t1 = threading.Thread(target=log_analyze.access_handler)
    # time.sleep(1)
    t2 = threading.Thread(target=draw_plot)
    t1.start()
    time.sleep(2)

    t2.start()
    t1.join()
    t2.join()