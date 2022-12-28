import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def formula_3p(x):
    return 0.0107 * x ** 2 - 2.9979 * x + 174


def formula_5p(x):
    return 4.7189 * 10 ** -7 * x ** 4 - 0.00021171 * x ** 3 + 0.029586 * x ** 2 - 2.04492 * x + 174


def formula_np(xs, ys, x_all):
    n = len(xs)
    fs = [ys]
    ans = []
    for i in range(1, n):
        fs.append([])
        for j in range(1, i + 1):
            fs[j].append((fs[j - 1][i - j + 1] - fs[j - 1][i - j]) / (xs[i] - xs[i - j]))
    for x in x_all:
        temp = 0
        for i in range(n):
            num = 1
            for j in range(0, i):
                num *= x - xs[j]
            temp += fs[i][0] * num
        ans.append(temp)
    return ans


def approximation(x, y, x_all):
    sx = [np.sum(list(map(lambda num: num ** i, x))) for i in range(1, 5)]
    sy = np.array([np.sum(list(map(lambda j, k: k * j ** i, x, y))) for i in range(3)])
    m = np.array([[len(x), sx[0], sx[1]],
                 [sx[0], sx[1], sx[2]],
                 [sx[1], sx[2], sx[3]]])
    a = np.linalg.inv(m).dot(sy)
    return list(map(lambda num: a[0] + a[1] * num + a[2] * num ** 2, x_all))


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


def differentiation_1(x, y):
    ans = []
    for i in range(len(x) - 1):
        ans.append((y[i + 1] - y[i]) / (x[i + 1] - x[i]))
    return ans


def differentiation_2(x, y):
    ans = []
    for i in range(1, len(x)):
        ans.append((y[i] - y[i - 1]) / (x[i] - x[i - 1]))
    return ans


def differentiation_3(x, y):
    ans = []
    for i in range(1, len(x) - 1):
        ans.append((y[i + 1] - y[i - 1]) / (x[i + 1] - x[i - 1]))
    return ans


def integration_left(x, y):
    s = 0
    for i in range(len(x) - 1):
        s += y[i] * (x[i + 1] - x[i])
    return s


def integration_right(x, y):
    s = 0
    for i in range(len(x) - 1):
        s += y[i + 1] * (x[i + 1] - x[i])
    return s


def integration_middle(x, y):
    s = 0
    for i in range(len(x) - 1):
        s += (y[i] + y[i + 1]) / 2 * (x[i + 1] - x[i])
    return s


def integration_trapezoid(x, y):
    s = 0
    for i in range(len(x) - 1):
        s += (y[i] + y[i + 1]) * (x[i + 1] - x[i]) / 2
    return s


def integration_simpson(x, y):
    s = 0
    for i in range(len(x) - 2):
        s += (y[i] + 4 * y[i + 1] + y[i + 2]) * (x[i + 1] - x[i]) / 6
    return s


def main():
    pit = open("pit.txt")
    y_values = list(map(int, pit.read().split(" ")))
    x_pit_values = [2 * i for i in range(len(y_values))]
    # x_all_values = [i / 10 for i in range(2801)]

    # x_interpolation_nodes = [0, 204, 280]
    # y_interpolation_nodes = [174, 8, 174]
    # x_interpolation_nodes = [0, 204, 280, 136, 66]
    # y_interpolation_nodes = [174, 8, 174, 72, 116]
    # x_interpolation_nodes = [x_pit_values[int(i)] for i in np.linspace(0, len(y_values) - 1, 10)]
    # y_interpolation_nodes = [y_values[int(i)] for i in np.linspace(0, len(y_values) - 1, 10)]
    #
    # y_values_2 = list(map(formula_3p, x_all_values))
    # y_values_3 = list(map(formula_5p, x_all_values))
    # y_values_3 = formula_np(x_interpolation_nodes, y_interpolation_nodes, x_all_values)
    # y_values_4 = approximation(x_pit_values, y_values, x_all_values)
    # x_nodes = [x_pit_values[int(i)] for i in np.linspace(0, len(y_values) - 1, 15)]
    # y_nodes = [y_values[int(i)] for i in np.linspace(0, len(y_values) - 1, 15)]
    # y_values_5 = spline(x_nodes, y_nodes, x_all_values)
    y_values_6 = differentiation_1(x_pit_values, y_values)
    y_values_7 = differentiation_2(x_pit_values, y_values)
    y_values_8 = differentiation_3(x_pit_values, y_values)
    y_values_9 = differentiation_3(x_pit_values[1:-1], y_values_8)
    # n = len(x_pit_values) - 1
    # d1 = differentiation_3(x_pit_values, y_values)
    # d2 = differentiation_3(x_pit_values[1:-1], d1)
    # d3 = differentiation_3(x_pit_values[2:-2], d2)
    # d4 = differentiation_3(x_pit_values[3:-3], d3)
    # h = x_pit_values[n] - x_pit_values[0]
    # error = np.max(list(map(abs, d1))) * h ** 2 / (2 * n)
    # print(f"Левые {integration_left(x_pit_values, y_values)} Погрешность {error}")
    # print(f"Правые {integration_right(x_pit_values, y_values)} Погрешность {error}")
    # error = np.max(list(map(abs, d2))) * h ** 3 / (24 * n ** 2)
    # print(f"Средние {integration_middle(x_pit_values, y_values)} Погрешность {error}")
    # error = np.max(list(map(abs, d2))) * h ** 3 / (12 * n ** 2)
    # print(f"Трапеций {integration_trapezoid(x_pit_values, y_values)} Погрешность {error}")
    # error = np.max(list(map(abs, d4))) * h ** 5 / (2880 * n ** 4)
    # print(f"Симпсон {integration_simpson(x_pit_values, y_values)} Погрешность {error}")

    fig, ax = plt.subplots()
    # ax.scatter(x_interpolation_nodes, y_interpolation_nodes, label="Узлы интерполяции", color='red')
    # ax.scatter(x_interpolation_nodes, y_interpolation_nodes, label="Узлы аппроксимации", color='red')
    # ax.scatter(x_nodes, y_nodes, label="Узлы интерполяции", color='red')
    # ax.scatter(x_pit_values, y_values, label="Ручная оцифровка", s=10, color="purple")
    # ax.plot(x_all_values, y_values_2, label="Интерполяция")
    # ax.plot(x_all_values, y_values_3, label="Интерполяция")
    # ax.plot(x_all_values, y_values_4, label="Аппроксимация")
    # ax.plot(x_all_values, y_values_5, label="Сплайн")
    ax.plot(x_pit_values[:-1], y_values_6, label="Дифференцирование правосторонней разностью")
    ax.plot(x_pit_values[1:], y_values_7, label="Дифференцирование левосторонней разностью")
    ax.plot(x_pit_values[1:-1], y_values_8, label="Дифференцирование двусторонней разностью")
    ax.plot(x_pit_values[2:-2], y_values_9, label="Вторая производная")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
    ax.grid(which='major', color='gray')
    ax.grid(which='minor', color='gray', linestyle=':')
    ax.legend()
    plt.xlim([0, 280])
    # plt.ylim([0, 180])
    plt.xlabel("X", fontsize=14)
    plt.ylabel("Y", fontsize=14)
    plt.show()
    fig.savefig('figure8.svg')


if __name__ == "__main__":
    main()
