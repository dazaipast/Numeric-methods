import timeit
import tracemalloc

import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# Задача 1: x in list  против  x in set
# ============================================================

sizes = [100, 1000, 10000]
time_list = []
time_set = []

print("Задача 1. Проверка вхождения, ищем -1")
for n in sizes:
    data_list = list(range(n))
    data_set = set(range(n))
    target = -1

    times_list = timeit.repeat(
        "target in data_list",
        globals={"target": target, "data_list": data_list},
        number=1000,
        repeat=5,
    )
    times_set = timeit.repeat(
        "target in data_set",
        globals={"target": target, "data_set": data_set},
        number=1000,
        repeat=5,
    )

    # timeit даёт сумму за number запусков, берём лучшую серию
    best_list = min(times_list) / 1000 * 1_000_000
    best_set = min(times_set) / 1000 * 1_000_000
    time_list.append(best_list)
    time_set.append(best_set)
    print(f"n={n}: list={best_list:.2f} мкс, set={best_set:.2f} мкс, set быстрее в {best_list / best_set:.1f} раз")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(sizes, time_list, "o-", label="list")
ax.plot(sizes, time_set, "s-", label="set")
ax.set_xlabel("Размер коллекции (n)")
ax.set_ylabel("Время одной проверки (мкс)")
ax.set_title("Вхождение: list и set")
ax.set_yscale("log")
ax.legend()
ax.grid(True, which="both", alpha=0.2)
plt.tight_layout()
fig.savefig("задача1_list_set.png", dpi=150, bbox_inches="tight")
plt.close()
print("График: задача1_list_set.png")

# ============================================================
# Задача 2: три способа собрать список квадратов
# ============================================================

stmts = {
    "append": "out = []\nfor i in range(N):\n    out.append(i * i)",
    "comprehension": "out = [i * i for i in range(N)]",
    "map": "out = list(map(lambda i: i * i, range(N)))",
}

N_values = [100_000, 1_000_000]
names = list(stmts)
res_time = {name: [] for name in names}
res_mem = {name: [] for name in names}

print("\nЗадача 2. Список квадратов")
for N in N_values:
    print(f"N={N}:")
    for name, stmt in stmts.items():
        times = timeit.repeat(stmt, globals={"N": N}, number=1, repeat=5)
        best_ms = min(times) * 1000

        tracemalloc.start()
        exec(stmt, {"N": N})
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_mb = peak / 1024 / 1024

        res_time[name].append(best_ms)
        res_mem[name].append(peak_mb)
        print(f"  {name:14s}  время={best_ms:8.2f} мс  память={peak_mb:6.2f} МБ")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

for name in names:
    ax1.plot(N_values, res_time[name], "o-", label=name, linewidth=2)
ax1.set_xlabel("N")
ax1.set_ylabel("Время (мс)")
ax1.set_title("Время создания списка квадратов")
ax1.legend()
ax1.grid(True, alpha=0.3)

x = np.arange(len(N_values))
width = 0.25
for i, name in enumerate(names):
    ax2.bar(x + (i - 1) * width, res_mem[name], width, label=name, alpha=0.85)
ax2.set_xticks(list(x))
ax2.set_xticklabels([f"N={N}" for N in N_values])
ax2.set_ylabel("Пиковая память (МБ)")
ax2.set_title("Память")
ax2.legend()
ax2.grid(True, axis="y", alpha=0.3)

plt.tight_layout()
fig.savefig("задача2_квадраты.png", dpi=150, bbox_inches="tight")
plt.close()
print("График: задача2_квадраты.png")

print("""
Вывод:
1. По памяти все три способа почти одинаковы: результат один и тот же список.
2. List comprehension быстрее: цикл идёт в C, без вызова append на каждый элемент.
3. map + lambda медленнее из-за вызова lambda на каждое число.
""")
