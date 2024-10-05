import plotext as plt
import numpy as np
from datetime import datetime, timedelta
import random
import log_analyze
import threading, time

def draw_plot():

    x = np.arange(0, 19)
    n = 20
    time_now = datetime.now()
    xticks = np.arange(0, n - 1, 1)
    xlabels = [str((time_now - timedelta(seconds=i)).strftime("%H:%M:%S")) for i in range(n+1, 1, -1)]
    y = [0]*n
    while True:
        for i in range(len(log_analyze.errors)):
            print(log_analyze.errors[i])
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
        plt.title("Plotting incoming requests")
        plt.ticks_color("blue")
        plt.xticks(xticks, xlabels)
        plt.sleep(1)
        plt.show()

if __name__ == "__main__":

    t1 = threading.Thread(target=log_analyze.access_handler)
    # time.sleep(1)
    t2 = threading.Thread(target=draw_plot)
    t3 = threading.Thread(target=log_analyze.error_handler)
    t1.start()
    t3.start()
    time.sleep(2)

    t2.start()
    t1.join()
    t2.join()
    t3.join()