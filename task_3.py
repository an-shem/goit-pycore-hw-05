import sys
from collections import defaultdict
from pathlib import Path
from colorama import Fore, init as colorama_init

""" 
startup script: python task_3.py src/logfile.log [log level: info/error/debug/warning ]
"""


def parse_log_line(line: str) -> dict:
    """
    Function for parsing log strings.
    """
    log = line.split(maxsplit=3)
    return {
        "date": log[0].strip(),
        "time": log[1].strip(),
        "level": log[2].strip(),
        "message": log[3].strip(),
    }


def load_logs(file_path: str) -> list:
    """
    Function for loading logs from a file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [parse_log_line(line) for line in file]
    except:
        print(Fore.RED + "There was a problem reading the file.")
        return []


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Function for filtering logs by level.
    """
    return list(filter(lambda log: log["level"].lower() == level.lower(), logs))


def count_logs_by_level(logs: list) -> dict:
    """
    Function for counting records by logging level.
    """
    counted_logs = defaultdict(int)
    for log in logs:
        counted_logs[log["level"]] += 1
    return dict(counted_logs)


def display_log_counts(counts: dict):
    """
    A function that formats and displays the results. It accepts the results of the count_logs_by_level function.
    """
    headers = ["Рівень логування", "Кількість"]

    # calculate the width of columns
    col1_width = max(len(headers[0]), max(len(level) for level in counts))
    col2_width = max(len(headers[1]), max(len(str(count)) for count in counts.values()))

    # print the headline
    print(Fore.MAGENTA + f"{headers[0]:<{col1_width}} | {headers[1]:<{col2_width}}")
    print(Fore.MAGENTA + "-" * col1_width + "-|-" + "-" * col2_width)

    # print lines
    for level, count in counts.items():
        level_color = Fore.WHITE
        if level == "ERROR":
            level_color = Fore.RED
        if level == "INFO":
            level_color = Fore.GREEN
        if level == "DEBUG":
            level_color = Fore.BLUE
        if level == "WARNING":
            level_color = Fore.YELLOW
        print(
            f"{level_color}{level:<{col1_width}}{Fore.MAGENTA} | {level_color}{count:<{col2_width}}"
        )


def main():
    colorama_init(autoreset=True)
    if len(sys.argv) <= 1:
        print(Fore.RED + "You have not specified the path to the log file.")
        return 1
    p = Path(sys.argv[1])
    if not p.exists():
        print(Fore.RED + "The specified file does not exist.")
        return 1
    if not p.is_file():
        print(Fore.RED + "You specified the path not to the file.")
        return 1
    list_dict_for_logs = load_logs(p)
    if not list_dict_for_logs:
        return 1
    list_counted_logs = count_logs_by_level(list_dict_for_logs)
    print()
    display_log_counts(list_counted_logs)
    if len(sys.argv) >= 3:
        list_sorted_logs = filter_logs_by_level(list_dict_for_logs, sys.argv[2])
        print()
        print(f"{Fore.CYAN}Деталі логів для рівня '{sys.argv[2].upper()}':")
        for log_info in list_sorted_logs:
            print(
                log_info["date"],
                log_info["time"],
                "-",
                log_info["message"],
            )
    print()
    return 0


if __name__ == "__main__":
    main()
