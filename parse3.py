import re

with open('protocolo_peru_fibra.html', encoding='utf-8') as f:
    html = f.read()

js = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)[-1]

# Strip template literals
def strip_template_literals(code):
    result = []
    in_template = False
    escape = False
    for i, char in enumerate(code):
        if escape:
            if in_template:
                pass
            else:
                result.append(char)
            escape = False
            continue
        if char == '\\':
            if in_template:
                escape = True
            else:
                result.append(char)
                escape = True
            continue
            
        if char == '`':
            if not in_template:
                in_template = True
                result.append('"')
                result.append('T')
                result.append('E')
                result.append('M')
                result.append('P')
                result.append('L')
                result.append('"')
            else:
                in_template = False
            continue
            
        if not in_template:
            result.append(char)
            
    return "".join(result)

js_no_templ = strip_template_literals(js)

# Instead of converting with regex which is error-prone, let's just use regular expressions to find all function declarations and braces.
# Actually, let's convert arrow functions better.
def replacer(m):
    args = m.group(1)
    body = m.group(2)
    # if body has a closing parenthesis at the end that shouldn't be there...
    # actually, `=>` doesn't consume the closing parenthesis of the function call if we are careful.
    return f"function({args}) {{ return {body} }}"

js_no_templ = re.sub(r'\(\s*([\w\s,]*?)\s*\)\s*=>\s*([^{][^,;)]*)', replacer, js_no_templ)
js_no_templ = re.sub(r'(\w+)\s*=>\s*([^{][^,;)]*)', replacer, js_no_templ)
js_no_templ = re.sub(r'\(\s*([\w\s,]*?)\s*\)\s*=>\s*\{', r'function(\1) {', js_no_templ)
js_no_templ = re.sub(r'(\w+)\s*=>\s*\{', r'function(\1) {', js_no_templ)


# Convert const/let to var
js_no_templ = re.sub(r'\bconst\b', 'var', js_no_templ)
js_no_templ = re.sub(r'\blet\b', 'var', js_no_templ)

with open('debug_js.js', 'w', encoding='utf-8') as f:
    f.write(js_no_templ)

try:
    from pyjsparser import parse
    parse(js_no_templ)
    print("SUCCESS")
except Exception as e:
    print(f"pyjsparser error: {e}")
