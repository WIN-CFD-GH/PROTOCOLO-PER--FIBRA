import re

def dump_text():
    with open('protocolo_PF.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    text = re.sub(r'<[^>]+>', '\n', html)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    with open('all_text_dump.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

if __name__ == '__main__':
    dump_text()
