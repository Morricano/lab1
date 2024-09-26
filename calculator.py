import json
import math

# Локалізація через словник
locale = {
    "input_first": "Введіть перше число: ",
    "input_second": "Введіть друге число: ",
    "input_operator": "Введіть оператор (+, -, *, /, ^, %, √): ",
    "invalid_operator": "Неправильний оператор! Спробуйте ще раз.",
    "result": "Результат: ",
    "use_memory": "Використати збережене значення з пам'яті? (так/ні): ",
    "calc_again": "Виконати ще одне обчислення? (так/ні): ",
    "history": "Переглянути історію? (так/ні): ",
    "save_history": "Історія збережена у файл history.json.",
    "error_div_by_zero": "Помилка: ділення на нуль!",
    "error_negative_sqrt": "Помилка: корінь з від'ємного числа!",
    "error_invalid_input": "Помилка: введено некоректні дані!",
    "error_file": "Помилка доступу до файлу!",
    "error_unknown": "Несподівана помилка!"
}

# Читання і запис історії у файл
def save_history(history):
    try:
        with open("history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=4)
    except IOError:
        print(locale["error_file"])

def load_history():
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(locale["error_file"])
        return []

# Введення користувача і перевірка оператора
def get_operator():
    while True:
        try:
            operator = input(locale["input_operator"])
            if operator in ['+', '-', '*', '/', '^', '%', '√']:
                return operator
            print(locale["invalid_operator"])
        except Exception:
            print(locale["error_unknown"])

# Функція для виконання обчислень з використанням модуля math
def calculate(num1, num2, operator):
    try:
        if operator == '+': 
            return num1 + num2
        if operator == '-': 
            return num1 - num2
        if operator == '*': 
            return num1 * num2
        if operator == '/': 
            return num1 / num2 if num2 != 0 else locale["error_div_by_zero"]
        if operator == '^': 
            return math.pow(num1, num2)
        if operator == '%': 
            return num1 % num2
        if operator == '√': 
            return math.sqrt(num1) if num1 >= 0 else locale["error_negative_sqrt"]
    except Exception as e:
        print(f"Помилка при обчисленні: {e}")
        return None

# Основна функція
def main():
    memory = None
    history = load_history()

    # Запит точності відображення з обробкою помилок
    while True:
        try:
            precision = int(input("Введіть кількість десяткових розрядів для результату: "))
            break
        except ValueError:
            print(locale["error_invalid_input"])

    while True:
        try:
            # Використання пам'яті або запит першого числа
            if memory and input(locale["use_memory"]).strip().lower() == 'так':
                num1 = memory
                print(f"Перше число: {num1} (з пам'яті)")
            else:
                while True:
                    try:
                        num1 = float(input(locale["input_first"]))
                        break
                    except ValueError:
                        print(locale["error_invalid_input"])

            # Оператор і введення другого числа
            operator = get_operator()

            if operator != '√':
                while True:
                    try:
                        num2 = float(input(locale["input_second"]))
                        break
                    except ValueError:
                        print(locale["error_invalid_input"])
            else:
                num2 = None

            # Обчислення
            result = calculate(num1, num2, operator)
            if result is None:
                continue
            if isinstance(result, float):
                result = round(result, precision)

            print(f"{locale['result']}{result}")
            memory = result

            # Історія
            history.append(f"{num1} {operator} {num2 if num2 is not None else ''} = {result}")
            if input(locale["history"]).strip().lower() == 'так':
                print("\n".join(history))

            # Повторення обчислень
            if input(locale["calc_again"]).strip().lower() != 'так':
                save_history(history)
                print(locale["save_history"])
                break

        except ValueError:
            print(locale["error_invalid_input"])
        except Exception as e:
            print(f"Несподівана помилка: {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Несподівана критична помилка: {e}")
