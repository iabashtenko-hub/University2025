class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    @staticmethod
    def read():
        while True:
            parts = input().split()
            if len(parts) == 2:
                n, m = parts
                break
            print("Please enter two numbers: rows and columns.")

        n, m = int(float(n)), int(float(m))

        data = []
        for _ in range(n):
            row = list(map(float, input().split()))
            if len(row) != m:
                raise ValueError("Row length does not match matrix size.")
            data.append(row)

        return Matrix(data)

    def print(self):
        for row in self.data:
            print(" ".join(str(x).rstrip('0').rstrip('.') if x % 1 == 0 else str(x) for x in row))

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            return None
        res = []
        for i in range(self.rows):
            row = [self.data[i][j] + other.data[i][j] for j in range(self.cols)]
            res.append(row)
        return Matrix(res)

    def mul_const(self, c):
        res = []
        for row in self.data:
            res.append([x * c for x in row])
        return Matrix(res)

    def mul_matrix(self, other):
        if self.cols != other.rows:
            return None
        res = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                s = 0
                for k in range(self.cols):
                    s += self.data[i][k] * other.data[k][j]
                row.append(s)
            res.append(row)
        return Matrix(res)


    def transpose_main(self):
        res = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(res)

    def transpose_side(self):
        res = [[self.data[self.rows - 1 - j][self.cols - 1 - i] for j in range(self.rows)] for i in range(self.cols)]
        return Matrix(res)

    def transpose_vertical(self):
        res = [list(reversed(row)) for row in self.data]
        return Matrix(res)

    def transpose_horizontal(self):
        res = list(reversed(self.data))
        return Matrix(res)

    def determinant(self):
        if self.rows != self.cols:
            return None
        return self._det(self.data)

    def _det(self, matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]

        det = 0
        for col in range(n):
            minor = [row[:col] + row[col+1:] for row in matrix[1:]]
            det += ((-1) ** col) * matrix[0][col] * self._det(minor)
        return det

    def inverse(self):
        det = self.determinant()
        if det == 0 or det is None:
            return None

        n = self.rows
        cof = []
        for i in range(n):
            row = []
            for j in range(n):
                minor = [r[:j] + r[j+1:] for k, r in enumerate(self.data) if k != i]
                row.append(((-1)**(i + j)) * self._det(minor))
            cof.append(row)

        adj = Matrix(cof).transpose_main()

        inv = adj.mul_const(1 / det)
        return inv



def run():
    while True:
        print("1. Add matrices")
        print("2. Multiply matrix by a constant")
        print("3. Multiply matrices")
        print("4. Transpose matrix")
        print("5. Calculate a determinant")
        print("6. Inverse matrix")
        print("0. Exit")

        choice = input("Your choice: > ").strip()

        if choice == "0":
            break

        elif choice == "1":
            print("Enter size of first matrix: > ", end="")
            A = Matrix.read()
            print("Enter first matrix:")
            print("Enter size of second matrix: > ", end="")
            B = Matrix.read()
            print("Enter second matrix:")
            res = A.add(B)
            if res is None:
                print("The operation cannot be performed.")
            else:
                print("The result is:")
                res.print()

        elif choice == "2":
            print("Enter size of matrix: > ", end="")
            A = Matrix.read()
            print("Enter matrix:")
            c = float(input("Enter constant: > "))
            res = A.mul_const(c)
            print("The result is:")
            res.print()

        elif choice == "3":
            print("Enter size of first matrix: > ", end="")
            A = Matrix.read()
            print("Enter first matrix:")
            print("Enter size of second matrix: > ", end="")
            B = Matrix.read()
            print("Enter second matrix:")
            res = A.mul_matrix(B)
            if res is None:
                print("The operation cannot be performed.")
            else:
                print("The result is:")
                res.print()

        elif choice == "4":
            print("1. Main diagonal")
            print("2. Side diagonal")
            print("3. Vertical line")
            print("4. Horizontal line")
            t_choice = input("Your choice: > ").strip()

            print("Enter matrix size: > ", end="")
            A = Matrix.read()
            print("Enter matrix:")

            options = {
                "1": A.transpose_main,
                "2": A.transpose_side,
                "3": A.transpose_vertical,
                "4": A.transpose_horizontal
            }

            if t_choice in options:
                print("The result is:")
                options[t_choice]().print()

        elif choice == "5":
            print("Enter matrix size: > ", end="")
            A = Matrix.read()
            print("Enter matrix:")
            det = A.determinant()
            print("The result is:")
            print(det)

        elif choice == "6":
            print("Enter matrix size: > ", end="")
            A = Matrix.read()
            print("Enter matrix:")
            inv = A.inverse()
            if inv is None:
                print("This matrix doesn't have an inverse.")
            else:
                print("The result is:")
                inv.print()


if __name__ == "__main__":
    run()
