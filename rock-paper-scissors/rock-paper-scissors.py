import random


class RockPaperScissorsPlus:
    DEFAULT_CHOICES = ["rock", "paper", "scissors"]

    # Игровые статусы
    STATE_PREPARATION = 0
    STATE_IN_GAME = 1
    STATE_TERMINATED = 2

    def __init__(self, save_file_path: str = "rating.txt"):
        self.save_path = save_file_path
        self.username = ""
        self.points = 0
        self.options = self.DEFAULT_CHOICES.copy()
        self.current_state = self.STATE_PREPARATION

    def _load_user_score(self) -> None:
        """Получение очков игрока из текстового файла базы."""
        try:
            with open(self.save_path, "r", encoding="utf-8") as file_reader:
                for current_line in file_reader:
                    user_id, current_points = current_line.strip().split()
                    if user_id == self.username:
                        self.points = int(current_points)
                        return
        except (FileNotFoundError, ValueError):
            pass
        self.points = 0

    def launch(self) -> None:
        self.username = input("Введите имя пользователя:\n> ").strip()
        print(f"Добро пожаловать, {self.username}!")
        self._load_user_score()
        self.show_controls()

    def show_controls(self):
        print("Команды управления:")
        print("!start  — переход к игре")
        print("!rating — посмотреть очки")
        print("!exit   — выход из приложения")
        print("Чтобы изменить список фигур, введите их через запятую (минимум 3 варианта) до начала игры.")

    def set_custom_variants(self, user_input_str: str) -> None:
        cleaned_input = user_input_str.strip()

        # Если строка пустая — ставим дефолт
        if not cleaned_input:
            self.options = self.DEFAULT_CHOICES.copy()
            print("Используются стандартные параметры.")
            return

        # Разбиваем и чистим список
        parsed_elements = [item.strip() for item in cleaned_input.split(",") if item.strip()]

        # ПРОВЕРКА: Нужно минимум 3 символа для корректной логики
        if len(parsed_elements) < 3:
            print("Ошибка: для игры нужно минимум 3 различных символа!")
            print(f"Оставлен текущий набор: {', '.join(self.options)}")
        else:
            self.options = parsed_elements
            print(f"Параметры обновлены. Текущий набор: {', '.join(self.options)}")

    def _check_computer_win(self, human_move: str, ai_move: str) -> bool:
        """Реализация круговой логики: бьет ли компьютерный выбор выбор игрока."""
        position_index = self.options.index(human_move)
        # Перестраиваем список так, чтобы выбор пользователя был в начале
        shifted_list = self.options[position_index + 1:] + self.options[:position_index]
        # Половина элементов после выбора игрока считаются выигрышными для ПК
        target_half_size = len(shifted_list) // 2
        return ai_move in shifted_list[:target_half_size]

    def play_turn(self, chosen_move: str) -> None:
        bot_move = random.choice(self.options)

        if bot_move == chosen_move:
            print(f"Результат: ничья ({bot_move})")
            self.points += 50
        elif self._check_computer_win(chosen_move, bot_move):
            print(f"Поражение. Компьютер выбрал {bot_move}")
        else:
            print(f"Победа! Вы обыграли {bot_move}")
            self.points += 100

    def _handle_input(self, raw_command: str):
        if raw_command == "!exit":
            print("Завершение программы. Всего доброго!")
            self.current_state = self.STATE_TERMINATED
            return

        if raw_command == "!rating":
            print(f"Ваш текущий счет: {self.points}")
            return

        if self.current_state == self.STATE_PREPARATION:
            if raw_command == "!help":
                self.show_controls()
            elif raw_command == "!start":
                print("Бой начался! Вводите выбранную фигуру.")
                self.current_state = self.STATE_IN_GAME
            else:
                self.set_custom_variants(raw_command)

        elif self.current_state == self.STATE_IN_GAME:
            if raw_command in self.options:
                self.play_turn(raw_command)
            else:
                print(f"Неизвестный вариант. Доступны: {', '.join(self.options)} или !exit.")

    def run(self):
        self.launch()

        while self.current_state != self.STATE_TERMINATED:
            entered_text = input("> ").strip()
            if not entered_text:
                continue
            self._handle_input(entered_text)


if __name__ == "__main__":
    game_instance = RockPaperScissorsPlus()
    game_instance.run()