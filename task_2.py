import re
from typing import Callable


def generator_numbers(text: str):
    pattern = r"(?<= )\d+\.\d{2}(?= )"
    for match in re.finditer(pattern, text):
        yield float(match.group())


def sum_profit(text: str, func: Callable):
    res = 0.0
    for sum in func(text):
        res += sum
    return res


def main():
    text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")


if __name__ == "__main__":
    main()
