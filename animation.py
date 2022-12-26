import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import numpy as np

g = 10
m = 1
fps = 300
nu = 0


def spline(x_all):
    len_nodes = len(x_nodes) - 1
    h = (x_nodes[len_nodes] - x_nodes[0]) / len_nodes
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


def differentiation_in_point(xs, ys, point):
    for i in range(1, len(xs)):
        if point - xs[i] < 0:
            return (ys[i] - ys[i - 1]) / (xs[i] - xs[i - 1])
    raise


def sign(elem):
    if elem >= 0:
        return -1
    else:
        return 1


def animate(i):
    scat.set_offsets(frames[i])
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

fig, axis = plt.subplots()
axis.xaxis.set_major_locator(ticker.MultipleLocator(10))
axis.xaxis.set_minor_locator(ticker.MultipleLocator(5))
axis.yaxis.set_major_locator(ticker.MultipleLocator(10))
axis.yaxis.set_minor_locator(ticker.MultipleLocator(5))
axis.grid(which='major', color='gray')
axis.grid(which='minor', color='gray', linestyle=':')
# ax.legend()
plt.xlim([0, 280])
plt.ylim([0, 180])
plt.xlabel("X мм", fontsize=14)
plt.ylabel("Y мм", fontsize=14)

y_values = spline(x_all_values)
axis.plot(x_all_values, y_values, label="Траектория")
x = int(input("Введите начальное положение "))
v = int(input("Введите начальную скорость "))
tg_a = differentiation_in_point(x_all_values, y_values, x)
cos_a = np.sqrt(1 / (1 + tg_a ** 2))
vx = - v * cos_a
vy = v * tg_a * cos_a
y0 = spline([x])[0]
energy = m * g * y0
ax = -1 * g * (1 / tg_a)
t = 1 / fps
frames = [(x, y0)]
x_new = x + vx * t + (ax * t ** 2) / 2
y_prev = y0
while np.abs(x_new - x) > 0.000001 and 0 <= x_new <= 280:
    x = x_new
    y = spline([x])[0]
    frames.append((x, y))
    tg_a = differentiation_in_point(x_all_values, y_values, x)
    vy_new = np.sqrt(2 * (energy / m - g * y))
    ay = (vy_new - vy) / t
    if x_new - x >= 0 and y_prev - y >= 0:
        ax = (g + ay) * ((nu + 1) / (nu - 1)) * (1 / tg_a)
    elif x_new - x < 0 and y_prev - y < 0:
        nu_coef = ((nu - 1) / (nu + 1))
        ax = (g + ay) * ((nu + 1) / (nu - 1)) * (1 / tg_a)
    elif x_new - x >= 0 and y_prev - y < 0:
        ax = (ay - g) * ((nu + 1) / (nu - 1)) * tg_a
    else:
        ax = (ay - g) * ((nu + 1) / (nu - 1)) * tg_a
    # ax = sign(tg_a) * (g + ay) * ((nu + 1) / (nu - 1)) * (1 / tg_a)
    vx += ax * t
    x_new = x + vx * t + (ax * t ** 2) / 2
    y_prev = y
    print(f"x = {x_new} tg_a = {tg_a} vy = {vy_new} ay = {ay} ax = {ax} vx = {vx} y = {y}")

scat = axis.scatter([], [])
ani = animation.FuncAnimation(fig, animate, repeat=True, frames=len(frames) - 1, interval=1000/fps, blit=True)
plt.show()
