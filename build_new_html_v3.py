import re
import os
import json

def generate_log(removed_items):
    log_content = "=== LOG DE DEDUPLICACIÓN ===\n\n"
    log_content += f"Total de elementos duplicados encontrados y eliminados: {len(removed_items)}\n\n"
    for idx, item in enumerate(removed_items):
        log_content += f"{idx + 1}. {item[:100]}...\n"
        
    with open('deduplication_log.txt', 'w', encoding='utf-8') as f:
        f.write(log_content)

def parse_and_rebuild():
    file_path = 'protocolo_PF.html'
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Extract sections
    sections = re.findall(r'<section id="sec-\d+".*?</section>', html, re.DOTALL)
    
    seen_speeches = set()
    seen_paragraphs = set()
    removed_items = []
    
    parsed_sections = []
    
    for sec in sections:
        sec_id_match = re.search(r'id="(sec-\d+)"', sec)
        sec_id = sec_id_match.group(1) if sec_id_match else ""
        
        title_match = re.search(r'<h1 class="content-title">(.*?)</h1>', sec)
        sec_title = title_match.group(1) if title_match else ""
        
        body_match = re.search(r'<div class="content-body">(.*?)</div>\s*</section>', sec, re.DOTALL)
        raw_body = body_match.group(1) if body_match else ""
        
        # Now we need to parse the raw body. It might have <p>, <ul>, <div class="speech-card">, <div class="timeline">
        # To make it easier and apply the new design, we can extract the plain text roughly and rebuild.
        # Let's clean the HTML tags to get raw blocks
        
        blocks = []
        
        # Split by <p>, <h3>, <div class="speech-card">, <li>
        # A simpler way is to extract text line by line and ignore HTML tags except those that structure it.
        # Let's remove all HTML tags and just get the text lines, since the previous script just wrapped text.
        text_only = re.sub(r'<.*?>', '\n', raw_body)
        lines = [line.strip() for line in text_only.split('\n') if line.strip()]
        
        # Group lines back into logical blocks
        current_block = []
        for line in lines:
            if line in ['Copiar', 'Speech', 'Introducción', sec_title]:
                continue
            if line.startswith('Paso ') or line.startswith('PASO '):
                if current_block:
                    blocks.append(" ".join(current_block))
                    current_block = []
                blocks.append(line)
            else:
                current_block.append(line)
        if current_block:
            blocks.append(" ".join(current_block))
            
        # Refined parsing logic based on the text
        new_components = []
        in_timeline = False
        timeline_items = []
        
        in_accordion = False
        
        # Determine if it's an ABC section
        is_abc = "ABC" in sec_title.upper()
        
        if is_abc:
            # Render as grid
            abc_grid = '<div class="abc-grid">\n'
            # In ABC, usually the format is Term - Definition or Term: Definition
            # Or consecutive lines: Term \n Definition
            
            for block in blocks:
                # Deduplication check
                if block in seen_paragraphs:
                    removed_items.append(block)
                    continue
                seen_paragraphs.add(block)
                
                # Try to split by : or -
                parts = re.split(r'[:\-]', block, 1)
                if len(parts) == 2 and len(parts[0]) < 50:
                    term = parts[0].strip()
                    desc = parts[1].strip()
                else:
                    term = "Término"
                    desc = block
                    
                abc_grid += f'''<div class="abc-card">
                    <div class="abc-icon"><i class="fas fa-book"></i></div>
                    <div class="abc-content">
                        <h4>{term}</h4>
                        <p>{desc}</p>
                    </div>
                </div>\n'''
            abc_grid += '</div>'
            new_components.append(abc_grid)
        else:
            # Regular parsing
            for block in blocks:
                # Deduplication check
                
                # Check for speech
                if block.startswith("Speech:") or block.startswith("Speech"):
                    speech_text = block.replace("Speech:", "").replace("Speech", "").strip()
                    if speech_text in seen_speeches:
                        removed_items.append(speech_text)
                        continue
                    seen_speeches.add(speech_text)
                    
                    if in_timeline:
                        # Append timeline first
                        tl_html = '<div class="timeline-container">\n'
                        for idx, item in enumerate(timeline_items):
                            tl_html += f'''<div class="timeline-step">
                                <div class="step-circle">{idx+1}</div>
                                <div class="step-content">
                                    <h4 class="step-title">{item['title']}</h4>
                                    <p class="step-desc">{item['desc']}</p>
                                </div>
                            </div>\n'''
                        tl_html += '</div>'
                        new_components.append(tl_html)
                        timeline_items = []
                        in_timeline = False
                        
                    new_components.append(f'''<div class="modern-speech-card">
                        <div class="speech-badge">[SPEECH OFICIAL]</div>
                        <div class="speech-content-wrap">
                            <i class="fas fa-headset speech-icon"></i>
                            <div class="speech-text">{speech_text}</div>
                        </div>
                        <div class="speech-actions">
                            <button class="btn-action" onclick="copyText(this, '{speech_text}')"><i class="fas fa-copy"></i> Copiar</button>
                            <button class="btn-action" onclick="toggleFav(this)"><i class="far fa-star"></i> Favorito</button>
                        </div>
                    </div>''')
                    
                elif re.match(r'^(Paso \d+|PASO \d+)', block, re.IGNORECASE):
                    in_timeline = True
                    step_match = re.match(r'^(Paso \d+|PASO \d+)[\s:-]*(.*)', block, re.IGNORECASE)
                    if step_match:
                        timeline_items.append({
                            'title': step_match.group(1).upper(),
                            'desc': step_match.group(2).strip()
                        })
                else:
                    # Regular text paragraph
                    if block in seen_paragraphs:
                        removed_items.append(block)
                        continue
                    seen_paragraphs.add(block)
                    
                    if in_timeline:
                        # Append timeline first
                        tl_html = '<div class="timeline-container">\n'
                        for idx, item in enumerate(timeline_items):
                            tl_html += f'''<div class="timeline-step">
                                <div class="step-circle">{idx+1}</div>
                                <div class="step-content">
                                    <h4 class="step-title">{item['title']}</h4>
                                    <p class="step-desc">{item['desc']}</p>
                                </div>
                            </div>\n'''
                        tl_html += '</div>'
                        new_components.append(tl_html)
                        timeline_items = []
                        in_timeline = False
                        
                    # Check if it's a section subtitle (Accordion trigger)
                    if re.match(r'^(\d+\.\d+|\d+\.)', block):
                        if in_accordion:
                            new_components.append('</div></div>') # Close previous accordion
                            
                        # Start new accordion
                        acc_id = "acc_" + str(hash(block))[-6:]
                        # Expand the first one by default if it's the first in the section
                        open_class = "open" if not in_accordion else ""
                        
                        new_components.append(f'''
                        <div class="accordion-item {open_class}">
                            <button class="accordion-header" onclick="toggleAccordion(this)">
                                <span><i class="fas fa-chevron-right"></i> {block}</span>
                            </button>
                            <div class="accordion-body">
                        ''')
                        in_accordion = True
                    else:
                        if not in_accordion and len(block) > 50:
                            # Wrap loose long paragraphs in a panel
                            new_components.append(f'<div class="info-panel"><p>{block}</p></div>')
                        elif len(block) > 0:
                            new_components.append(f'<p class="mb-4">{block}</p>')
                            
            if in_timeline:
                tl_html = '<div class="timeline-container">\n'
                for idx, item in enumerate(timeline_items):
                    tl_html += f'''<div class="timeline-step">
                        <div class="step-circle">{idx+1}</div>
                        <div class="step-content">
                            <h4 class="step-title">{item['title']}</h4>
                            <p class="step-desc">{item['desc']}</p>
                        </div>
                    </div>\n'''
                tl_html += '</div>'
                new_components.append(tl_html)
                
            if in_accordion:
                new_components.append('</div></div>')
                
        # Word count for estimated time
        word_count = len(" ".join(blocks).split())
        est_time = max(1, word_count // 200) # 200 WPM
        
        parsed_sections.append({
            'id': sec_id,
            'title': sec_title,
            'content': "\n".join(new_components),
            'time': est_time
        })
        
    generate_log(removed_items)
    
    # Generate new HTML structure
    new_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaaS Knowledge Base | Perú Fibra</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --pf-red: #E31E24;
            --pf-red-light: #fef2f2;
            --pf-bg: #f3f4f6;
            --pf-white: #ffffff;
            --pf-gray-50: #f9fafb;
            --pf-gray-200: #e5e7eb;
            --pf-gray-300: #d1d5db;
            --pf-gray-600: #4b5563;
            --pf-gray-800: #1f2937;
            --shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
            --radius: 16px;
            --radius-sm: 12px;
            --transition: all 0.3s ease;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--pf-bg);
            color: var(--pf-gray-800);
            margin: 0;
            padding: 0;
            display: flex;
        }

        /* SIDEBAR */
        .sidebar {
            width: 280px;
            background: var(--pf-white);
            height: 100vh;
            position: fixed;
            border-right: 1px solid var(--pf-gray-200);
            overflow-y: auto;
            padding: 20px 0;
            z-index: 100;
        }
        .sidebar-logo {
            padding: 0 20px 20px;
            font-size: 20px;
            font-weight: 800;
            color: var(--pf-red);
            border-bottom: 1px solid var(--pf-gray-200);
            margin-bottom: 20px;
        }
        .nav-category-title {
            padding: 0 20px;
            font-size: 12px;
            text-transform: uppercase;
            font-weight: 700;
            color: var(--pf-gray-600);
            margin: 20px 0 10px;
        }
        .nav-item {
            display: block;
            padding: 10px 20px 10px 30px;
            color: var(--pf-gray-800);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            border-left: 3px solid transparent;
            cursor: pointer;
            transition: var(--transition);
        }
        .nav-item:hover, .nav-item.active {
            background: var(--pf-gray-50);
            color: var(--pf-red);
            border-left-color: var(--pf-red);
        }

        /* MAIN CONTENT */
        .main-content {
            margin-left: 280px;
            width: calc(100% - 280px);
            min-height: 100vh;
            display: flex;
            justify-content: center;
        }
        .content-wrapper {
            max-width: 900px;
            width: 100%;
            padding: 40px;
        }
        .content-section {
            display: none;
            animation: fadeIn 0.4s ease;
        }
        .content-section.active { display: block; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

        /* ACTION BAR */
        .action-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid var(--pf-gray-200);
        }
        .reading-time { font-size: 13px; color: var(--pf-gray-600); font-weight: 500; }
        .action-btns button {
            background: var(--pf-white);
            border: 1px solid var(--pf-gray-200);
            padding: 6px 12px;
            border-radius: var(--radius-sm);
            font-size: 13px;
            cursor: pointer;
            margin-left: 10px;
            color: var(--pf-gray-800);
            font-weight: 500;
            box-shadow: var(--shadow-sm);
        }
        .action-btns button:hover { background: var(--pf-gray-50); }

        /* TYPOGRAPHY */
        .content-title {
            font-size: 32px;
            font-weight: 800;
            margin-bottom: 30px;
            color: var(--pf-gray-900);
        }
        .mb-4 { margin-bottom: 16px; line-height: 1.7; }

        /* INFO PANEL */
        .info-panel {
            background: var(--pf-white);
            padding: 20px;
            border-radius: var(--radius);
            box-shadow: var(--shadow-sm);
            margin-bottom: 20px;
            border: 1px solid var(--pf-gray-200);
        }

        /* ABC GRID */
        .abc-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .abc-card {
            background: var(--pf-white);
            padding: 24px;
            border-radius: var(--radius);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--pf-gray-200);
            transition: var(--transition);
        }
        .abc-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-lg);
        }
        .abc-icon {
            color: var(--pf-red);
            font-size: 24px;
            margin-bottom: 15px;
        }
        .abc-content h4 { margin: 0 0 10px; font-size: 16px; color: var(--pf-gray-900); }
        .abc-content p { margin: 0; font-size: 14px; color: var(--pf-gray-600); }

        /* SPEECH CARD */
        .modern-speech-card {
            background: var(--pf-gray-50);
            border-radius: var(--radius);
            border: 1px solid var(--pf-gray-200);
            border-left: 6px solid var(--pf-red);
            margin: 20px 0;
            box-shadow: var(--shadow-sm);
            position: relative;
            overflow: hidden;
        }
        .speech-badge {
            background: var(--pf-red);
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 0 0 8px 0;
            display: inline-block;
        }
        .speech-content-wrap {
            padding: 20px;
            display: flex;
            gap: 15px;
        }
        .speech-icon { font-size: 24px; color: var(--pf-red); margin-top: 5px; }
        .speech-text { font-size: 15px; font-style: italic; color: var(--pf-gray-800); flex: 1; }
        .speech-actions {
            display: flex;
            gap: 10px;
            padding: 10px 20px;
            background: var(--pf-white);
            border-top: 1px solid var(--pf-gray-200);
        }
        .btn-action {
            background: transparent;
            border: 1px solid var(--pf-gray-300);
            padding: 6px 12px;
            border-radius: var(--radius-sm);
            cursor: pointer;
            font-size: 13px;
            font-weight: 500;
            color: var(--pf-gray-800);
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .btn-action:hover { background: var(--pf-gray-100); }
        .btn-action.active { color: var(--pf-red); border-color: var(--pf-red); }

        /* TIMELINE */
        .timeline-container {
            margin: 30px 0;
            padding: 20px;
            background: var(--pf-white);
            border-radius: var(--radius);
            box-shadow: var(--shadow-sm);
        }
        .timeline-step {
            display: flex;
            gap: 20px;
            position: relative;
            margin-bottom: 20px;
        }
        .timeline-step:last-child { margin-bottom: 0; }
        .timeline-step::after {
            content: '';
            position: absolute;
            left: 17px;
            top: 40px;
            bottom: -20px;
            width: 2px;
            background: var(--pf-gray-200);
        }
        .timeline-step:last-child::after { display: none; }
        .step-circle {
            width: 36px;
            height: 36px;
            background: var(--pf-red);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            z-index: 1;
            flex-shrink: 0;
        }
        .step-content {
            background: var(--pf-gray-50);
            padding: 15px 20px;
            border-radius: var(--radius-sm);
            flex: 1;
            border: 1px solid var(--pf-gray-200);
        }
        .step-title { margin: 0 0 5px; font-size: 15px; color: var(--pf-gray-900); }
        .step-desc { margin: 0; font-size: 14px; color: var(--pf-gray-600); }

        /* ACCORDION */
        .accordion-item {
            background: var(--pf-white);
            border: 1px solid var(--pf-gray-200);
            border-radius: var(--radius-sm);
            margin-bottom: 10px;
            overflow: hidden;
        }
        .accordion-header {
            width: 100%;
            text-align: left;
            background: var(--pf-white);
            border: none;
            padding: 15px 20px;
            font-size: 15px;
            font-weight: 600;
            color: var(--pf-gray-900);
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .accordion-header span i {
            color: var(--pf-red);
            margin-right: 10px;
            transition: transform 0.3s ease;
        }
        .accordion-body {
            padding: 0 20px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease, padding 0.3s ease;
            background: var(--pf-gray-50);
        }
        .accordion-item.open .accordion-body {
            padding: 20px;
            max-height: 2000px; /* arbitrary large value */
        }
        .accordion-item.open .accordion-header span i {
            transform: rotate(90deg);
        }

        /* NAVIGATION CARDS */
        .nav-cards {
            display: flex;
            gap: 20px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--pf-gray-200);
        }
        .nav-card {
            flex: 1;
            background: var(--pf-white);
            padding: 20px;
            border-radius: var(--radius);
            box-shadow: var(--shadow-sm);
            text-decoration: none;
            color: var(--pf-gray-800);
            border: 1px solid var(--pf-gray-200);
            transition: var(--transition);
        }
        .nav-card:hover { border-color: var(--pf-red); box-shadow: var(--shadow-md); }
        .nav-card.prev { text-align: left; }
        .nav-card.next { text-align: right; }
        .nav-label { font-size: 12px; color: var(--pf-gray-600); text-transform: uppercase; font-weight: 700; margin-bottom: 5px; }
        .nav-title { font-size: 16px; font-weight: 600; color: var(--pf-red); }
        
        /* ALERTS */
        .page-alert {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 15px;
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            color: #1e3a8a;
            border-radius: var(--radius-sm);
            margin-bottom: 20px;
            font-size: 14px;
            font-weight: 500;
        }
    </style>
</head>
<body>
"""

    # Add Sidebar
    new_html += '''
    <nav class="sidebar">
        <div class="sidebar-logo">PERÚ FIBRA</div>
        <div class="nav-category">
            <div class="nav-category-title">Contenido</div>
'''
    for i, sec in enumerate(parsed_sections):
        if not sec['id']: continue
        cls = "active" if i == 0 else ""
        new_html += f'<a class="nav-item {cls}" onclick="showSection(\'{sec["id"]}\', this)">{sec["title"]}</a>\n'
        
    new_html += '''
        </div>
    </nav>
    <main class="main-content">
        <div class="content-wrapper">
'''

    # Add sections
    for i, sec in enumerate(parsed_sections):
        if not sec['id']: continue
        
        prev_sec = parsed_sections[i-1] if i > 0 else None
        next_sec = parsed_sections[i+1] if i < len(parsed_sections)-1 else None
        
        cls = "active" if i == 0 else ""
        new_html += f'''
        <section id="{sec['id']}" class="content-section {cls}">
            <div class="action-bar">
                <div class="reading-time"><i class="far fa-clock"></i> Tiempo estimado: {sec['time']} min</div>
                <div class="action-btns">
                    <button onclick="expandAll()"><i class="fas fa-expand-alt"></i> Expandir</button>
                    <button onclick="collapseAll()"><i class="fas fa-compress-alt"></i> Contraer</button>
                    <button onclick="window.print()"><i class="fas fa-print"></i> Imprimir</button>
                </div>
            </div>
            
            <h1 class="content-title">{sec['title']}</h1>
            
            {sec['content']}
            
            <div class="nav-cards">
'''
        if prev_sec:
            new_html += f'''
                <a href="#" class="nav-card prev" onclick="showSection('{prev_sec['id']}', document.querySelectorAll('.nav-item')[{i-1}]); return false;">
                    <div class="nav-label">Anterior</div>
                    <div class="nav-title"><i class="fas fa-arrow-left"></i> {prev_sec['title']}</div>
                </a>
'''
        else:
            new_html += '<div></div>' # Empty space filler
            
        if next_sec:
            new_html += f'''
                <a href="#" class="nav-card next" onclick="showSection('{next_sec['id']}', document.querySelectorAll('.nav-item')[{i+1}]); return false;">
                    <div class="nav-label">Siguiente</div>
                    <div class="nav-title">{next_sec['title']} <i class="fas fa-arrow-right"></i></div>
                </a>
'''
        new_html += '''
            </div>
        </section>
'''

    new_html += '''
        </div>
    </main>

    <script>
        function showSection(id, navEl) {
            document.querySelectorAll('.content-section').forEach(el => el.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            
            document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
            if(navEl) navEl.classList.add('active');
            
            window.scrollTo(0,0);
        }
        
        function toggleAccordion(btn) {
            const item = btn.parentElement;
            item.classList.toggle('open');
        }
        
        function expandAll() {
            const activeSec = document.querySelector('.content-section.active');
            activeSec.querySelectorAll('.accordion-item').forEach(acc => acc.classList.add('open'));
        }
        
        function collapseAll() {
            const activeSec = document.querySelector('.content-section.active');
            activeSec.querySelectorAll('.accordion-item').forEach(acc => acc.classList.remove('open'));
        }

        function copyText(btn, text) {
            navigator.clipboard.writeText(text).then(() => {
                const icon = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check"></i> Copiado';
                btn.style.color = '#10b981';
                setTimeout(() => {
                    btn.innerHTML = icon;
                    btn.style.color = '';
                }, 2000);
            });
        }
        
        function toggleFav(btn) {
            btn.classList.toggle('active');
            if(btn.classList.contains('active')) {
                btn.innerHTML = '<i class="fas fa-star"></i> Guardado';
            } else {
                btn.innerHTML = '<i class="far fa-star"></i> Favorito';
            }
        }
    </script>
</body>
</html>
'''

    with open('protocolo_PF_new_v3.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
    print("Redesign Phase 3 generated successfully in protocolo_PF_new_v3.html")

if __name__ == "__main__":
    parse_and_rebuild()
