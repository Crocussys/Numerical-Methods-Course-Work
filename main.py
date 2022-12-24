import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def formula_3p(x):
    return 0.0107 * x ** 2 - 2.9979 * x + 174


def formula_5p(x):
    return 4.7189 * 10 ** -7 * x ** 4 - 0.00021171 * x ** 3 + 0.029586 * x ** 2 - 2.04492 * x + 174


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
    ans = []
    for i in range(len(x) - 1):
        ans.append(y[i] * (x[i + 1] - x[i]))
    return ans


def integration_right(x, y):
    ans = []
    for i in range(len(x) - 1):
        ans.append(y[i + 1] * (x[i + 1] - x[i]))
    return ans


def integration_middle(x, y):
    ans = []
    for i in range(len(x) - 1):
        ans.append((y[i] + y[i + 1]) / 2 * (x[i + 1] - x[i]))
    return ans


def main():
    pit = open("pit.txt")
    y_values = list(map(int, pit.read().split(" ")))
    x_pit_values = [2 * i for i in range(len(y_values))]
    x_all_values = [i / 10 for i in range(2801)]

    # x_interpolation_nodes = [0, 204, 280]
    # y_interpolation_nodes = [174, 8, 174]
    # x_interpolation_nodes = [0, 204, 280, 136, 66]
    # y_interpolation_nodes = [174, 8, 174, 72, 116]
    #
    # y_values_2 = list(map(formula_3p, x_all_values))
    # y_values_3 = list(map(formula_5p, x_all_values))
    # y_values_4 = approximation(x_interpolation_nodes, y_interpolation_nodes, x_all_values)
    # x_nodes = [x_pit_values[i] for i in range(len(x_pit_values)) if i % (len(x_pit_values) // 28) == 0]
    # y_nodes = [y_values[i] for i in range(len(x_pit_values)) if i % (len(x_pit_values) // 28) == 0]
    # y_values_5 = spline(x_nodes, y_nodes, x_all_values)
    # y_values_6 = differentiation_1(x_pit_values, y_values)
    # y_values_7 = differentiation_2(x_pit_values, y_values)
    # y_values_8 = differentiation_3(x_pit_values, y_values)
    # y_values_9 = differentiation_3(x_pit_values[1:-1], y_values_8)
    y_values_10 = integration_left(x_pit_values, y_values)
    y_values_11 = integration_right(x_pit_values, y_values)
    y_values_12 = integration_right(x_pit_values, y_values)

    fig, ax = plt.subplots()
    # ax.scatter(x_interpolation_nodes, y_interpolation_nodes, label="Узлы интерполяции", color='red')
    # ax.scatter(x_nodes, y_nodes, label="Узлы аппроксимации", color='red')
    # ax.scatter(x_pit_values, y_values, label="Ручная оцифровка", s=10, color="purple")
    # ax.plot(x_all_values, y_values_2, label="Интерполяция")
    # ax.plot(x_all_values, y_values_3, label="Интерполяция")
    # ax.plot(x_all_values, y_values_4, label="Аппроксимация")
    # ax.plot(x_all_values, y_values_5, label="Сплайн")
    # ax.plot(x_pit_values[:-1], y_values_6, label="Дифференцирование 1")
    # ax.plot(x_pit_values[1:], y_values_7, label="Дифференцирование 2")
    # ax.plot(x_pit_values[1:-1], y_values_8, label="Дифференцирование 3")
    # ax.plot(x_pit_values[2:-2], y_values_9, label="Дифференцирование x2")
    ax.plot(x_pit_values[:-1], y_values_10, label="Интегрирование левыми")
    ax.plot(x_pit_values[:-1], y_values_11, label="Интегрирование правыми")
    ax.plot(x_pit_values[:-1], y_values_12, label="Интегрирование средними")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.grid(which='major', color='gray')
    ax.grid(which='minor', color='gray', linestyle=':')
    ax.legend()
    plt.xlim([0, 280])
    # plt.ylim([0, 180])
    # plt.title("Отцифрованная ямка", fontsize=14)
    plt.xlabel("X мм", fontsize=14)
    plt.ylabel("Y мм", fontsize=14)
    plt.show()


if __name__ == "__main__":
    main()
