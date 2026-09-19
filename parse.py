import re
import traceback

with open('protocolo_peru_fibra.html', encoding='utf-8') as f:
    html = f.read()

js = re.findall(r'<script>(.*?)</script>', html, re.DOTALL)[-1]

# Extremely naive conversion from ES6 to ES5 to bypass pyjsparser's ES6 limitations
# Convert arrow functions
js = re.sub(r'\(\s*([\w\s,]*?)\s*\)\s*=>\s*\{', r'function(\1) {', js)
js = re.sub(r'(\w+)\s*=>\s*\{', r'function(\1) {', js)
js = re.sub(r'\(\s*([\w\s,]*?)\s*\)\s*=>\s*([^{][^;]*);', r'function(\1) { return \2; };', js)
js = re.sub(r'(\w+)\s*=>\s*([^{][^;]*);', r'function(\1) { return \2; };', js)
js = re.sub(r'\(\s*([\w\s,]*?)\s*\)\s*=>\s*([^{][^\n]*)\n', r'function(\1) { return \2; }\n', js)
js = re.sub(r'(\w+)\s*=>\s*([^{][^\n]*)\n', r'function(\1) { return \2; }\n', js)

# Convert const/let to var
js = re.sub(r'\bconst\b', 'var', js)
js = re.sub(r'\blet\b', 'var', js)

# Template literals (very hard to convert accurately, but let's just make them strings)
# We can just replace backticks with quotes if there are no ${}, but there are ${}.
# Let's just leave template literals and see if pyjsparser handles them? Pyjsparser DOES NOT support template literals.
# Oh, pyjsparser doesn't support template literals!

# Better idea: Let's write a python script that launches Chrome with a custom error-reporting extension!
