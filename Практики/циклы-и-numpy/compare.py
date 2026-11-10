import math
import sys
import time

import numpy as np


def measure(fn, *args):
    best = float("inf")
    result = None
    for _ in range(3):
        t0 = time.perf_counter()
        result = fn(*args)
        best = min(best, time.perf_counter() - t0)
    return result, best


def show(t_loop, t_numpy, same):
    print(f"цикл:      {t_loop * 1000:10.2f} мс")
    print(f"NumPy:     {t_numpy * 1000:10.2f} мс")
    print(f"ускорение: {t_loop / t_numpy:.1f}×")
    print(f"результаты совпадают: {same}")


def task1():
    print("\nЗадача 1. Сумма массива")

    def loop_sum(a):
        total = 0.0
        for x in a:
            total += x
        return total

    def numpy_sum(a):
        return a.sum()

    rng = np.random.default_rng(42)
    print(f"{'n':>10} {'цикл, мс':>12} {'NumPy, мс':>12} {'ускорение':>12} {'совпало':>8}")
    for n in (10**5, 10**6, 10**7):
        a = rng.normal(size=n)
        r_loop, t_loop = measure(loop_sum, a)
        r_numpy, t_numpy = measure(numpy_sum, a)
        same = bool(np.isclose(r_loop, r_numpy))
        print(
            f"{n:10d} {t_loop * 1000:12.2f} {t_numpy * 1000:12.2f} "
            f"{t_loop / t_numpy:11.1f}× {str(same):>8}"
        )


def task2():
    print("\nЗадача 2. Среднее и стандартное отклонение")

    def loop_mean_std(a):
        n = len(a)
        total = 0.0
        total_sq = 0.0
        for x in a:
            total += x
            total_sq += x * x
        mean = total / n
        var = total_sq / n - mean * mean
        if var < 0:
            var = 0.0
        return mean, math.sqrt(var)

    def numpy_mean_std(a):
        return float(a.mean()), float(a.std())

    a = np.random.default_rng(42).normal(size=10**6)
    (mean_l, std_l), t_loop = measure(loop_mean_std, a)
    (mean_n, std_n), t_numpy = measure(numpy_mean_std, a)
    same = abs(mean_l - mean_n) < 1e-12 and abs(std_l - std_n) < 1e-12
    show(t_loop, t_numpy, same)
    print(f"mean  цикл {mean_l:.12f}  NumPy {mean_n:.12f}  |разница| {abs(mean_l - mean_n):.3e}")
    print(f"std   цикл {std_l:.12f}  NumPy {std_n:.12f}  |разница| {abs(std_l - std_n):.3e}")


def task3():
    print("\nЗадача 3. sin(x) + x^2")

    def loop_y(a):
        out = []
        for x in a:
            x = float(x)
            out.append(math.sin(x) + x * x)
        return out

    def numpy_y(a):
        return np.sin(a) + a**2

    a = np.random.default_rng(42).normal(size=10**6)
    r_loop, t_loop = measure(loop_y, a)
    r_numpy, t_numpy = measure(numpy_y, a)
    show(t_loop, t_numpy, bool(np.allclose(r_loop, r_numpy)))
    mem_loop = sys.getsizeof(r_loop)
    for item in r_loop:
        mem_loop += sys.getsizeof(item)
    print(f"память списка:  {mem_loop / 1024**2:.2f} МиБ")
    print(f"память массива: {r_numpy.nbytes / 1024**2:.2f} МиБ")


def task4():
    print("\nЗадача 4. Clip в [0, 1]")

    def loop_clip(a):
        out = np.empty_like(a)
        for i in range(len(a)):
            x = a[i]
            if x < 0:
                out[i] = 0.0
            elif x > 1:
                out[i] = 1.0
            else:
                out[i] = x
        return out

    def numpy_clip(a):
        return np.clip(a, 0, 1)

    a = np.random.default_rng(42).normal(size=10**6)
    changed = int(np.sum((a < 0) | (a > 1)))
    r_loop, t_loop = measure(loop_clip, a)
    r_numpy, t_numpy = measure(numpy_clip, a)
    show(t_loop, t_numpy, bool(np.allclose(r_loop, r_numpy)))
    print("элементов изменено:", changed)


def task5():
    print("\nЗадача 5. Сумма по строкам")

    def loop_sum_rows(m):
        result = [0.0] * m.shape[0]
        for i in range(m.shape[0]):
            s = 0.0
            for j in range(m.shape[1]):
                s += m[i, j]
            result[i] = s
        return result

    def numpy_sum_rows(m):
        return m.sum(axis=1)

    m = np.random.default_rng(42).normal(size=(10**5, 10))
    r_loop, t_loop = measure(loop_sum_rows, m)
    r_numpy, t_numpy = measure(numpy_sum_rows, m)
    show(t_loop, t_numpy, bool(np.allclose(r_loop, r_numpy)))
    print("строк в цикле: 7, в NumPy: 1")


def task6():
    print("\nЗадача 6. Среднее по столбцам")

    def loop_center(m):
        rows, cols = m.shape
        means = [0.0] * cols
        for j in range(cols):
            s = 0.0
            for i in range(rows):
                s += m[i, j]
            means[j] = s / rows
        out = np.empty_like(m)
        for i in range(rows):
            for j in range(cols):
                out[i, j] = m[i, j] - means[j]
        return out

    def numpy_center(m):
        return m - m.mean(axis=0)

    m = np.random.default_rng(42).normal(size=(10**5, 10))
    r_loop, t_loop = measure(loop_center, m)
    r_numpy, t_numpy = measure(numpy_center, m)
    show(t_loop, t_numpy, bool(np.allclose(r_loop, r_numpy)))


def task7():
    print("\nЗадача 7. Максимум и индекс")

    def loop_argmax(a):
        max_val = a[0]
        max_idx = 0
        for i in range(1, len(a)):
            if a[i] > max_val:
                max_val = a[i]
                max_idx = i
        return float(max_val), int(max_idx)

    def numpy_argmax(a):
        return float(a.max()), int(a.argmax())

    a = np.random.default_rng(42).normal(size=10**6)
    r_loop, t_loop = measure(loop_argmax, a)
    r_numpy, t_numpy = measure(numpy_argmax, a)
    same = r_loop[1] == r_numpy[1] and bool(np.isclose(r_loop[0], r_numpy[0]))
    print(f"цикл:  значение {r_loop[0]:.6f}, индекс {r_loop[1]}")
    print(f"NumPy: значение {r_numpy[0]:.6f}, индекс {r_numpy[1]}")
    show(t_loop, t_numpy, same)


def task8():
    print("\nЗадача 8. Фильтр x > 0")

    def loop_positive(a):
        return [x for x in a if x > 0]

    def numpy_positive(a):
        return a[a > 0]

    a = np.random.default_rng(42).normal(size=10**6)
    r_loop, t_loop = measure(loop_positive, a)
    r_numpy, t_numpy = measure(numpy_positive, a)
    show(t_loop, t_numpy, bool(np.allclose(r_loop, r_numpy)))
    mem_loop = sys.getsizeof(r_loop)
    for item in r_loop:
        mem_loop += sys.getsizeof(item)
    print("элементов:", len(r_loop))
    print(f"список: {mem_loop / 1024**2:.2f} МиБ, {mem_loop / len(r_loop):.1f} байт на элемент")
    print(f"массив: {r_numpy.nbytes / 1024**2:.2f} МиБ, 8 байт на элемент")


def task9():
    print("\nЗадача 9. Модуль на месте")

    def loop_abs(a):
        for i in range(len(a)):
            if a[i] < 0:
                a[i] = -a[i]
        return a

    def numpy_abs(a):
        a[a < 0] *= -1
        return a

    a = np.random.default_rng(42).normal(size=10**6)

    def best_of_copies(fn):
        best = float("inf")
        result = None
        for _ in range(3):
            copy = a.copy()
            t0 = time.perf_counter()
            result = fn(copy)
            best = min(best, time.perf_counter() - t0)
        return result, best

    r_loop, t_loop = best_of_copies(loop_abs)
    r_numpy, t_numpy = best_of_copies(numpy_abs)
    show(t_loop, t_numpy, bool(np.allclose(r_loop, r_numpy)) and bool(np.all(r_loop >= 0)))


def task10():
    print("\nЗадача 10. Маска -1 < x < 1")

    def loop_band(a):
        return [x for x in a if -1 < x < 1]

    def numpy_band(a):
        return a[(a > -1) & (a < 1)]

    a = np.random.default_rng(42).normal(size=10**6)
    r_loop, t_loop = measure(loop_band, a)
    r_numpy, t_numpy = measure(numpy_band, a)
    show(t_loop, t_numpy, bool(np.allclose(r_loop, r_numpy)))
    print("элементов:", len(r_numpy))
    try:
        a[a > -1 & a < 1]
    except Exception as exc:
        print("без скобок:", type(exc).__name__)


TASKS = [task1, task2, task3, task4, task5, task6, task7, task8, task9, task10]

if len(sys.argv) == 1:
    chosen = range(1, 11)
else:
    chosen = [int(arg) for arg in sys.argv[1:]]

for number in chosen:
    TASKS[number - 1]()
