import re

def check():
    with open('protocolo_peru_fibra.html', encoding='utf-8') as f:
        html = f.read()
    js = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)[-1]
    print(f'Total length of JS: {len(js)}')

    brackets = {'{': 0, '}': 0, '[': 0, ']': 0, '(': 0, ')': 0}
    in_string = False
    string_char = ''
    in_template = False
    in_regex = False
    escape = False

    for i, char in enumerate(js):
        if escape:
            escape = False
            continue
        if char == '\\':
            escape = True
            continue
            
        if not in_string and not in_template and not in_regex:
            if char in ['"', "'"]:
                in_string = True
                string_char = char
            elif char == '`':
                in_template = True
            elif char == '/':
                # check for regex (simplistic) or comment
                pass
            elif char in brackets:
                brackets[char] += 1
        elif in_string:
            if char == string_char:
                in_string = False
        elif in_template:
            if char == '`':
                in_template = False
            elif char == '$' and i + 1 < len(js) and js[i+1] == '{':
                # inside template literal we can have ${...}, which means we enter code mode again!
                # this simple parser doesn't track deep nesting of ${}, but it's enough if we don't have it.
                pass

    print(brackets)
    print(f'{{ diff: {brackets["{"] - brackets["}"]}')
    print(f'[ diff: {brackets["["] - brackets["]"]}')
    print(f'( diff: {brackets["("] - brackets[")"]}')

if __name__ == '__main__':
    check()
