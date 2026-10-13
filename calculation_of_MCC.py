import math

def is_zero(x, tol = 1e-12):
    return abs(x) < tol

# 1. Ф-ции расчета собственных характеристик

def sphere(m, r, x0, y0, z0):
    """Сфера: центр в (x0, y0, z0), радиус r"""
    xc = x0
    yc = y0
    zc = z0
    I = (2 / 5) * m * r**2
    Ixx = Iyy = Izz = I
    Ixy = Ixz = Iyz = 0.0
    return xc, yc, zc, Ixx, Iyy, Izz, Ixy, Ixz, Iyz

def rect_prism(m, a, b, c, x0, y0, z0):
    """Прямоугольный параллелепипед.
    Размеры: a — по x, b — по y, c — по z.
    x0, y0, z0 — координаты УГЛА (0, 0, 0) локальной системы (угол куба)"""
    """xc = x0 + a / 2 # x0, y0, z0 — координаты УГЛА (0, 0, 0) локальной системы (угол куба)
    yc = y0 + b / 2
    zc = z0 + c / 2"""
    xc = x0 # x0, y0, z0 — координаты центра (0, 0, 0) локальной системы (центр куба)
    yc = y0
    zc = z0
    Ixx = (1 / 12) * m * (b**2 + c**2)
    Iyy = (1 / 12) * m * (a**2 + c**2)
    Izz = (1 / 12) * m * (a**2 + b**2)
    Ixy = Ixz = Iyz = 0.0
    return xc, yc, zc, Ixx, Iyy, Izz, Ixy, Ixz, Iyz

def cylinder(m, r, h, x0, y0, z0, axis = 'z'):
    """Цилиндр с осью симметрии вдоль axis ('x', 'y', 'z')
    x0, y0, z0 — координаты центра основания (нижнего)"""
    if axis == 'z':
        xc = x0
        yc = y0
        #zc = z0 + h / 2 # пересчет, если центр нижнего основания
        zc = z0
        I_axis = 0.5 * m * r**2
        I_perp = (1 / 12) * m * (3 * r**2 + h**2)
        Ixx = Iyy = I_perp
        Izz = I_axis
    elif axis == 'y':
        xc = x0
        #yc = y0 + h / 2 # пересчет, если центр нижнего основания
        yc = y0
        zc = z0
        Iyy = 0.5 * m * r**2
        I_perp = (1 / 12) * m * (3 * r**2 + h**2)
        Ixx = Izz = I_perp
    elif axis == 'x':
        #xc = x0 + h / 2 # пересчет, если центр нижнего основания
        xc = x0
        yc = y0
        zc = z0
        Ixx = 0.5 * m * r**2
        I_perp = (1 / 12) * m * (3 * r**2 + h**2)
        Iyy = Izz = I_perp
    else:
        raise ValueError("axis должен быть 'x', 'y' или 'z'")
    Ixy = Ixz = Iyz = 0.0
    return xc, yc, zc, Ixx, Iyy, Izz, Ixy, Ixz, Iyz

# 2. Ввод данных

print("=== Калькулятор массовых характеристик (МЦХ) ===\n")
n = int(input("Количество составных частей: "))

parts = []

for i in range(n):
    print(f"\n--- Часть {i+1} ---")
    m = float(input("  Масса (кг): "))
    shape = input("  Форма (sphere / rect / cylinder): ").strip().lower()

    if shape == "sphere":
        r = float(input("  Радиус r (м): "))
        x0 = float(input("  x0 (координата центра): "))
        y0 = float(input("  y0: "))
        z0 = float(input("  z0: "))
        xc, yc, zc, Ixx, Iyy, Izz, Ixy, Ixz, Iyz = sphere(m, r, x0, y0, z0)

    elif shape == "rect":
        a = float(input("  Размер по x (a): "))
        b = float(input("  Размер по y (b): "))
        c = float(input("  Размер по z (c): "))
        x0 = float(input("  x0 (координата центра): ")) # (коордната угла)
        y0 = float(input("  y0: "))
        z0 = float(input("  z0: "))
        xc, yc, zc, Ixx, Iyy, Izz, Ixy, Ixz, Iyz = rect_prism(m, a, b, c, x0, y0, z0)

    elif shape == "cylinder":
        r = float(input("  Радиус r: "))
        h = float(input("  Высота h: "))
        x0 = float(input("  x0 (центр нижнего основания): "))
        y0 = float(input("  y0: "))
        z0 = float(input("  z0: "))
        axis = input("  Ось симметрии (x/y/z, по умолчанию z): ").strip().lower() or 'z'
        xc, yc, zc, Ixx, Iyy, Izz, Ixy, Ixz, Iyz = cylinder(m, r, h, x0, y0, z0, axis)

    else:
        print("  Неизвестная форма → считаем точечной массой")
        xc = yc = zc = 0.0
        Ixx = Iyy = Izz = Ixy = Ixz = Iyz = 0.0

    print(f"  → Центр масс части: ({xc:.6f}, {yc:.6f}, {zc:.6f})")
    parts.append((m, xc, yc, zc, Ixx, Iyy, Izz, Ixy, Ixz, Iyz))

# 3. Общий центр масс

M = sum(m for m, _, _, _, _, _, _, _, _, _ in parts)
Xc = sum(m * xc for m, xc, _, _, _, _, _, _, _, _ in parts) / M
Yc = sum(m * yc for m, _, yc, _, _, _, _, _, _, _ in parts) / M
Zc = sum(m * zc for m, _, _, zc, _, _, _, _, _, _ in parts) / M

print("\n" + "=" * 60)
print("        РЕЗУЛЬТАТЫ РАСЧЁТА МЦХ")
print("=" * 60)
print(f"Суммарная масса:         M = {M:.6f} кг")
print(f"Центр масс системы:      Xc = {Xc:.6f}, Yc = {Yc:.6f}, Zc = {Zc:.6f}")

# 4. Тензор инерции относительно общего ц.м.

Ixx = Iyy = Izz = Ixy = Ixz = Iyz = 0.0

for m, xc, yc, zc, Ixx_i, Iyy_i, Izz_i, Ixy_i, Ixz_i, Iyz_i in parts:
    dx = xc - Xc
    dy = yc - Yc
    dz = zc - Zc

    Ixx += Ixx_i + m * (dy**2 + dz**2)
    Iyy += Iyy_i + m * (dx**2 + dz**2)
    Izz += Izz_i + m * (dx**2 + dy**2)
    Ixy += Ixy_i + m * dx * dy
    Ixz += Ixz_i + m * dx * dz
    Iyz += Iyz_i + m * dy * dz

print(f"\nТензор инерции относительно центра масс (кг·м²):")
print(f"  Ixx = {Ixx:12.6f}    Ixy = {Ixy:12.6f}    Ixz = {Ixz:12.6f}")
print(f"  Iyx = {Ixy:12.6f}    Iyy = {Iyy:12.6f}    Iyz = {Iyz:12.6f}")
print(f"  Izx = {Ixz:12.6f}    Izy = {Iyz:12.6f}    Izz = {Izz:12.6f}")

# 5. Главные оси инерции

print("\n" + "-" * 60)
print("ГЛАВНЫЕ МОМЕНТЫ И ОСИ ИНЕРЦИИ")

# 7.1 — все произведения нулевые
if is_zero(Ixy) and is_zero(Ixz) and is_zero(Iyz):
    print("→ Все центробежные моменты ≈ 0 → текущие оси — главные")
    J1, J2, J3 = sorted([Ixx, Iyy, Izz])
    print(f"Главные моменты: {J1:.6f}, {J2:.6f}, {J3:.6f}")

# 7.2 — случай с плоскостью симметрии
elif is_zero(Ixy) and is_zero(Ixz):
    print("→ Ixy = Ixz ≈ 0, Iyz ≠ 0 → плоскость симметрии XY, главная ось Z")
    tan2a = 2 * Iyz / (Ixx - Iyy)
    alpha = 0.5 * math.atan(tan2a)
    R = math.sqrt(((Ixx - Iyy) / 2)**2 + Iyz**2)
    J1 = (Ixx + Iyy) / 2 + R
    J2 = (Ixx + Iyy) / 2 - R
    J3 = Izz
    print(f"Угол поворота вокруг Z: α = {math.degrees(alpha):.3f}°")
    print(f"Главные моменты: {J1:.6f}, {J2:.6f}, {J3:.6f}")

elif is_zero(Ixy) and is_zero(Iyz):
    print("→ Ixy = Iyz ≈ 0, Ixz ≠ 0 → плоскость симметрии XZ, главная ось Y")
    tan2a = 2 * Ixz / (Ixx - Izz)
    alpha = 0.5 * math.atan(tan2a)
    R = math.sqrt(((Ixx - Izz) / 2)**2 + Ixz**2)
    J1 = (Ixx + Izz) / 2 + R
    J3 = (Ixx + Izz) / 2 - R
    J2 = Iyy
    print(f"Угол поворота вокруг Y: α = {math.degrees(alpha):.3f}°")
    print(f"Главные моменты: {J1:.6f}, {J2:.6f}, {J3:.6f}")

elif is_zero(Ixz) and is_zero(Iyz):
    print("→ Ixz = Iyz ≈ 0, Ixy ≠ 0 → плоскость симметрии YZ, главная ось X")
    tan2a = 2 * Ixy / (Iyy - Izz)
    alpha = 0.5 * math.atan(tan2a)
    R = math.sqrt(((Iyy - Izz) / 2)**2 + Ixy**2)
    J2 = (Iyy + Izz) / 2 + R
    J3 = (Iyy + Izz) / 2 - R
    J1 = Ixx
    print(f"Угол поворота вокруг X: α = {math.degrees(alpha):.3f}°")
    print(f"Главные моменты: {J1:.6f}, {J2:.6f}, {J3:.6f}")

else:
    print("→ Общий случай (все три центробежных момента ≠ 0)")
    # Решение кубического уравнения (тригонометрический метод)
    a = -(Ixx + Iyy + Izz)
    b = Ixx * Iyy + Ixx * Izz + Iyy * Izz - Ixy**2 - Ixz**2 - Iyz**2
    c = -(Ixx * Iyy * Izz + 2 * Ixy * Ixz * Iyz - Ixx * Iyz**2 - Iyy * Ixz**2 - Izz * Ixy**2)

    p = (3 * b - a**2) / 3
    q = (2 * a**3 - 9 * a * b + 27 * c) / 27
    disc = (q / 2)**2 + (p / 3)**3

    if disc > 1e-8:
        print("Ошибка: дискриминант положительный → проверьте данные!")
    else:
        r = math.sqrt(max(-p / 3, 0))
        if r < 1e-12:
            phi = 0
        else:
            cos_phi = max(min(-q / (2 * r**3), 1), -1)
            phi = math.acos(cos_phi)
        J1 = 2 * r * math.cos(phi / 3) - a / 3
        J2 = 2 * r * math.cos((phi + 2 * math.pi) / 3) - a / 3
        J3 = 2 * r * math.cos((phi + 4 * math.pi) / 3) - a / 3

        J1, J2, J3 = sorted([J1, J2, J3])
        print(f"Главные моменты инерции: {J1:.6f}, {J2:.6f}, {J3:.6f}")

print("\nРасчёт завершён!")
