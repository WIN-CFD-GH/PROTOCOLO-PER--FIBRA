import re

with open('protocolo_peru_fibra.html', encoding='utf-8') as f:
    html = f.read()

js = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)[-1]

# Strip all template literals from JS to see if they contain unmatched braces?
# Better: Just count the braces ignoring template literals again, but correctly.

def find_first_syntax_error(code):
    try:
        from pyjsparser import parse
        parse(code)
    except Exception as e:
        print(f"pyjsparser error: {e}")

find_first_syntax_error(js)
