import argparse
import re

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

