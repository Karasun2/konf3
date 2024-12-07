import argparse
import re
import sys

def parse_config(input_text):
    lines = input_text.splitlines()
    output_lines = []
    constants = {}
    inside_dict = False
    current_dict_name = ""

    for line in lines:
        line = line.strip()
        
        # Пропуск однострочных комментариев
        if line.startswith('%'):
            continue
        
        # Обработка многострочных комментариев
        if '/+' in line:
            # Удаляем многострочные комментарии
            line = re.sub(r'/\+.*?\+\//', '', line)
            line = line.strip()
            if not line:  # Если строка пустая после удаления комментариев, пропускаем
                continue
        
        # Обработка объявления константы
        const_match = re.match(r'(\w+)\s+is\s+(.+);', line)
        if const_match:
            name, value = const_match.groups()
            constants[name] = value.strip()
            continue
        
        # Обработка вычисления константы
        const_eval_match = re.match(r'\[(\w+)\]', line)
        if const_eval_match:
            name = const_eval_match.group(1)
            if name in constants:
                output_lines.append(f"{name} = {constants[name]}")
            else:
                print(f"Ошибка: Константа '{name}' не объявлена.")
            continue
        
        # Обработка начала словаря
        dict_match = re.match(r'"(\w+)"\s+=\s+@\{', line)
        if dict_match:
            current_dict_name = dict_match.group(1)
            output_lines.append(f'[{current_dict_name}]')
            inside_dict = True
            continue
        
        # Обработка элементов словаря
        if inside_dict:
            if line == '}':
                inside_dict = False
                continue
            
            dict_entry_match = re.match(r'(\w+)\s*=\s*(.+);', line)
            if dict_entry_match:
                key, value = dict_entry_match.groups()
                output_lines.append(f"{key} = {value.strip().strip(';')}")
                continue
            
        
        # Проверка на синтаксическую ошибку
        if line:
            print(f"Ошибка: Непонятная строка: '{line}'")
    
    # Включение всех констант в выходной файл в конце
    for name, value in constants.items():
        output_lines.append(f"{name} = {value}")

    return '\n'.join(output_lines)

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
