import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import numpy as np

g = 10
fps = 60


def spline(xs, ys, x_all):
    len_nodes = len(xs) - 1
    h = (xs[len_nodes] - xs[0]) / len_nodes
    ans = []
    ms = [(4 * ys[1] - ys[2] - 3 * ys[0]) / (2 * h)]
    for i in range(1, len_nodes):
        ms.append((ys[i + 1] - ys[i - 1]) / (2 * h))
    ms.append((3 * ys[len_nodes] - ys[len_nodes - 2] - 3 * ys[len_nodes - 1]) / (2 * h))
    for i in range(len_nodes):
        x_slice = []
        for j in range(len(x_all)):
            if i + 1 < len_nodes:
                if xs[i] <= x_all[j] < xs[i + 1]:
                    x_slice.append(x_all[j])
            else:
                if xs[i] <= x_all[j] <= xs[i + 1]:
                    x_slice.append(x_all[j])
        temp = list(map(lambda s: (((xs[i + 1] - s) ** 2) * (2 * (s - xs[i]) + h)) / (h ** 3) * ys[i] +
                                  (((s - xs[i]) ** 2) * (2 * (xs[i + 1] - s) + h)) / (h ** 3) * ys[i + 1] +
                                  (((xs[i + 1] - s) ** 2) * (s - xs[i])) / (h ** 2) * ms[i] +
                                  (((s - xs[i]) ** 2) * (s - xs[i + 1])) / (h ** 2) * ms[i + 1], x_slice))
        for j in range(len(temp)):
            ans.append(temp[j])
    return ans


def differentiation_in_point(xs, ys, point):
    size = len(xs)
    ans = []
    if size < 3 or len(ys) < 3:
        raise
    for i in range(1, size - 1):
        ans.append((ys[i + 1] - ys[i - 1]) / (xs[i + 1] - xs[i - 1]))
    x_sp = [xs[int(i)] for i in np.linspace(1, size - 1, 15)]
    y_sp = [ans[int(i)] for i in np.linspace(0, size - 3, 15)]
    s = spline(x_sp, y_sp, [point])
    return s[0]


def animate(i, sx, sy):
    frame = frames[i]
    sx.append(frame[0])
    sy.append(frame[1])
    scat.set_offsets(frame)
    p.set_data(sx, sy)
    return scat, p


pit = open("pit.txt")
y_values_pit = list(map(int, pit.read().split(" ")))
n = len(y_values_pit)
x_pit_values = [2 * i for i in range(n)]
x_all_values = [i / 10 for i in range(2801)]
x_nodes = [x_pit_values[int(i)] for i in np.linspace(0, len(y_values_pit) - 1, 15)]
y_nodes = [y_values_pit[int(i)] for i in np.linspace(0, len(y_values_pit) - 1, 15)]

fig, axis = plt.subplots()
axis.xaxis.set_major_locator(ticker.MultipleLocator(10))
axis.xaxis.set_minor_locator(ticker.MultipleLocator(5))
axis.yaxis.set_major_locator(ticker.MultipleLocator(10))
axis.yaxis.set_minor_locator(ticker.MultipleLocator(5))
axis.grid(which='major', color='gray')
axis.grid(which='minor', color='gray', linestyle=':')
plt.xlim([0, 280])
plt.ylim([0, 180])
plt.xlabel("X мм", fontsize=14)
plt.ylabel("Y мм", fontsize=14)

f, z = plt.subplots()
z.xaxis.set_major_locator(ticker.MultipleLocator(1))
z.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
z.yaxis.set_major_locator(ticker.MultipleLocator(10))
z.yaxis.set_minor_locator(ticker.MultipleLocator(5))
z.grid(which='major', color='gray')
z.grid(which='minor', color='gray', linestyle=':')

y_values = spline(x_nodes, y_nodes, x_all_values)
axis.plot(x_all_values, y_values, label="Траектория")
x0 = int(input("Введите начальное положение "))
v0 = int(input("Введите начальную скорость "))
a = differentiation_in_point(x_all_values, y_values, x0)
y = spline(x_nodes, y_nodes, [x0])[0]
t = 1 / fps
frames = [(x0, y)]
v = v0
x_new = x0 + v * t
x = x0
vs = []
ts = []
time = t
for _ in range(fps * 23):
    x = x_new
    y = spline(x_nodes, y_nodes, [x])[0]
    frames.append((x, y))
    vs.append(v)
    ts.append(time)
    print(f"x = {x} dif = {a} v = {v} y = {y}")
    a = differentiation_in_point(x_all_values, y_values, x)
    v -= a * g * t
    x_new = x + v * t
    time += t

scat = axis.scatter([], [], label="Точка", color="red")
p = axis.plot([], [], label="Пройденное расстояние", alpha=0.5, color="r")[0]
z.plot(ts, vs)
axis.legend()
ani = animation.FuncAnimation(fig, animate, repeat=True, frames=len(frames) - 1, interval=1000/fps, blit=True,
                              fargs=([], []))
plt.show()
