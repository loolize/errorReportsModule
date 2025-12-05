import error_module


def divide():
    a_str = input("Введите делимое: ")
    b_str = input("Введите делитель (0 для ошибки): ")

    a = int(a_str)
    b = int(b_str)

    result = a / b
    print(f"Результат деления: {result}")


def list_index():
    items = ["первый", "второй", "третий"]

    print("Содержимое списка:", items)
    index_str = input("Введите индекс элемента (для ошибки > 2): ")

    index = int(index_str)
    # при выходе за границы возникнет ошибка
    value = items[index]
    print(f"Выбранный элемент: {value}")


def file_read():
    filename = input("Введите имя файла (несуществующее имя для ошибки): ")

    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    print("\nСодержимое:")
    print()
    print(content)
    print()


def show_menu():
    print()
    print(" ОТЧЕТЫ ОБ ОШИБКАХ тесты")
    print()
    print("1 — Деление")
    print("2 — Доступ к элементу списка")
    print("3 — Чтение файла")
    print("0 — Выход")
    print()


def main():
    error_module.activate_error_reporting()

    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            divide()

        elif choice == "2":
            list_index()

        elif choice == "3":
            file_read()

        elif choice == "0":
            print("Завершение работы программы.")
            break
        else:
            print("Неизвестная команда. Повторите ввод.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
