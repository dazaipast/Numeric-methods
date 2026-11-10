import math
import random
from decimal import Decimal, getcontext

getcontext().prec = 28


def relative_error(approx, exact):
    if exact == 0:
        return float("inf")
    return abs(approx - exact) / abs(exact)


def show_pair(name, approx, exact):
    delta = abs(approx - exact)
    rel = relative_error(approx, exact)
    print(f"{name}: x={approx}, x*={exact}")
    print(f"  Δ = {delta:.6e},  δ = {rel * 100:.6f}%")
    return delta, rel


def task1():
    print("\n=== Задача 1 ===")
    pairs = [
        ("π", 3.14, math.pi),
        ("e", 2.718, math.e),
        ("g", 9.8, 9.81),
        ("1/3", 0.333, 1 / 3),
    ]
    rows = []
    for name, approx, exact in pairs:
        rows.append((name, *show_pair(name, approx, exact)))
    by_abs = sorted(rows, key=lambda row: row[1])
    by_rel = sorted(rows, key=lambda row: row[2])
    print("лучше по Δ:", " < ".join(row[0] for row in by_abs))
    print("лучше по δ:", " < ".join(row[0] for row in by_rel))


def task2():
    print("\n=== Задача 2 ===")
    show_pair("мост, м", 1247, 1250)
    show_pair("болт, мм", 9.7, 10.0)


def task3():
    print("\n=== Задача 3 ===")
    print("exact=0 ->", relative_error(1.0, 0))
    for name, approx, exact in (
        ("π", 3.14, math.pi),
        ("e", 2.718, math.e),
        ("g", 9.8, 9.81),
        ("1/3", 0.333, 1 / 3),
    ):
        print(name, relative_error(approx, exact))


def task4():
    print("\n=== Задача 4 ===")
    x = 47.3
    delta = 0.001
    left = x / (1 + delta)
    right = x / (1 - delta)
    print(f"x* в [{left:.4f}, {right:.4f}]")


def task5():
    print("\n=== Задача 5 ===")
    limit = 0.3 / 0.005
    print(f"B точнее по Δ, пока |T| <= {limit:.0f} °C")


def task6():
    print("\n=== Задача 6 ===")
    print("0.004520 -> 4 значащих, 4.520e-3")
    print("1200 -> хвост нулей неясен (2, 3 или 4), лучше 1.200e3 если их 4")
    print("1.200 -> 4 значащих, 1.200e0")
    print("10.03 -> 4 значащих, 1.003e1")
    print("0.03050 -> 4 значащих, 3.050e-2")
    print("250000 -> хвост нулей неясен, лучше 2.50000e5 если их 6")


def task7():
    print("\n=== Задача 7 ===")
    print("4.74 ± 0.02")
    print("значащих цифр осталось: 3")


def task8():
    print("\n=== Задача 8 ===")
    print(round(0.5), round(1.5), round(2.5), round(3.5), round(-0.5), round(-1.5), round(-2.5))
    rng = random.Random(42)
    values = [rng.randrange(10) + 0.5 for _ in range(10**6)]
    banker = sum(round(value) for value in values)
    up = sum(math.floor(value + 0.5) for value in values)
    print(f"сумма banker's = {banker}")
    print(f"сумма всегда вверх = {up}")
    print(f"сдвиг = {up - banker}")


def task9():
    print("\n=== Задача 9 ===")
    import mpmath as mp

    mp.mp.dps = 50
    plain = 0.0
    rounded = 0.0
    terms = []
    for k in range(1, 101):
        term = 1 / k
        plain += term
        rounded += round(term, 3)
        terms.append(term)
    fsum_ref = math.fsum(terms)
    exact = mp.harmonic(100)
    for name, value in (("без округления", plain), ("до 3 знаков", rounded)):
        delta_f = abs(value - fsum_ref)
        delta = abs(mp.mpf(value) - exact)
        print(f"{name}: S={value:.10f}")
        print(f"  к fsum: Δ={delta_f:.6e}")
        print(f"  к mpmath: Δ={float(delta):.6e}, δ={float(delta / abs(exact)):.6e}")
    err_plain = abs(mp.mpf(plain) - exact)
    err_round = abs(mp.mpf(rounded) - exact)
    print(f"ошибка округления больше в {float(err_round / err_plain):.1f} раз")


def task10():
    print("\n=== Задача 10 ===")
    total = 0.1 + 0.2
    print("0.1 + 0.2 =", total)
    print("== 0.3:", total == 0.3)
    print("isclose:", math.isclose(total, 0.3))
    delta = abs(total - 0.3)
    print(f"Δ = {delta:.6e}, δ = {relative_error(total, 0.3):.6e}")


def task11():
    print("\n=== Задача 11 ===")
    a = 1 + 1e-15
    got = a - 1
    print(f"1 + 1e-15 - 1 = {got:.6e}, ждали 1e-15")
    print(f"δ = {relative_error(got, 1e-15):.6e}")

    def roots(b):
        disc = math.sqrt(b * b - 4)
        bad = (-b + disc) / 2
        good = 2 / (-b - disc)
        return bad, good

    getcontext().prec = 50
    b = Decimal(10**8)
    disc = (b * b - 4).sqrt()
    exact = (-b + disc) / 2
    bad, good = roots(1e8)
    print("меньший корень, b=1e8")
    print(f"  плохо  {bad:.6e}  δ={relative_error(bad, float(exact)):.6e}")
    print(f"  хорошо {good:.6e}  δ={relative_error(good, float(exact)):.6e}")
    print(f"  эталон {exact}")


def task12():
    print("\n=== Задача 12 ===")
    arr = [0.1] * 10**6
    exact = 1e5
    naive = 0.0
    for value in arr:
        naive += value
    ways = (("цикл", naive), ("sum", sum(arr)), ("fsum", math.fsum(arr)))
    print(f"{'способ':<8} {'результат':>20} {'Δ':>12} {'δ':>12}")
    for name, value in ways:
        delta = abs(value - exact)
        print(f"{name:<8} {value:20.10f} {delta:12.3e} {delta / exact:12.3e}")


def task13():
    print("\n=== Задача 13 ===")
    half = 10**6 // 2
    small = [1e-10] * half
    large = [1e6] * half
    small_first = small + large
    large_first = large + small
    ref = math.fsum(small_first)
    for name, data in (("сначала маленькие", small_first), ("сначала большие", large_first)):
        total = 0.0
        for value in data:
            total += value
        print(f"{name}: {total:.10f}, Δ={abs(total - ref):.6e}")
    print(f"fsum: {ref:.10f}")


def task14():
    print("\n=== Задача 14 ===")
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = 1.0
    exact = Decimal(1)
    factor = Decimal("1.0001")
    steps = []
    errors = []
    limits = (1e-9, 1e-6, 1e-3)
    hit = {limit: None for limit in limits}
    for step in range(1, 10_001):
        x *= 1.0001
        exact *= factor
        rel = float(abs(Decimal(x) - exact) / abs(exact))
        steps.append(step)
        errors.append(rel)
        for limit in limits:
            if hit[limit] is None and rel > limit:
                hit[limit] = step
    final = math.exp(10_000 * math.log(1.0001))
    print(f"после 10000 шагов x={x:.10f}")
    print(f"math.exp = {final:.10f}, Decimal = {exact}")
    print(f"δ к Decimal = {errors[-1]:.6e}")
    for limit, step in hit.items():
        print(f"δ > {limit:.0e} на шаге {step}")

    plt.figure(figsize=(7, 4))
    plt.plot(steps, errors)
    plt.yscale("log")
    plt.xlabel("шаг")
    plt.ylabel("относительная погрешность")
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    path = "рост_ошибки.png"
    plt.savefig(path, dpi=120)
    plt.close()
    print("график:", path)


def task15():
    print("\n=== Задача 15 ===")
    total = 0.0
    for _ in range(10**6):
        total += 0.01
    dec = Decimal("0")
    step = Decimal("0.01")
    for _ in range(10**6):
        dec += step
    kopecks = 10**6
    rub_from_kop = kopecks / 100
    exact = Decimal("10000")
    print(f"float   = {total:.10f}")
    print(f"Decimal = {dec}")
    print(f"копейки = {rub_from_kop:.2f}")
    gap = abs(Decimal(str(total)) - exact)
    print(f"расхождение float и 10000 руб: {gap} руб, {float(gap / exact) * 100:.6e}%")


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
