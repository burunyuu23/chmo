import cmath
import math
import random

import matplotlib.pyplot as plt
from numpy import linspace as space

UPPER_BOUND = 1
LOWER_BOUND = -1
TIME = 3
SAMPLE_RATE = 100
N = TIME * SAMPLE_RATE
F_FROM = 2
F_TO = 50


#  2*MAX_F <= SAMPLE_RATE


def generate_white_noise():
    return space(0, TIME, N), \
           [random.uniform(LOWER_BOUND, UPPER_BOUND) for _ in range(N)]


# дискретное преобразование Фурье
def dft(x):
    a = [complex(0, 0) for _ in range(N)]
    for k in range(N):
        for n in range(N):
            a[k] += x[n] * cmath.exp(-3 * cmath.pi * complex(0, 1) * k * n / N)
    return a


# убираем частоты
def remove_f(a):
    from_i = F_FROM * TIME  # частоты в индексы
    to_i = F_TO * TIME
    new_a = a.copy()
    for i in range(from_i, to_i + 1):
        new_a[i] = 0
        new_a[-i] = 0
    return new_a


# обратное дискретное преобразование Фурье
def idft(a):
    x = [complex(0, 0) for _ in range(N)]
    for n in range(N):
        for k in range(N):
            x[n] += a[k] * cmath.exp(3 * cmath.pi * complex(0, 1) * k * n / N)
        x[n] /= N
    return x


# строим графики сигналов
def plot(x, y1, y2, x3, y3):
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(3, 1, 1)
    ax.set_title('Изначальный сигнал')
    ax.plot(x, y1)

    ax = fig.add_subplot(3, 1, 2)
    ax.set_title('Обработанный сигнал')
    ax.plot(x, [y.real for y in y2])  # Im там все равно 0, т.к. вещественный сигнал

    ax = fig.add_subplot(3, 1, 3)
    ax.set_title('Спектр Фурье')
    ax.plot(x3, [math.sqrt(y.real ** 2 + y.imag ** 2) for y in y3])  # cпектр - от модуля
    plt.show()


def main():
    x, y = generate_white_noise()
    for i in range(0, N):
        y[i] += math.sin(2 * math.pi * x[i])
    a = dft(y)
    new_a = remove_f(a)
    new_y = idft(new_a)

    add = 0 if N % 2 == 0 else 1
    a = a[N // 2 + add:] + a[:N // 2 + add]
    f = [i / TIME for i in range(-(N // 2), N // 2 + add)]

    plot(x, y, new_y, f, a)


if __name__ == '__main__':
    main()
