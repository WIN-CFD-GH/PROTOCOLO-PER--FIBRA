import re
def test():
    with open('pdf_text_dump.txt', 'r', encoding='utf-8') as f:
        pages = f.read().split("---PAGE_BREAK---")
        
    sections_map = {f'sec-{i}': [] for i in range(12)}
    current_section = 'sec-1'
    
    for page in pages:
        lines = [line.strip() for line in page.split('\n') if line.strip()]
        if not lines: continue
        
        if "ÍNDICE" in lines[:5]:
            sections_map['sec-0'].extend(lines)
            continue
            
        header_text = " ".join(lines[:10]).upper()
        
        matched_sec = None
        if "FORMATOS" in header_text or "CESIÓN DE POSICIÓN" in header_text:
            matched_sec = 'sec-11'
        elif "ESCALACIÓN SUPERVISOR" in header_text:
            matched_sec = 'sec-10'
        elif "FACTURACIÓN" in header_text:
            matched_sec = 'sec-9'
        elif "GESTIONES" in header_text or "ACTUALIZACIÓN DE DATOS" in header_text or "SOPORTE ATC" in header_text:
            matched_sec = 'sec-8'
        elif "PROTOCOLO DE BAJA" in header_text or "CONTINGENCIAS" in header_text:
            matched_sec = 'sec-7'
        elif "VALIDACIÓN Y SEGURIDAD" in header_text or "CLIENTE DIFÍCIL" in header_text:
            matched_sec = 'sec-6'
        elif "VALIDACIONES DE CONTACTO" in header_text:
            matched_sec = 'sec-5'
        elif "PROTOCOLO DE LLAMADA" in header_text:
            matched_sec = 'sec-4'
        elif "ABC GAMER" in header_text:
            matched_sec = 'sec-3'
        elif "ABC PERÚ FIBRA" in header_text:
            matched_sec = 'sec-2'
        elif "LINEAMIENTOS" in header_text:
            matched_sec = 'sec-1'
            
        if matched_sec:
            current_section = matched_sec
            
        sections_map[current_section].extend(lines)
        
    for k, v in sections_map.items():
        print(f"{k}: {len(v)} lines")

test()
