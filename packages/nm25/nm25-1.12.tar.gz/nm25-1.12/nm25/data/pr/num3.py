# # Алгоритм Штрассена


import time

import matplotlib.pyplot as plt
import numpy as np


def strassen(A, B):
    n = len(A[0])

    if n == 1:
        return A * B

    #разбиваем матрицу на подматрицы
    mid = n//2
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]
    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]

    #Рекурсивное умножение
    F1 = strassen(A11 + A22, B11 + B22)
    F2 = strassen(A21 + A22, B11)
    F3 = strassen(A11, B12 - B22)
    F4 = strassen(A22, B21 - B11)
    F5 = strassen(A11 + A12, B22)
    F6 = strassen(A21 - A11, B11 + B12)
    F7 = strassen(A12 - A22, B21 + B22)

    #Обьединим результаты в матрицу С
    C11 = F1 + F4 - F5 + F7
    C12 = F5 + F3
    C21 = F2 + F4
    C22 = F1 - F2 + F3 + F6

    C = np.zeros((n, n))
    C[:mid, :mid] = C11
    C[:mid, mid:] = C12
    C[mid:, :mid] = C21
    C[mid:, mid:] = C22

    return C




A = np.random.uniform(0, 10, (8, 8))
B = np.random.uniform(0, 10, (8, 8))
result = strassen(A, B)
print(result)

# График сходимости:

# Обычное умножение для сравнения
def standard_matrix_multiplication(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return np.array(C)


# Замер скорости выполнения
sizes = [2**i for i in range(1, 9)]  # Размеры матриц: 2, 4, 8, 16, ..., 128
times_strassen = []
times_standard = []

for size in sizes:
    A = np.random.uniform(0, 10, (size, size))
    B = np.random.uniform(0, 10, (size, size))

    # Время для алгоритма Штрассена
    start_time = time.time()
    result_strassen = strassen(A, B)
    end_time = time.time()
    times_strassen.append(end_time - start_time)

    # Время для стандартного умножения
    start_time = time.time()
    result_standard = standard_matrix_multiplication(A.tolist(), B.tolist())
    end_time = time.time()
    times_standard.append(end_time - start_time)

# Построение графика
plt.figure(figsize=(10, 6))
plt.plot(sizes, times_strassen, marker="o", label="Алгоритм Штрассена")
plt.plot(sizes, times_standard, marker="o", label="Стандартное умножение")
plt.xlabel("Размер матрицы (NxN)")
plt.ylabel("Время выполнения (секунды)")
plt.grid()
plt.legend()
plt.show()