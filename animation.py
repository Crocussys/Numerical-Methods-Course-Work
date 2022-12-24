import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from time import time


def spline(x, y, x_all):
    n = len(x) - 1
    a = x[0]
    b = x[n]
    h = (b - a) / n
    ans = []
    ms = [(4 * y[1] - y[2] - 3 * y[0]) / (2 * h)]
    for i in range(1, n):
        ms.append((y[i + 1] - y[i - 1]) / (2 * h))
    ms.append((3 * y[n] - y[n - 2] - 3 * y[n - 1]) / (2 * h))
    for i in range(n):
        x_slice = []
        for j in range(len(x_all)):
            if i + 1 < n:
                if x[i] <= x_all[j] < x[i + 1]:
                    x_slice.append(x_all[j])
            else:
                if x[i] <= x_all[j] <= x[i + 1]:
                    x_slice.append(x_all[j])
        temp = list(map(lambda s: (((x[i + 1] - s) ** 2) * (2 * (s - x[i]) + h)) / (h ** 3) * y[i] +
                                  (((s - x[i]) ** 2) * (2 * (x[i + 1] - s) + h)) / (h ** 3) * y[i + 1] +
                                  (((x[i + 1] - s) ** 2) * (s - x[i])) / (h ** 2) * ms[i] +
                                  (((s - x[i]) ** 2) * (s - x[i + 1])) / (h ** 2) * ms[i + 1], x_slice))
        for j in range(len(temp)):
            ans.append(temp[j])
    return ans


def y_from_x(x_spline, y_spline, x):
    if x < 0:
        x = 0
    if x > 280:
        x = 280
    return spline(x_spline, y_spline, [x])[0]


def main():
    pit = open("pit.txt")
    y_values_pit = list(map(int, pit.read().split(" ")))
    n = len(y_values_pit)
    x_pit_values = [2 * i for i in range(n)]
    x_all_values = [i / 10 for i in range(2801)]
    x_nodes = []
    y_nodes = []
    for i in range(n):
        if i % (n // 28) == 0:
            x_nodes.append(x_pit_values[i])
            y_nodes.append(y_values_pit[i])
    y_values = spline(x_nodes, y_nodes, x_all_values)
    fig, ax = plt.subplots()
    ax.plot(x_all_values, y_values, label="Траектория")
    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.grid(which='major', color='gray')
    ax.grid(which='minor', color='gray', linestyle=':')
    ax.legend()
    plt.xlim([0, 280])
    plt.ylim([0, 180])
    plt.xlabel("X мм", fontsize=14)
    plt.ylabel("Y мм", fontsize=14)
    x = int(input("Введите начальное положение "))
    y = y_from_x(x_nodes, y_nodes, x)
    point = ax.scatter(x, y, color='red')
    # v = int(input("Введите начальную скорость "))
    first = True
    t = 0
    while True:
        v = (y_from_x(x_nodes, y_nodes, x - 0.1) - y_from_x(x_nodes, y_nodes, x + 0.1)) / 0.2
        v1 = (y_from_x(x_nodes, y_nodes, x - 0.2) - y_from_x(x_nodes, y_nodes, x)) / 0.2
        v2 = (y_from_x(x_nodes, y_nodes, x) - y_from_x(x_nodes, y_nodes, x + 0.2)) / 0.2
        a = (v2 - v1) / 0.2
        if first:
            first = False
            t = time()
        t = time() - t
        x = x + v * t + a * t ** 2 / 2
        y = y_from_x(x_nodes, y_nodes, x)
        point.clear()
        point = ax.scatter(x, y, color='red')
        plt.draw()
        plt.gcf().canvas.flush_events()


if __name__ == "__main__":
    main()
