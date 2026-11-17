import numpy as np
import matplotlib.pyplot as plt

# Задача 1. Шестиугольник: поворот на 45° и отражение относительно y = x
k = np.arange(6)
hexagon = np.column_stack([
    np.cos(2 * np.pi * k / 6),
    np.sin(2 * np.pi * k / 6),
])
hexagon = np.vstack([hexagon, hexagon[0]])

theta = np.deg2rad(45)
rotate45 = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)],
])
reflect_yx = np.array([
    [0.0, 1.0],
    [1.0, 0.0],
])

rotated = hexagon @ rotate45.T
reflected = hexagon @ reflect_yx.T

fig, ax = plt.subplots(figsize=(7, 7))
ax.plot(hexagon[:, 0], hexagon[:, 1], "o-", color="gray", label="исходный", lw=2)
ax.plot(rotated[:, 0], rotated[:, 1], "o-", color="steelblue", label="поворот 45°", lw=2)
ax.plot(reflected[:, 0], reflected[:, 1], "s--", color="crimson", label="отражение y = x", lw=2)
ax.axhline(0, color="black", lw=0.5)
ax.axvline(0, color="black", lw=0.5)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title("Шестиугольник: исходный, поворот, отражение")
plt.tight_layout()
fig.savefig("задача1_шестиугольник.png", dpi=150, bbox_inches="tight")
plt.close()

rot90 = np.array([
    [0.0, -1.0],
    [1.0,  0.0],
])
print("Задача 1")
print("отражение y=x:\n", reflect_yx)
print("поворот на 90°:\n", rot90)
print("График: задача1_шестиугольник.png")

# Задача 2. Масштаб, поворот, перенос и обратный ход
rng = np.random.default_rng(42)
points = rng.uniform(-2, 2, size=(200, 2))

sx, sy = 1.5, 0.5
scale = np.array([
    [sx, 0.0],
    [0.0, sy],
])
theta = np.deg2rad(60)
rotate = np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta),  np.cos(theta)],
])

scaled = points @ scale.T
rotated_pts = scaled @ rotate.T

ones = np.ones((len(rotated_pts), 1))
points_h = np.hstack([rotated_pts, ones])
translate = np.array([
    [1.0, 0.0,  1.0],
    [0.0, 1.0, -1.0],
    [0.0, 0.0,  1.0],
])
transformed = (translate @ points_h.T).T[:, :2]

# обратные преобразования в обратном порядке: перенос, поворот, масштаб
translate_inv = np.array([
    [1.0, 0.0, -1.0],
    [0.0, 1.0,  1.0],
    [0.0, 0.0,  1.0],
])
back_h = np.hstack([transformed, np.ones((len(transformed), 1))])
after_shift = (translate_inv @ back_h.T).T[:, :2]

theta_inv = np.deg2rad(-60)
rotate_inv = np.array([
    [np.cos(theta_inv), -np.sin(theta_inv)],
    [np.sin(theta_inv),  np.cos(theta_inv)],
])
after_rot = after_shift @ rotate_inv.T

scale_inv = np.array([
    [1 / sx, 0.0],
    [0.0, 1 / sy],
])
restored = after_rot @ scale_inv.T

# те же обратные матрицы, но в прямом порядке
fwd = transformed @ scale_inv.T
fwd = fwd @ rotate_inv.T
fwd_h = np.hstack([fwd, np.ones((len(fwd), 1))])
fwd = (translate_inv @ fwd_h.T).T[:, :2]

print("\nЗадача 2")
print("совпали с исходными:", np.allclose(restored, points, atol=1e-12))
print("макс. расхождение:", np.max(np.abs(restored - points)))
print("если обратные в прямом порядке, совпали:", np.allclose(fwd, points, atol=1e-12))
print("макс. расхождение в прямом порядке:", np.max(np.abs(fwd - points)))

fig, ax = plt.subplots(figsize=(7, 7))
ax.scatter(points[:, 0], points[:, 1], s=18, color="gray", label="исходные", alpha=0.8)
ax.scatter(transformed[:, 0], transformed[:, 1], s=18, color="crimson", label="преобразованные", alpha=0.8)
ax.scatter(restored[:, 0], restored[:, 1], s=12, facecolors="none", edgecolors="steelblue",
           label="восстановленные", linewidths=1)
ax.axhline(0, color="black", lw=0.5)
ax.axvline(0, color="black", lw=0.5)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.legend()
ax.set_title("Облако: исходные, преобразованные, восстановленные")
plt.tight_layout()
fig.savefig("задача2_облако.png", dpi=150, bbox_inches="tight")
plt.close()
print("График: задача2_облако.png")
