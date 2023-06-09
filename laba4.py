"""
С клавиатуры вводится два числа K и N.Квадратная матрица А(N,N), состоящая из 4-х равных по размерам подматриц, B,C,D,E
заполняется случайным образом целыми числами в интервале [-10,10]. Для отладки использовать не случайное заполнение,
а целенаправленное. Вид матрицы А:

D E
C B

Вариант №16:
Формируется матрица F следующим образом: скопировать в нее А и  если в Е максимальный элемент в нечетных столбцах
больше, чем сумма чисел в нечетных строках, то поменять местами С и В симметрично, иначе В и Е поменять местами
несимметрично. При этом матрица А не меняется. После чего если определитель матрицы А больше суммы диагональных
элементов матрицы F, то вычисляется выражение: A-1*AT – K * F-1, иначе вычисляется выражение (AТ +G-FТ)*K, где G-нижняя
треугольная матрица, полученная из А. Выводятся по мере формирования А, F и все матричные операции последовательно.
"""

from math import ceil, floor
import random
import numpy as np
from matplotlib import pyplot as plt



def printMatrix(matrix):  # функция вывода матрицы
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print("{:5d}".format(matrix[i][j]), end="")
        print()


k = int(input("Введите число K: "))
n = int(input("Введите число число N>3: "))
while n <= 3:  # ошибка в случае введения слишком малого порядка матрицы
    n = int(input("Вы ввели число, неподходящее по условию, введите число N>=3:\n"))

A = np.random.randint(-10.0, 10.0, (n, n))  # создание матрицы А
print("\nМатрица A:\n")
printMatrix(A)

F = A.copy()  # Создание матрицы F
F_dump = F.copy()

submatrix_order = ceil(n / 2)  # определитель матрицы  для смены B на E
submatrix_length = n // 2  # # определитель матрицы для смены C на B
b = np.array(A[submatrix_length + n % 2:n, submatrix_length + n % 2:n])  # создание подматрицы B
c = np.array(A[submatrix_length + n % 2:n, :submatrix_length])  # создание подматрицы C

# вычленяем подматрицу Е через срезы
# проверка n на четность нужна для корректного среза(чтобы матрица А делилась на равные 4 подматрицы)
if n % 2 == 0:
    e = [F[i][submatrix_order:n] for i in range(0, submatrix_order)]
else:
    e = [F[i][submatrix_order - 1:n] for i in range(0, submatrix_order)]

# ниже ищем максимальный элемент в нечетных столбцах в Е
maxlist = []
for i in range(submatrix_order):
    for j in range(submatrix_order):
        if (j + 1) % 2 != 0:
            maxlist.append(e[i][j])
maxvalue = max(maxlist)

# ниже ищем сумму чисел в нечетных строках в E
sumvalue = 0
for i in range(submatrix_order):
    for j in range(submatrix_order):
        if (i + 1) % 2 != 0:
            sumvalue += e[i][j]

# создание матрицы F по условию
if maxvalue > sumvalue:
    # меняем C и B симметрично
    F[submatrix_length + n % 2:n, submatrix_length + n % 2:n] = c[::, ::-1]
    F[submatrix_length + n % 2:n, :submatrix_length] = b[::, ::-1]
    print("Матрица F:")
    printMatrix(F)
else:
    # меняем B и E несимметрично
    for i in range(ceil(n / 2)):
        for j in range(ceil(n / 2), n):
            F[i][j] = F_dump[floor(n / 2) + i][j]
            F[floor(n / 2) + i][j] = F_dump[i][j]
    print("Матрица F:")
    printMatrix(F)

# ниже вычисляем и выводим выражения по условию
np.set_printoptions(linewidth=1000)
try:
    if np.linalg.det(A) > sum(np.diagonal(F)):
        print("\nРезультат выражения A^(-1)*AT – K * F^(-1):\n",
              np.linalg.inv(A) * A.transpose() - k * np.linalg.inv(F))
    else:
        G = np.tri(n) * A
        print("\nРезультат выражения (AT + G - FT) * K:\n",
              (A.transpose() + G - F.transpose()) * k)
except np.linalg.LinAlgError:
    print("Одна из матриц является вырожденной, обратную матрицу найти невозможно.")




fig, axs = plt.subplots(2, 2, figsize=(11, 8)) #создаем окно и 4 графика на нем

# ниже первый график с фунцией plot
x = list(range(1, n + 1)) # получаем значения х
for j in range(n):
    y = list(F[j, ::]) #получаем значения у
    axs[0, 1].plot(x, y) # строим график справа вверху
    axs[0, 1].set(title="График с использованием функции plot:", #обозначения на графике
                  xlabel='Номер элемента в строке',
                  ylabel='Значение элемента')
    axs[0, 1].grid(True) # сетка на графике

    # ниже второй график с фунцией bar
    axs[1, 0].bar(x, y, 0.4, label=f"{j+1} строка.") # строим график слева снизу
    axs[1, 0].set(title="График с использованием функции bar:", #обозначения на графике
                  xlabel='Номер элемента в строке',
                  ylabel='Значение элемента')

# ниже блок для создания массива, чтобы потом скормить его функции pie
av = [np.mean(abs(F[i, ::])) for i in range(n)]
av = int(sum(av))
sizes = [round(np.mean(abs(F[i, ::])) * 100/av, 1) for i in range(n)]

axs[0, 0].set(title="График с использованием функции pie:",) #обозначения на графике
axs[0, 0].pie(sizes, labels=list(range(1, n+1)), autopct='%1.1f%%', shadow=True) # строим график слева вверху


z = np.random.randint(-10, 10, n)

fig = plt.figure()
axs[1,1] = fig.add_subplot(111, projection='3d')


x = list(range(1, n + 1)) # получаем значения х
for j in range(n):

    y = list(F[j, ::]) #получаем значения у

    axs[1,1].scatter(x, y, z)


plt.show()
