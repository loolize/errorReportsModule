import sys  # для подключения собственного обработчика исключений
import os # для работы с файлами и папками
import json 
import traceback # для получения стека вызовов
from datetime import datetime # для фиксации времени ошибки

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOG_DIR = os.path.join(BASE_DIR, "logs") # папка для отчетов рядом с моудем




# ansi цвета
RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
PURPLE = "\033[95m"
GREEN = "\033[92m"

# вывод в терминал
def print_report_to_terminal(error_data):
    print()
    print(f"{GREEN}{BOLD} " + "–"*54 + RESET)
    print(f"{GREEN}{BOLD}|                   ОТЧЕТ ОБ ОШИБКЕ                    |{RESET}")
    print(f"{GREEN}{BOLD} " + "-"*54 + RESET)

    print(f"{GREEN}Дата и время:{RESET}   {error_data.get('дата_и_время')}")
    print(f"{GREEN}Тип ошибки:{RESET}     {error_data.get('тип_ошибки')}")
    print(f"{GREEN}Сообщение:{RESET}      {error_data.get('сообщение')}")
    print()

    print(f"{PURPLE}СТЕК ВЫЗОВОВ{RESET}")
    print(f"{PURPLE}{'-'*55}{RESET}")
    print()

    raw = error_data.get("путь", "").strip().split("\n")

    formatted_frames = []
    index = 1

    for line in raw:
        line = line.strip()

        # строки формата: File "...", line X, in Y
        if line.startswith("File"):
            try:
                parts = line.split('"')
                file_name = parts[1].split("/")[-1]          # main.py
                after = parts[2]                             # , line 93, in <module>
                after = after.replace(",", "").strip()       # line 93 in <module>

                file_info = after.split()
                line_number = file_info[1]                   # 93
                func_name = file_info[3]                     # <module>/имя функции

                formatted_frames.append(
                    f"{PURPLE}{index}) {file_name}:{line_number}   -   {func_name}{RESET}"
                )
                index += 1
            except:
                continue

    # стек
    for frame in formatted_frames:
        print(frame)

    print()
    print(f"{RED}{BOLD}ИТОГ:{RESET}")
    print(f"{RED}{error_data.get('тип_ошибки')} — {error_data.get('сообщение')}{RESET}")
    print()






# сбор информации об ошибке
def build_error_data(exc_type, exc_value, exc_traceback): # на взод класс ошибки, текст и вызовы
    tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    return{
        "тип_ошибки": exc_type.__name__,
        "сообщение": str(exc_value),
        "дата_и_время": now,
        "путь": tb_text,
    }


# гарантия наличия папки
def prepare_log_path(log_dir = DEFAULT_LOG_DIR):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok = True) # еслм папки нет,
    return log_dir # путь


# генерация имени файла
def generate_filename(prefix = "error", extension = ".txt"):
    now = datetime.now()
    
    timestamp = now.strftime("%Y.%m.%d_%H-%M-%S")
    return f"{prefix}_{timestamp}{extension}" # уникальное имя формата error_дата_время.txt


# запись отчета
def save_report(error_data, log_dir = DEFAULT_LOG_DIR):
    log_dir = prepare_log_path(log_dir)

    filename = generate_filename()
    full_path = os.path.join(log_dir, filename)

    pretty_text = build_pretty_text_report(error_data)

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(pretty_text)

    return full_path



def build_pretty_text_report(error_data):
    lines = []
    lines.append(" ——————————————————————————————————————————————————————")
    lines.append("|                   ОТЧЕТ ОБ ОШИБКЕ                    |")
    lines.append(" ——————————————————————————————————————————————————————")
    lines.append("")
    lines.append(f"Дата и время:   {error_data.get('дата_и_время')}")
    lines.append(f"Тип ошибки:     {error_data.get('тип_ошибки')}")
    lines.append(f"Сообщение:      {error_data.get('сообщение')}")
    lines.append("")
    lines.append("СТЕК ВЫЗОВОВ")
    lines.append("––––––––––––––––––––––––––––––––––––––––––––––––––––––––")

    raw = error_data.get("путь", "").strip().split("\n")

    index = 1
    for line in raw:
        line = line.strip()
        if line.startswith("File"):
            try:
                parts = line.split('"')
                file_name = parts[1].split("/")[-1]
                after = parts[2].replace(",", "").strip()
                file_info = after.split()
                line_number = file_info[1]
                func_name = file_info[3]

                lines.append(f"{index}) {file_name}:{line_number} — {func_name}")
                index += 1
            except:
                pass

    lines.append("")
    lines.append("ИТОГ:")
    lines.append(f"{error_data.get('тип_ошибки')} — {error_data.get('сообщение')}")
    lines.append("")

    return "\n".join(lines)


# глобальный обработчик необработанных исключений
def exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_data = build_error_data(exc_type, exc_value, exc_traceback)

    # отчет в файл
    report_path = save_report(error_data)

    print()
    print(f"{GREEN}{BOLD}Во время выполнения программы произошла ошибка.{RESET}")
    print(f"Отчет сохранен в файле: {GREEN}{report_path}{RESET}")
    print()

    print_report_to_terminal(error_data)




# активирует модуль
def activate_error_reporting(log_dir = DEFAULT_LOG_DIR):
    global DEFAULT_LOG_DIR
    DEFAULT_LOG_DIR = log_dir

    # подмена стандартного обработчика исключений своим
    sys.excepthook = exception_handler

    print(f"Модуль отчетов об ошибках активирован. Каталог логов: {DEFAULT_LOG_DIR}")
