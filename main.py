import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def formula(x):
    return 166 / 15631 * x ** 2 - 6640 / 2233 * x + 174


def main():
    pit = open("pit.txt")
    y_values = list(map(int, pit.read().split(" ")))
    x_values = [2 * i for i in range(len(y_values))]

    x_values_2 = [i / 10 for i in range(2801)]
    y_values_2 = list(map(formula, x_values_2))

    fig, ax = plt.subplots()
    ax.plot(x_values, y_values, label="Ручная отцифровка")
    ax.plot(x_values_2, y_values_2, label="Полином Лагранжа")

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
