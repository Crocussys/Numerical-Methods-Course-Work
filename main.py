import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


def formula_3p(x):
    return 166 / 15631 * x ** 2 - 6640 / 2233 * x + 174


def formula_5p(x):
    return 13991221 / 29475904402560 * x ** 4 - 6279797609 / 29475904402560 * x ** 3 + 438718547539 / 14737952201280 *\
           x ** 2 - 108002745479 / 52635543576 * x + 174


def approximation(x, y, x_all):
    sx = [np.sum(list(map(lambda num: num ** i, x))) for i in range(1, 5)]
    sy = np.array([np.sum(list(map(lambda j, k: k * j ** i, x, y))) for i in range(3)])
    m = np.array([[len(x), sx[0], sx[1]],
                 [sx[0], sx[1], sx[2]],
                 [sx[1], sx[2], sx[3]]])
    a = np.linalg.inv(m).dot(sy)
    return list(map(lambda num: a[0] + a[1] * num + a[2] * num ** 2, x_all))


def main():
    pit = open("pit.txt")
    y_values = list(map(int, pit.read().split(" ")))
    x_pit_values = [2 * i for i in range(len(y_values))]
    x_all_values = [i / 10 for i in range(2801)]

    x_interpolation_nodes = [0, 203, 280, 136, 66]
    y_interpolation_nodes = [174, 8, 174, 72, 116]

    y_values_2 = list(map(formula_3p, x_all_values))
    y_values_3 = list(map(formula_5p, x_all_values))
    y_values_4 = approximation(np.array(x_pit_values), np.array(y_values), x_all_values)

    fig, ax = plt.subplots()
    ax.scatter(x_interpolation_nodes, y_interpolation_nodes, label="Узлы интерполяции", color='red')
    ax.scatter(x_pit_values, y_values, label="Ручная отцифровка", s=10, color="purple")
    ax.plot(x_all_values, y_values_2, label="Полином Лагранжа по трём точкам")
    ax.plot(x_all_values, y_values_3, label="Полином Лагранжа по пяти точкам")
    ax.plot(x_all_values, y_values_4, label="Аппроксимация")

    ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.grid(which='major', color='gray')
    ax.grid(which='minor', color='gray', linestyle=':')
    ax.legend()
    plt.xlim([0, 280])
    plt.ylim([-40, 180])
    # plt.title("Отцифрованная ямка", fontsize=14)
    plt.xlabel("X мм", fontsize=14)
    plt.ylabel("Y мм", fontsize=14)
    plt.show()


if __name__ == "__main__":
    main()
