import math
import platform
import random
import sys
from decimal import Decimal, getcontext

import numpy as np

getcontext().prec = 50


def rel_err(approx, exact):
    exact = float(exact)
    if exact == 0:
        return float("inf")
    return abs(approx - exact) / abs(exact)


def task1():
    print("\n=== Задача 1 ===")
    items = []

    x = 1e-8
    cond = abs(x * (1 / (2 * math.sqrt(x))) / math.sqrt(x))
    items.append(("sqrt(x), x=1e-8", cond))

    x = 1.001
    cond = abs(1 / math.log(x))
    items.append(("ln(x), x=1.001", cond))

    x = 1.000001
    cond = abs(x / (x - 1))
    items.append(("x-1, x=1.000001", cond))

    x = math.pi / 2
    cond = abs(x * math.cos(x) / math.sin(x))
    items.append(("sin(x), x=pi/2", cond))

    for name, value in items:
        print(f"{name}: cond = {value:.6e}")
    items.sort(key=lambda row: row[1])
    print("по возрастанию:", " < ".join(row[0] for row in items))


def task2():
    print("\n=== Задача 2 ===")
    a = 1 + 1e-8
    b = 1.0
    delta_a = 1e-9
    f = a - b
    f2 = (a + delta_a) - b
    cond_a = abs(a / (a - b))
    measured = abs((f2 - f) / f) / abs(delta_a / a)
    print(f"cond по a = {cond_a:.6e}")
    print(f"фактическое |Δf/f| / |δa/a| = {measured:.6e}")
    print(f"Δf / δa = {(f2 - f) / delta_a:.6f}")


def task3():
    print("\n=== Задача 3 ===")
    print(f"{'eps':>10} {'сдвиг':>12} {'отношение сдвигов':>20}")
    prev = None
    for eps in (1e-2, 1e-4, 1e-6):
        shift = math.sqrt(eps)
        ratio = "" if prev is None else f"{prev / shift:.1f}"
        print(f"{eps:10.0e} {shift:12.6f} {ratio:>20}")
        prev = shift


def task4():
    print("\n=== Задача 4 ===")
    x = 20.0
    term = 1.0
    total = 1.0
    for k in range(1, 80):
        term *= -x / k
        total += term
    stable = math.exp(-x)
    print(f"ряд Тейлора e^(-20) = {total:.6e}")
    print(f"math.exp(-20)     = {stable:.6e}")
    print(f"δ ряда = {rel_err(total, stable):.6e}")
    print(f"cond задачи = |x| = {x:.0f}")


def small_root(b):
    disc = math.sqrt(b * b - 4.0)
    bad = (-b + disc) / 2.0
    good = 2.0 / (-b - disc)
    bb = Decimal(str(b))
    exact_disc = (bb * bb - 4).sqrt()
    exact = (-bb + exact_disc) / 2
    return bad, good, exact


def task5():
    print("\n=== Задача 5 ===")
    print(f"{'b':>8} {'δ плохого':>14} {'δ хорошего':>14}")
    for b in (1e4, 1e8, 1e12):
        bad, good, exact = small_root(b)
        print(f"{b:8.0e} {rel_err(bad, exact):14.3e} {rel_err(good, exact):14.3e}")


def f_bad(x):
    return (1 - math.cos(x)) / (x * x)


def f_good(x):
    half = x / 2
    return 2 * math.sin(half) ** 2 / (x * x)


def f_exact(x):
    import mpmath as mp

    mp.mp.dps = 50
    xx = mp.mpf(str(x))
    return (1 - mp.cos(xx)) / (xx * xx)


def task6():
    print("\n=== Задача 6 ===")
    print(f"{'x':>8} {'δ плохого':>14} {'δ хорошего':>14}")
    crossed = None
    for x in (1e-2, 1e-4, 1e-6, 1e-8, 1e-10):
        exact = f_exact(x)
        bad = rel_err(f_bad(x), exact)
        good = rel_err(f_good(x), exact)
        print(f"{x:8.0e} {bad:14.3e} {good:14.3e}")
        if crossed is None and bad > 0.01:
            crossed = x
    print("плохой способ хуже 1% начиная с x =", crossed)


def task7():
    print("\n=== Задача 7 ===")

    def exact(x):
        xx = Decimal(str(x))
        return (xx + 1).sqrt() - xx.sqrt()

    print(f"{'x':>8} {'δ плохого':>14} {'δ хорошего':>14}")
    xs = []
    errs = []
    for x in (1e4, 1e8, 1e12, 1e14, 1e16):
        ref = exact(x)
        bad = math.sqrt(x + 1) - math.sqrt(x)
        good = 1 / (math.sqrt(x + 1) + math.sqrt(x))
        bad_err = rel_err(bad, ref)
        xs.append(x)
        errs.append(bad_err)
        print(f"{x:8.0e} {bad_err:14.3e} {rel_err(good, ref):14.3e}")
    slope = math.log(errs[-1] / errs[0]) / math.log(xs[-1] / xs[0])
    print(f"показатель роста ошибки плохого способа ≈ {slope:.2f}")


def task8():
    print("\n=== Задача 8 ===")
    import mpmath as mp

    mp.mp.dps = 50
    print(f"{'x':>8} {'δ log':>14} {'δ log1p':>14}")
    for x in (1e-2, 1e-8, 1e-12, 1e-16):
        ref = mp.log(1 + mp.mpf(str(x)))
        bad = math.log(1 + x) if 1 + x != 1 else 0.0
        good = math.log1p(x)
        print(f"{x:8.0e} {rel_err(bad, ref):14.3e} {rel_err(good, ref):14.3e}")


def task9():
    print("\n=== Задача 9 ===")
    import mpmath as mp

    mp.mp.dps = 50
    print(f"{'n':>8} {'δ цикла':>12} {'δ sum':>12} {'δ fsum':>12}")
    for n in (10**5, 10**6, 10**7):
        ref = mp.harmonic(n)
        naive = 0.0
        for k in range(1, n + 1):
            naive += 1.0 / k
        builtin = sum(1.0 / k for k in range(1, n + 1))
        accurate = math.fsum(1.0 / k for k in range(1, n + 1))
        print(
            f"{n:8d} {rel_err(naive, ref):12.3e} {rel_err(builtin, ref):12.3e} {rel_err(accurate, ref):12.3e}"
        )


def task10():
    print("\n=== Задача 10 ===")
    bad_small = rel_err(f_bad(1e-8), f_exact(1e-8))
    bad_big = rel_err(f_bad(1e-2), f_exact(1e-2))
    print(f"(а) плохой алгоритм, x=1e-2 -> δ={bad_big:.3e}, x=1e-8 -> δ={bad_small:.3e}")

    x = np.float32(1e-3)
    bad32 = (np.float32(1) - np.cos(x)) / (x * x)
    bad64 = f_bad(1e-3)
    ref = f_exact(1e-3)
    print(f"(б) x=1e-3, δ float32={rel_err(float(bad32), ref):.3e}, δ float64={rel_err(bad64, ref):.3e}")

    good = rel_err(f_good(1e-8), f_exact(1e-8))
    print(f"(в) x=1e-8, δ плохого={bad_small:.3e}, δ хорошего={good:.3e}")


def task11():
    print("\n=== Задача 11 ===")
    b = 1e16
    one = (-b + math.sqrt(b * b - 4)) / 2
    two = (-b + (b**2 - 4) ** 0.5) / 2
    bb = Decimal(b)
    exact = (-bb + (bb * bb - 4).sqrt()) / 2
    print(f"способ 1 = {one}, способ 2 = {two}, равны: {one == two}")
    print(f"эталон = {exact}")
    print(f"δ обоих = {rel_err(one, exact):.3e}")


def task12():
    print("\n=== Задача 12 ===")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xs = np.logspace(2, 16, 8)
    errs = []
    print(f"{'x':>10} {'δ плохого':>14}")
    for x in xs:
        xx = Decimal(str(x))
        ref = (xx + 1).sqrt() - xx.sqrt()
        bad = math.sqrt(x + 1) - math.sqrt(x)
        err = rel_err(bad, ref)
        errs.append(err)
        print(f"{x:10.3e} {err:14.3e}")
    slope = math.log(errs[-1] / errs[0]) / math.log(xs[-1] / xs[0])
    print(f"наклон log-log ≈ {slope:.2f}, теория для ε·x даёт 1")

    plt.figure(figsize=(7, 4))
    plt.loglog(xs, errs, marker="o", label="плохой способ")
    eps = sys.float_info.epsilon
    plt.loglog(xs, eps * xs, linestyle="--", label="ε·x")
    plt.xlabel("x")
    plt.ylabel("относительная ошибка")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig("ошибка_sqrt.png", dpi=120)
    plt.close()
    print("график: ошибка_sqrt.png")


def task13():
    print("\n=== Задача 13 ===")
    print("Python", platform.python_version())
    print("numpy", np.__version__)

    def methods(values):
        values = [float(value) for value in values]
        return sum(values), math.fsum(values), float(np.sum(np.asarray(values)))

    def run(seed):
        random.seed(seed)
        rng = np.random.default_rng(seed)
        plain = [random.random() for _ in range(10**5)]
        noise = rng.random(10**5)
        sign = np.where(np.arange(10**5) % 2 == 0, 1.0, -1.0)
        hard = sign * (2.0**53) + (noise - 0.5) * 8
        return methods(plain), methods(hard)

    first = run(42)
    second = run(42)
    other = run(43)
    print("seed 42, повтор совпал:", first == second)
    print("обычные числа, seed 42:", first[0])
    print("обычные числа, seed 43:", other[0])
    print("с сокращением, seed 42: sum, fsum, np.sum =", first[1])
    print("с сокращением, seed 43: sum, fsum, np.sum =", other[1])
    print("на обычных числах три способа совпали:", len(set(first[0])) == 1)


def describe(name, values):
    try:
        naive = sum(values)
    except Exception as exc:
        naive = type(exc).__name__
    try:
        accurate = math.fsum(values)
    except Exception as exc:
        accurate = type(exc).__name__ + ": " + str(exc).split("\n")[0]
    print(f"{name}: sum={naive}, fsum={accurate}")


def task14():
    print("\n=== Задача 14 ===")
    describe("большое 1e300", [1e300, 1e300])
    describe("маленькое 1e-300", [1e-300, 1e-300])
    describe("ноль", [0.0, 1.0])
    describe("денормал отдельно", [1e-320, 1e-320])
    describe("денормал плюс 1", [1e-320, 1.0])
    describe("inf", [float("inf"), 1.0])
    describe("inf и -inf", [float("inf"), float("-inf")])
    describe("nan", [float("nan"), 1.0])
    describe("всё вместе", [1e300, 1e-300, 0.0, 1e-320, float("inf"), float("nan")])


def task15():
    print("\n=== Задача 15 ===")
    print(f"{'x':>10} {'плохой':>14} {'хороший':>14} {'эталон':>14} {'δ плохого':>12} {'δ хорошего':>12}")
    for x in np.logspace(2, 16, 8):
        xx = Decimal(str(float(x)))
        ref = (xx + 1).sqrt() - xx.sqrt()
        bad = math.sqrt(x + 1) - math.sqrt(x)
        good = 1 / (math.sqrt(x + 1) + math.sqrt(x))
        print(
            f"{float(x):10.3e} {bad:14.6e} {good:14.6e} {float(ref):14.6e} "
            f"{rel_err(bad, ref):12.3e} {rel_err(good, ref):12.3e}"
        )


def main():
    task1()
    task2()
    task3()
    task4()
    task5()
    task6()
    task7()
    task8()
    task9()
    task10()
    task11()
    task12()
    task13()
    task14()
    task15()


if __name__ == "__main__":
    main()
