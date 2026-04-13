class TextMarkupProcessor:
    def __init__(self):
        self.buffer = ""
        # Разделил опции на логические группы
        self.valid_styles = {
            "plain", "bold", "italic", "header", "link",
            "inline-code", "ordered-list", "unordered-list", "new-line"
        }
        self.system_actions = {"!help", "!done", "exit"}

    def show_instructions(self):
        print("Доступные инструменты разметки: " + ", ".join(self.valid_styles))
        print("Системные вызовы: !help (помощь), !done (сохранить и выйти)")

    def _ask_for_count(self):
        while True:
            try:
                val = int(input("Укажите количество строк: > "))
                if val > 0:
                    return val
                print("Ошибка: значение должно быть положительным числом.")
            except ValueError:
                print("Ошибка: введите корректное целое число.")

    def execute(self):
        print("Запущен процессор Markdown-разметки.")
        print("Для вывода списка команд введите !help. Для выхода без сохранения — exit.")

        while True:
            cmd = input("Выберите тип разметки или команду:\n> ").strip().lower()

            if cmd in self.system_actions:
                if cmd == "!help":
                    self.show_instructions()
                elif cmd == "!done":
                    with open("output.md", "w", encoding="utf-8") as file_out:
                        file_out.write(self.buffer)
                    print("Данные успешно экспортированы в output.md. Завершение.")
                    break
                elif cmd == "exit":
                    print("Выход выполнен без сохранения изменений.")
                    break
                continue

            if cmd not in self.valid_styles:
                print("Ошибка: неизвестный тип форматирования или команда.")
                continue

            # Обработка текстовых блоков
            if cmd == "plain":
                content = input("Введите текст: > ")
                self.buffer += content

            elif cmd == "bold":
                content = input("Текст для жирного шрифта: > ")
                self.buffer += f"**{content}**"

            elif cmd == "italic":
                content = input("Текст для курсива: > ")
                self.buffer += f"*{content}*"

            elif cmd == "inline-code":
                content = input("Код: > ")
                self.buffer += f"`{content}`"

            elif cmd == "header":
                while True:
                    try:
                        lvl = int(input("Уровень заголовка (1-6): > "))
                        if 1 <= lvl <= 6:
                            break
                        print("Уровень должен быть в диапазоне от 1 до 6.")
                    except ValueError:
                        print("Введите число от 1 до 6.")
                content = input("Текст заголовка: > ")
                self.buffer += f"{'#' * lvl} {content}\n"

            elif cmd == "link":
                anchor = input("Текст ссылки (Label): > ")
                href = input("URL адрес: > ")
                self.buffer += f"[{anchor}]({href})"

            elif cmd == "new-line":
                if self.buffer.endswith("\n\n"):
                    pass
                elif self.buffer.endswith("\n"):
                    self.buffer += "\n"
                else:
                    self.buffer += "\n\n"

            elif cmd in ("ordered-list", "unordered-list"):
                num_rows = self._ask_for_count()
                if self.buffer and not self.buffer.endswith("\n"):
                    self.buffer += "\n"

                for i in range(1, num_rows + 1):
                    line_data = input(f"Элемент списка #{i}: > ")
                    if cmd == "ordered-list":
                        self.buffer += f"{i}. {line_data}\n"
                    else:
                        self.buffer += f"* {line_data}\n"
                self.buffer += "\n"

            # Вывод текущего состояния документа
            print("--- Текущий результат ---")
            print(self.buffer)
            print("-------------------------")


if __name__ == "__main__":
    processor = TextMarkupProcessor()
    processor.execute()