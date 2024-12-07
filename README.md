## Постановка задачи
Разработать инструмент командной строки для учебного конфигурационного 
языка, синтаксис которого приведен далее. Этот инструмент преобразует текст из 
входного формата в выходной. Синтаксические ошибки выявляются с выдачей 
сообщений. 

Входной текст на учебном конфигурационном языке принимается из 
файла, путь к которому задан ключом командной строки. Выходной текст на 
языке toml попадает в файл, путь к которому задан ключом командной строки. 
Однострочные комментарии: 

```
% Это однострочный комментарий
```
Многострочные комментарии:

```
/+ 
Это многострочный 
комментарий 
+/
```
Словари: 

```
@{ 
имя = значение; 
имя = значение; 
имя = значение; 
... 
}
```
Имена: 

```
[a-z][a-z0-9_]*
```
Значения:

• Числа. 

• Словари. 

Объявление константы на этапе трансляции: 

```
имя is значение;
```
Вычисление константы на этапе трансляции: 

```
[имя]
```

Результатом вычисления константного выражения является значение. 
Все конструкции учебного конфигурационного языка (с учетом их 
возможной вложенности) должны быть покрыты тестами. Необходимо показать 2 
примера описания конфигураций из разных предметных областей.
## Описание основных функций
**1. parse_config(input_text)**

```
def parse_config(input_text):
    lines = input_text.splitlines()
    output_lines = []
    constants = {}
    dict_stack = []
    current_dict_name = ""
    inside_dict = False
    lines_iter = iter(lines)

    for line in lines:
        line = line.strip()

        if line.startswith('%'):
            continue
        
        if line.startswith('/+'):
            while '+/' not in line:
                line = next(lines_iter).strip()
        
        const_match = re.match(r'(\w+)\s+is\s+(.+);', line)
        if const_match:
            name, value = const_match.groups()
            constants[name] = value.strip()
            continue
        
        const_eval_match = re.match(r'(\w+)\s*=\s*\[(.+?)\]', line)
        if const_eval_match:
            name = const_eval_match.group(1)
            value = const_eval_match.group(2)
            if value in constants:
                output_lines.append(f"{'    ' * len(dict_stack)}{name} = {constants[value]}")
            else:
                print(f"Ошибка: Константа '{value}' не объявлена.")
            continue
        
        dict_match = re.match(r'"(\w+)"\s+=\s+@\{', line)
        if dict_match:
            current_dict_name = dict_match.group(1)
            output_lines.append(f'\n{"    " * len(dict_stack)}[{current_dict_name}]\n')
            dict_stack.append(current_dict_name)
            inside_dict = True
            continue
        
        if inside_dict:
            if line == '}':
                dict_stack.pop()
                inside_dict = bool(dict_stack)
                continue
            
            dict_entry_match = re.match(r'(\w+)\s*=\s*(.+);', line)
            if dict_entry_match:
                key, value = dict_entry_match.groups()
                output_lines.append(f"{"    " * len(dict_stack)}{key} = {value.strip().strip(';')}")
                continue
            
            print(f"Ошибка: Неверный формат записи в словаре: '{line}'")
            continue
        
    return '\n'.join(output_lines)
```

*Описание:*

Функция принимает строку input_text, которая содержит конфигурационные данные в учебном формате, и парсит её, преобразуя в формат TOML.
В процессе парсинга функция обрабатывает объявление констант, вычисление констант, объявление словарей и их записи. 
Результат работы функции - строка в формате TOML.

**2. main()**
```
def main():
    parser = argparse.ArgumentParser(description="Конвертер учебного конфигурационного языка в формат TOML.")
    parser.add_argument('input_file', help='Путь к входному файлу с конфигурацией.')
    parser.add_argument('output_file', help='Путь к выходному файлу в формате TOML.')
    
    args = parser.parse_args()
    
    try:
        with open(args.input_file, 'r', encoding='utf-8') as infile:
            input_text = infile.read()
        
        output_text = parse_config(input_text)
        
        with open(args.output_file, 'w', encoding='utf-8') as outfile:
            outfile.write(output_text)
        
        print("Конвертация завершена успешно.")
    
    except FileNotFoundError:
        print(f"Ошибка: Файл '{args.input_file}' не найден.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
```

*Описание:*

Это основная функция скрипта.
Она использует argparse для обработки аргументов командной строки (путь к входному файлу с конфигурацией и путь к выходному файлу), читает содержимое входного файла, парсит его с помощью parse_config(),
записывает результат в выходной файл и выводит сообщение об успешном завершении операции или сообщение об ошибке, если что-то пошло не так.

## Сборка проекта
*Комманда для запуска эмулятора для языка оболочки ОС:*
```
python config_parser.py input_web.txt output_file.toml 
```
*Комманда для запуска тестов:*
```
python -m pytest
```

## Примеры использования
Файл input_app.txt:

![Скриншот 07-12-2024 145639](https://github.com/user-attachments/assets/5817ad2b-554a-493b-a12d-e976a94e2cc7)

Файл input_web.txt:

![Скриншот 07-12-2024 145722](https://github.com/user-attachments/assets/d23dc457-691f-4f5c-ab55-69914fd9a803)

Результат работы с файлом input_app.txt:

![image](https://github.com/user-attachments/assets/66bd9d24-a832-4df6-9487-95af439d9245)

Результат работы с файлом input_web.txt:

![image](https://github.com/user-attachments/assets/7b48dade-ca06-4263-bb89-6e9f354f18d9)

## Результаты прогона тестов

![результаты тестирования](https://github.com/user-attachments/assets/a657dd07-c813-4ca4-ae0c-9f915b9a3827)

