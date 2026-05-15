import math
import argparse
import sys


class LoanCalculator:
    def __init__(self, cli_arguments):
        self.mode = cli_arguments.type
        self.loan_base = cli_arguments.principal
        self.monthly_fee = cli_arguments.payment
        self.total_periods = cli_arguments.periods
        self.yearly_interest = cli_arguments.interest

        # Валидация наличия и корректности процентной ставки
        if self.yearly_interest is None or self.yearly_interest <= 0:
            print("Ошибка: параметры указаны неверно.")
            sys.exit()

        # Месячная процентная ставка в долях
        self.fractional_rate = self.yearly_interest / (12 * 100)

    def _show_extra_costs(self, absolute_paid, initial_borrowed):
        """Вычисляет и выводит итоговую переплату."""
        print(f"Переплата по кредиту: {int(absolute_paid - initial_borrowed)}")

    def calculate_annuity_payment(self):
        """Расчет суммы ежемесячного платежа."""
        accrual_coef = (1 + self.fractional_rate) ** self.total_periods
        calculated_payout = self.loan_base * (self.fractional_rate * accrual_coef) / (accrual_coef - 1)
        calculated_payout = math.ceil(calculated_payout)
        print(f"Ваш ежемесячный аннуитетный платеж составит {calculated_payout}.")
        self._show_extra_costs(calculated_payout * self.total_periods, self.loan_base)

    def calculate_principal_value(self):
        """Расчет максимально возможной суммы займа."""
        accrual_coef = (1 + self.fractional_rate) ** self.total_periods
        derived_principal = self.monthly_fee / ((self.fractional_rate * accrual_coef) / (accrual_coef - 1))
        derived_principal = math.floor(derived_principal)
        print(f"Основная сумма займа: {derived_principal}.")
        self._show_extra_costs(self.monthly_fee * self.total_periods, derived_principal)

    def calculate_period_length(self):
        """Расчет времени, необходимого для погашения долга."""
        ratio_argument = self.monthly_fee / (self.monthly_fee - self.fractional_rate * self.loan_base)
        evaluated_months = math.ceil(math.log(ratio_argument, 1 + self.fractional_rate))

        years_num, leftover_months = divmod(evaluated_months, 12)
        time_strings = []
        if years_num > 0:
            time_strings.append(f"{years_num} {'год' if years_num == 1 else 'года' if 2 <= years_num <= 4 else 'лет'}")
        if leftover_months > 0:
            time_strings.append(f"{leftover_months} {'месяц' if leftover_months == 1 else 'месяца' if 2 <= leftover_months <= 4 else 'месяцев'}")

        print(f"Срок выплаты составит {' и '.join(time_strings)}.")
        self._show_extra_costs(self.monthly_fee * evaluated_months, self.loan_base)

    def calculate_diff_payments(self):
        """Расчет дифференцированных платежей по месяцам."""
        cumulative_payout = 0
        for current_month in range(1, self.total_periods + 1):
            cleared_part = self.loan_base * (current_month - 1) / self.total_periods
            periodic_charge = (self.loan_base / self.total_periods) + self.fractional_rate * (self.loan_base - cleared_part)
            periodic_charge = math.ceil(periodic_charge)
            cumulative_payout += periodic_charge
            print(f"Месяц {current_month}: платеж — {periodic_charge}")

        self._show_extra_costs(cumulative_payout, self.loan_base)

    def is_input_valid(self):
        """Проверка логической связности и корректности входных данных."""
        metrics_list = [self.loan_base, self.monthly_fee, self.total_periods, self.yearly_interest]
        # Значения не могут быть отрицательными
        if any(metric is not None and metric < 0 for metric in metrics_list):
            return False

        # Дифференцированные платежи несовместимы с фиксированным ежемесячным взносом
        if self.mode == "diff" and self.monthly_fee is not None:
            return False

        # Должно быть заполнено минимум 4 параметра из 5 (тип + 3 числовых)
        core_metrics = [self.loan_base, self.monthly_fee, self.total_periods]
        if sum(1 for target in core_metrics if target is not None) < 2:
            return False

        return True

    def process(self):
        """Запуск соответствующего алгоритма расчета."""
        if not self.is_input_valid():
            print("Ошибка: параметры указаны неверно.")
            return

        if self.mode == "annuity":
            if self.monthly_fee is None:
                self.calculate_annuity_payment()
            elif self.loan_base is None:
                self.calculate_principal_value()
            elif self.total_periods is None:
                self.calculate_period_length()
        elif self.mode == "diff":
            self.calculate_diff_payments()
        else:
            print("Ошибка: тип расчета не определен.")


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Финансовый калькулятор")

    arg_parser.add_argument("--type", choices=["annuity", "diff"], help="Тип платежа")
    arg_parser.add_argument("--principal", type=float, help="Тело кредита")
    arg_parser.add_argument("--payment", type=float, help="Ежемесячный взнос")
    arg_parser.add_argument("--periods", type=int, help="Срок в месяцах")
    arg_parser.add_argument("--interest", type=float, help="Процентная ставка (годовая)")

    parsed_parameters = arg_parser.parse_args()
    finance_app = LoanCalculator(parsed_parameters)
    finance_app.process()