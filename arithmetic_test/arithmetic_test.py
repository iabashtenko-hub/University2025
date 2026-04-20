class MatrixProcessor:
    def __init__(self, data):
        self.matrix = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def print_me(self):
        for r in self.matrix:
            # Форматирование :g убирает лишние нули
            print(' '.join(f"{round(x, 2):g}" for x in r))

    def addition(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            print("Размеры не совпадают!")
            return None
        res = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)]
               for i in range(self.rows)]
        return MatrixProcessor(res)

    def multiplier(self, n):
        res = [[item * n for item in row] for row in self.matrix]
        return MatrixProcessor(res)

    def dot(self, other):
        if self.cols != other.rows:
            print("Некорректные размерности для умножения.")
            return None
        res = [[sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols))
                for j in range(other.cols)] for i in range(self.rows)]
        return MatrixProcessor(res)

    def modify(self, mode=1):
        if mode == 1: # Главная
            res = [[self.matrix[j][i] for j in range(self.rows)] for i in range(self.cols)]
        elif mode == 2: # Побочная
            res = [[self.matrix[self.rows - 1 - j][self.cols - 1 - i] for j in range(self.rows)]
                   for i in range(self.cols)]
        elif mode == 3: # Вертикальное отражение
            res = [r[::-1] for r in self.matrix]
        elif mode == 4: # Горизонтальное отражение
            res = self.matrix[::-1]
        else:
            return None
        return MatrixProcessor(res)

    def determinant(self):
        if self.rows != self.cols:
            print("Нужна квадратная матрица.")
            return None
        return self._do_det(self.matrix)

    def _do_det(self, m):
        if len(m) == 1:
            return m[0][0]
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        val = 0
        for c in range(len(m)):
            minor = [row[:c] + row[c+1:] for row in m[1:]]
            val += ((-1) ** c) * m[0][c] * self._do_det(minor)
        return val

    def inverse(self):
        d = self.determinant()
        if not d:
            print("Матрица вырожденная.")
            return None

        size = self.rows
        adj = []
        for i in range(size):
            line = []
            for j in range(size):
                sub = [r[:j] + r[j+1:] for idx, r in enumerate(self.matrix) if idx != i]
                line.append(((-1) ** (i + j)) * self._do_det(sub))
            adj.append(line)

        # Транспонируем сразу при создании финального списка
        inv_grid = [[adj[j][i] / d for j in range(size)] for i in range(size)]
        return MatrixProcessor(inv_grid)


def get_matrix():
    while True:
        try:
            inp = input("Введите размер (R C): ").split()
            r, c = int(inp[0]), int(inp[1])
            break
        except:
            print("Ошибка ввода параметров.")

    data = []
    print(f"Введите {r} строк(и):")
    for _ in range(r):
        while True:
            line = input("> ").split()
            if len(line) == c:
                try:
                    data.append([float(x) for x in line])
                    break
                except:
                    print("Только числа!")
            else:
                print(f"Нужно {c} значений.")
    return MatrixProcessor(data)


def main():
    while True:
        print("\n1. Сложить\n2. На число\n3. Умножить\n4. Транспонировать\n5. Дет.\n6. Обратная\n0. Выход")
        cmd = input("Выбор: ")

        if cmd == '1':
            m1, m2 = get_matrix(), get_matrix()
            res = m1.addition(m2)
            if res: res.print_me()
        elif cmd == '2':
            m = get_matrix()
            try:
                num = float(input("Множитель: "))
                m.multiplier(num).print_me()
            except: pass
        elif cmd == '3':
            m1, m2 = get_matrix(), get_matrix()
            res = m1.dot(m2)
            if res: res.print_me()
        elif cmd == '4':
            print("1-Гл, 2-Поб, 3-Верт, 4-Гор")
            t = int(input("Тип: "))
            get_matrix().modify(t).print_me()
        elif cmd == '5':
            d = get_matrix().determinant()
            if d is not None: print("Определитель:", round(d, 4))
        elif cmd == '6':
            res = get_matrix().inverse()
            if res: res.print_me()
        elif cmd == '0':
            break

if __name__ == "__main__":
    main()