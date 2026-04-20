class CoffeeUnit:
    def __init__(self):
        # Начальные запасы
        self.w_volume = 400
        self.m_volume = 540
        self.b_stock = 120
        self.c_count = 9
        self.cash = 550
        # Текущий режим системы
        self.mode = "idle"

    def _parse_input(self, data):
        try:
            return int(data)
        except ValueError:
            print("Ошибка: требуется числовой ввод.")
            return None

    def process(self, cmd):
        if self.mode == "idle":
            self.navigation(cmd)
        elif self.mode == "selection":
            self.execute_purchase(cmd)
        elif self.mode.startswith("refill"):
            self.update_inventory(cmd)

    def navigation(self, task):
        if task == "buy":
            self.mode = "selection"
            print("Что желаете купить? 1 - эспрессо, 2 - латте, 3 - капучино, back – назад:")

        elif task == "fill":
            self.mode = "refill_w"
            print("Введите количество воды (мл):")

        elif task == "take":
            print(f"Выдано: ${self.cash}")
            self.cash = 0

        elif task == "remaining":
            self.show_report()

        elif task == "exit":
            self.mode = "shutdown"

        else:
            print("Команда не распознана. Доступно: buy, fill, take, remaining, exit.")

    def execute_purchase(self, item_id):
        if item_id == "back":
            self.mode = "idle"
            return

        # Настройки напитков: [вода, молоко, зерна, цена]
        menu = {
            "1": [250, 0, 16, 4],
            "2": [350, 75, 20, 7],
            "3": [200, 100, 12, 6]
        }

        specs = menu.get(item_id)
        if not specs:
            print("Вариант отсутствует.")
            self.mode = "idle"
            return

        w_req, m_req, b_req, price = specs

        if self.w_volume < w_req:
            print("Недостаточно воды!")
        elif self.m_volume < m_req:
            print("Недостаточно молока!")
        elif self.b_stock < b_req:
            print("Недостаточно кофейных зерен!")
        elif self.c_count < 1:
            print("Нет стаканчиков!")
        else:
            self.w_volume -= w_req
            self.m_volume -= m_req
            self.b_stock -= b_req
            self.c_count -= 1
            self.cash += price
            print("Ингредиентов достаточно, начинаю приготовление!")

        self.mode = "idle"

    def update_inventory(self, val):
        amount = self._parse_input(val)
        if amount is None:
            return

        if self.mode == "refill_w":
            self.w_volume += amount
            self.mode = "refill_m"
            print("Введите количество молока (мл):")

        elif self.mode == "refill_m":
            self.m_volume += amount
            self.mode = "refill_b"
            print("Введите вес зерен (г):")

        elif self.mode == "refill_b":
            self.b_stock += amount
            self.mode = "refill_c"
            print("Введите количество стаканов (шт):")

        elif self.mode == "refill_c":
            self.c_count += amount
            self.mode = "idle"

    def show_report(self):
        print("\n=== Текущие ресурсы ===")
        print(f"Вода: {self.w_volume} мл")
        print(f"Молоко: {self.m_volume} мл")
        print(f"Зерна: {self.b_stock} г")
        print(f"Стаканы: {self.c_count} шт")
        print(f"Баланс: ${self.cash}\n")


# Цикл управления
app = CoffeeUnit()

while app.mode != "shutdown":
    if app.mode == "idle":
        print("Выберите действие (buy, fill, take, remaining, exit):")

    entry = input("> ")
    app.process(entry)