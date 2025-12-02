import sys  # для подключения собственного обработчика исключений
import os # для работы с файлами и папками
import json 
import traceback # для получения стека вызовов
from datetime import datetime # для фиксации времени ошибки

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOG_DIR = os.path.join(BASE_DIR, "logs") # папка для отчетов рядом с моудем

# сбор информации об ошибке
def build_error_data(exc_type, exc_value, exc_traceback): # на взод класс ошибки, текст и вызовы
    tb_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    now = datetime.now().strftime("%d.%m.%Y %H-%M-%S")

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

    # файл на запись с отступами 
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(error_data, f, ensure_ascii = False, indent = 4)

    return full_path


# глобальный обработчик необработанных исключений
def exception_handler(exc_type, exc_value, exc_traceback):
    # если пользователь сам остановил отчет не нужен
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    error_data = build_error_data(exc_type, exc_value, exc_traceback)

    report_path = save_report(error_data)

    print()
    print("Во время выполнения программы произошла ошибка.")
    print(f"Отчет об ошибке сохранен в файле: {report_path}")


# активирует модуль
def activate_error_reporting(log_dir = DEFAULT_LOG_DIR):
    global DEFAULT_LOG_DIR
    DEFAULT_LOG_DIR = log_dir

    # подмена стандартного обработчика исключений своим
    sys.excepthook = exception_handler

    print(f"Модуль отчетов об ошибках активирован. Каталог логов: {DEFAULT_LOG_DIR}")
