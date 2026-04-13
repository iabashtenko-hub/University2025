class MatrixHandler:
    def __init__(self, data):
        self.grid = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def show(self):
        for row in self.grid:
            # Используем форматирование :g для компактного вывода чисел
            print(' '.join(f"{round(elem, 2):g}" for elem in row))

    def add_matrix(self, second_mtx):
        if self.rows != second_mtx.rows or self.cols != second_mtx.cols:
            print("Ошибка: несовпадение размерностей.")
            return None

        summed = [[self.grid[i][j] + second_mtx.grid[i][j] for j in range(self.cols)]
                  for i in range(self.rows)]
        return MatrixHandler(summed)

    def multiply_by_val(self, n):
        multiplied = [[item * n for item in row] for row in self.grid]
        return MatrixHandler(multiplied)

    def multiply_matrices(self, other):
        if self.cols != other.rows:
            print("Ошибка: такие матрицы нельзя перемножить.")
            return None

        # Классическое перемножение через вложенные циклы
        out = [[sum(self.grid[i][k] * other.grid[k][j] for k in range(self.cols))
                for j in range(other.cols)] for i in range(self.rows)]
        return MatrixHandler(out)

    def rotate(self, mode=1):
        if mode == 1:  # Главная диагональ
            res = [[self.grid[j][i] for j in range(self.rows)] for i in range(self.cols)]
        elif mode == 2:  # Побочная
            res = [[self.grid[self.rows - 1 - j][self.cols - 1 - i] for j in range(self.rows)]
                   for i in range(self.cols)]
        elif mode == 3:  # По вертикали
            res = [r[::-1] for r in self.grid]
        elif mode == 4:  # По горизонтали
            res = self.grid[::-1]
        else:
            return None
        return MatrixHandler(res)

    def calculate_det(self):
        if self.rows != self.cols:
            print("Матрица должна быть квадратной.")
            return None
        return self._det_logic(self.grid)

    def _det_logic(self, m):
        ln = len(m)
        if ln == 1:
            return m[0][0]
        if ln == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        d = 0
        for c in range(ln):
            # Создаем минор матрицы
            minor = [row[:c] + row[c + 1:] for row in m[1:]]
            d += ((-1) ** c) * m[0][c] * self._det_logic(minor)
        return d

    def invert(self):
        det_val = self.calculate_det()
        if det_val == 0 or det_val is None:
            print("Обратной матрицы не существует.")
            return None

        size = self.rows
        # Поиск союзной матрицы (adjugate)
        adj_mtx = []
        for i in range(size):
            tmp_row = []
            for j in range(size):
                sub = [r[:j] + r[j + 1:] for idx, r in enumerate(self.grid) if idx != i]
                tmp_row.append(((-1) ** (i + j)) * self._det_logic(sub))
            adj_mtx.append(tmp_row)

        # Транспонируем и делим на детерминант
        inv_data = [[adj_mtx[j][i] / det_val for j in range(size)] for i in range(size)]
        return MatrixHandler(inv_data)


def get_user_matrix():
    while True:
        try:
            size_in = input("Введите количество строк и столбцов (через пробел): ").split()
            r_num, c_num = int(size_in[0]), int(size_in[1])
            break
        except (ValueError, IndexError):
            print("Ошибка ввода. Нужно 2 целых числа.")

    vals = []
    print(f"Заполнение данных ({r_num}x{c_num}):")
    for i in range(r_num):
        while True:
            row_raw = input(f"Строка {i + 1}: ").split()
            if len(row_raw) != c_num:
                print(f"Нужно ввести {c_num} чисел.")
                continue
            try:
                vals.append([float(x) for x in row_raw])
                break
            except ValueError:
                print("Введите только числа.")
    return MatrixHandler(vals)


def main_loop():
    while True:
        print("\n--- ГЛАВНОЕ МЕНЮ ---")
        print("1 - Сложить")
        print("2 - Умножить на скаляр")
        print("3 - Перемножить матрицы")
        print("4 - Транспонировать/Отразить")
        print("5 - Найти детерминант")
        print("6 - Инвертировать")
        print("0 - Выйти")

        choice = input("Действие: ")

        if choice == '1':
            a, b = get_user_matrix(), get_user_matrix()
            res = a.add_matrix(b)
            if res: res.show()

        elif choice == '2':
            a = get_user_matrix()
            try:
                k = float(input("Множитель: "))
                a.multiply_by_val(k).show()
            except ValueError:
                print("Некорректное число.")

        elif choice == '3':
            a, b = get_user_matrix(), get_user_matrix()
            res = a.multiply_matrices(b)
            if res: res.show()

        elif choice == '4':
            print("Типы: 1-Главная, 2-Побочная, 3-Верт., 4-Гор.")
            m_type = input("Тип: ")
            if m_type in '1234':
                a = get_user_matrix()
                a.rotate(int(m_type)).show()

        elif choice == '5':
            a = get_user_matrix()
            d = a.calculate_det()
            if d is not None: print(f"Результат: {d}")

        elif choice == '6':
            a = get_user_matrix()
            res = a.invert()
            if res: res.show()

        elif choice == '0':
            break


if __name__ == "__main__":
    main_loop()