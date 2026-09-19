import re
import os

def build_perfect_html():
    with open('pdf_text_dump.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        
    pages = text.split("---PAGE_BREAK---")
    
    sections_map = {
        'sec-1': {'title': 'NUESTROS LINEAMIENTOS', 'nav_short': 'LINEAMIENTOS', 'content': []},
    }
    
    current_section = 'sec-1'
    
    for page in pages:
        lines = [line.strip() for line in page.split('\n') if line.strip()]
        if not lines: continue
        
        header_text = " ".join(lines[:10]).upper()
        
        matched_sec = None
        if "LINEAMIENTOS" in header_text:
            matched_sec = 'sec-1'
            
        if matched_sec:
            current_section = matched_sec
            
        if current_section == 'sec-1':
            sections_map['sec-1']['content'].extend(lines)

    lines = sections_map['sec-1']['content']
    clean_lines = []
    for line in lines:
        if line in ["VOZ", "FORMAL", "INFORMAL", "QUÉ DIGO", "QUÉ NO DIGO", "DEFINICIÓN"]:
            continue
        clean_lines.append(line)
        
    components_html = ""
    
    in_accordion = False
    curr_mode = "normal"
    curr_block = []
    
    def flush_block():
        nonlocal components_html, curr_block, curr_mode
        if not curr_block: return
        text = " ".join(curr_block)
        if curr_mode == "digo":
            components_html += f'<div class="box-digo"><div class="box-header">LO QUE DIGO</div><div class="box-body">{text}</div></div>'
        elif curr_mode == "hago":
            components_html += f'<div class="box-hago"><div class="box-header">LO QUE HAGO</div><div class="box-body">{text}</div></div>'
        else:
            components_html += f'<div class="info-card"><p>{text}</p></div>\n'
        curr_block = []
        curr_mode = "normal"
        
    def close_accordion():
        nonlocal in_accordion, components_html
        flush_block()
        if in_accordion:
            components_html += '</div></div>\n'
            in_accordion = False

    for line in clean_lines:
        upper_match = re.match(r'^([A-ZÁÉÍÓÚÑ0-9\-\.\, ]+)$', line)
        if (upper_match and len(line) < 60) or " - Opción" in line or "Pág" in line:
            close_accordion()
            components_html += f'''
            <div class="accordion-item open">
                <button class="accordion-header" onclick="toggleAccordion(this)">
                    {line}
                    <i class="fas fa-minus"></i>
                </button>
                <div class="accordion-content">
            '''
            in_accordion = True
        elif line.startswith("LO QUE DIGO") or line.startswith("QUÉ DIGO"):
            flush_block()
            curr_mode = "digo"
            if len(line) > 12: curr_block.append(line[12:])
        elif line.startswith("LO QUE HAGO") or line.startswith("QUÉ HAGO"):
            flush_block()
            curr_mode = "hago"
            if len(line) > 12: curr_block.append(line[12:])
        else:
            curr_block.append(line)
            if len(curr_block) >= 4 or line.endswith('.'):
                if curr_mode == "normal":
                    flush_block()

    close_accordion()
    print("COMPONENTS HTML FOR SEC-1:")
    print(components_html)

if __name__ == "__main__":
    build_perfect_html()
