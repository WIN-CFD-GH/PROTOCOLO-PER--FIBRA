import re

with open('protocolo_peru_fibra.html', encoding='utf-8') as f:
    text = f.read()

start = text.find('const protocolData = [')
end = text.find('];', start)

data = text[start:end+2]

# Strip strings
s = re.sub(r"'[^']*'", 'STR', data)
s = re.sub(r'"[^"]*"', 'STR', s)

# Strip template literals
def strip_template_literals(code):
    result = []
    in_template = False
    escape = False
    for i, char in enumerate(code):
        if escape:
            if not in_template:
                result.append(char)
            escape = False
            continue
        if char == '\\':
            if not in_template:
                result.append(char)
            escape = True
            continue
            
        if char == '`':
            in_template = not in_template
            if in_template:
                result.append('STR')
            continue
            
        if not in_template:
            result.append(char)
            
    return "".join(result)

s = strip_template_literals(s)

print('Left braces: ', s.count('{'))
print('Right braces: ', s.count('}'))
print('Left brackets: ', s.count('['))
print('Right brackets: ', s.count(']'))
print('Left parens: ', s.count('('))
print('Right parens: ', s.count(')'))
