import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import numpy as np


def spline(x_all):
    len_nodes = len(x_nodes) - 1
    a = x_nodes[0]
    b = x_nodes[len_nodes]
    h = (b - a) / len_nodes
    ans = []
    ms = [(4 * y_nodes[1] - y_nodes[2] - 3 * y_nodes[0]) / (2 * h)]
    for i in range(1, len_nodes):
        ms.append((y_nodes[i + 1] - y_nodes[i - 1]) / (2 * h))
    ms.append((3 * y_nodes[len_nodes] - y_nodes[len_nodes - 2] - 3 * y_nodes[len_nodes - 1]) / (2 * h))
    for i in range(len_nodes):
        x_slice = []
        for j in range(len(x_all)):
            if i + 1 < len_nodes:
                if x_nodes[i] <= x_all[j] < x_nodes[i + 1]:
                    x_slice.append(x_all[j])
            else:
                if x_nodes[i] <= x_all[j] <= x_nodes[i + 1]:
                    x_slice.append(x_all[j])
        temp = list(map(lambda s: (((x_nodes[i + 1] - s) ** 2) * (2 * (s - x_nodes[i]) + h)) / (h ** 3) * y_nodes[i] +
                                  (((s - x_nodes[i]) ** 2) * (2 * (x_nodes[i + 1] - s) + h)) /
                                  (h ** 3) * y_nodes[i + 1] +
                                  (((x_nodes[i + 1] - s) ** 2) * (s - x_nodes[i])) / (h ** 2) * ms[i] +
                                  (((s - x_nodes[i]) ** 2) * (s - x_nodes[i + 1])) / (h ** 2) * ms[i + 1], x_slice))
        for j in range(len(temp)):
            ans.append(temp[j])
    return ans


def animate(i):
    scat.set_offsets((t[i], spline([t[i]])[0]))
    return scat,


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

fig, ax = plt.subplots()
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.grid(which='major', color='gray')
ax.grid(which='minor', color='gray', linestyle=':')
# ax.legend()
plt.xlim([0, 280])
plt.ylim([0, 180])
plt.xlabel("X мм", fontsize=14)
plt.ylabel("Y мм", fontsize=14)

y_values = spline(x_all_values)
ax.plot(x_all_values, y_values, label="Траектория")
x = int(input("Введите начальное положение "))
scat = ax.scatter(x, spline([x])[0])
t = np.linspace(0., 280., num=280)

ani = animation.FuncAnimation(fig, animate, repeat=False, frames=len(t) - 1, interval=0)
plt.show()
