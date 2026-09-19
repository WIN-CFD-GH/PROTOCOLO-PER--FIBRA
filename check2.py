import re

def check():
    with open('protocolo_peru_fibra.html', encoding='utf-8') as f:
        html = f.read()
    js = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)[-1]
    
    stack = []
    in_string = False
    string_char = ''
    in_template = False
    escape = False

    lines = js.split('\n')
    for line_num, line in enumerate(lines):
        for col, char in enumerate(line):
            if escape:
                escape = False
                continue
            if char == '\\':
                escape = True
                continue
                
            if not in_string and not in_template:
                if char in ['"', "'"]:
                    in_string = True
                    string_char = char
                elif char == '`':
                    in_template = True
                elif char in ['{', '(', '[']:
                    stack.append((char, line_num + 1, col + 1))
                elif char in ['}', ')', ']']:
                    if not stack:
                        print(f"Unmatched {char} at line {line_num + 1}, col {col + 1}")
                        continue
                    last_char, last_line, last_col = stack.pop()
                    if (char == '}' and last_char != '{') or \
                       (char == ')' and last_char != '(') or \
                       (char == ']' and last_char != '['):
                        print(f"Mismatched {char} at line {line_num + 1}, col {col + 1}. Expected match for {last_char} from line {last_line}")
            elif in_string:
                if char == string_char:
                    in_string = False
            elif in_template:
                if char == '`':
                    in_template = False
                    
    for char, line, col in stack:
        print(f"Unclosed {char} from line {line}, col {col}")

if __name__ == '__main__':
    check()
