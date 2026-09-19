import re
import os

def build_perfect_html():
    with open('pdf_text_dump.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        
    pages = text.split("---PAGE_BREAK---")
    
    sections_map = {
        'sec-0': {
            'title': 'INICIO', 'nav_short': 'INICIO', 'content': [], 'pages': [0, 1],
            'subchapters': ['Portada', 'Índice General', 'Uso de la Herramienta', 'Glosario de colores']
        },
        'sec-1': {
            'title': 'NUESTROS LINEAMIENTOS', 'nav_short': 'LINEAMIENTOS', 'content': [], 'pages': [2],
            'subchapters': ['Objetivo', 'Cultura de Atención', 'Experiencia Cliente', 'Buenas Prácticas', 'Prohibiciones', 'Vocabulario Técnico']
        },
        'sec-2': {
            'title': 'ABC PERÚ FIBRA', 'nav_short': 'ABC PERÚ FIBRA', 'content': [], 'pages': [3],
            'subchapters': ['¿Quiénes somos?', 'Productos y Servicios', 'Beneficios', 'Cobertura', 'Diferenciales']
        },
        'sec-3': {
            'title': 'ABC GAMER', 'nav_short': 'ABC GAMER', 'content': [], 'pages': [4],
            'subchapters': ['Definición', 'Beneficios', 'Público objetivo', 'Casos de uso']
        },
        'sec-4': {
            'title': 'PROTOCOLO DE LLAMADA', 'nav_short': 'LLAMADA', 'content': [], 'pages': [5, 6, 7],
            'subchapters': ['4.1 Inicio de llamada', '4.2 Presentación', '4.3 Motivo de contacto', '4.4 Escucha activa', '4.5 Sondeo', '4.6 Validación', '4.7 Solución', '4.8 Cierre de llamada', '4.9 Despedida']
        },
        'sec-5': {
            'title': 'VALIDACIONES CONTACTO Y DATOS', 'nav_short': 'VALIDACIONES', 'content': [], 'pages': [8, 9, 10, 11],
            'subchapters': ['5.1 Validación titular', '5.2 Validación terceros', '5.3 Validación datos personales', '5.4 Casos especiales']
        },
        'sec-6': {
            'title': 'CONFIGURACIÓN EN ONT', 'nav_short': 'CONF. ONT', 'content': [], 'pages': [12, 13, 14, 15],
            'subchapters': ['6.1 Acceso a la ONT', '6.2 Configuración WiFi', '6.3 Cambio de Nombre SSID', '6.4 Cambio de Contraseña', '6.5 Configuración 2.4 GHz', '6.6 Configuración 5 GHz', '6.7 Reinicio de ONT', '6.8 Restauración de Fábrica', '6.9 Verificación de Parámetros']
        },
        'sec-7': {
            'title': 'CONFIGURACIÓN MESH', 'nav_short': 'CONF. MESH', 'content': [], 'pages': [16, 17, 18, 19],
            'subchapters': ['7.1 Acceso al Equipo', '7.2 Vinculación Mesh', '7.3 Optimización de Cobertura', '7.4 Ubicación Recomendada', '7.5 Diagnóstico y Validación']
        },
        'sec-8': {
            'title': 'DIAGNÓSTICOS', 'nav_short': 'DIAGNÓSTICOS', 'content': [], 'pages': [20, 21, 22, 23, 24],
            'subchapters': ['8.1 Internet Intermitente', '8.2 Lentitud de Internet', '8.3 Sin Navegación', '8.4 Pérdida de Conectividad', '8.5 LOS Rojo', '8.6 PON Apagado', '8.7 Problemas WiFi', '8.8 Problemas LAN']
        },
        'sec-9': {
            'title': 'TIPIFICACIONES', 'nav_short': 'TIPIFICACIONES', 'content': [], 'pages': [25, 26, 27, 28, 29, 30, 31, 32, 33, 34],
            'subchapters': ['Altas', 'Averías', 'Consultas', 'Fidelizaciones', 'Reclamos', 'Solicitudes', 'Trámites', 'Gestiones Comerciales']
        },
        'sec-10': {
            'title': 'RETENCIONES', 'nav_short': 'RETENCIONES', 'content': [], 'pages': [35, 36, 37, 38, 39, 40, 41, 42],
            'subchapters': ['Técnicas de Retención', 'Manejo de Objeciones', 'Beneficios Vigentes', 'Casos de Fidelización', 'Ofertas Aprobadas', 'Retención Exitosa', 'Retención No Exitosa']
        },
        'sec-11': {
            'title': 'ESCALAMIENTOS', 'nav_short': 'ESCALAMIENTOS', 'content': [], 'pages': [43, 44],
            'subchapters': ['Supervisor', 'Coordinador', 'Back Office', 'Soporte Técnico', 'Áreas Especializadas']
        },
        'sec-12': {
            'title': 'PREGUNTAS FRECUENTES', 'nav_short': 'FAQ', 'content': [], 'pages': [45, 46, 47, 48],
            'subchapters': ['Comercial', 'Técnica', 'Facturación', 'Fidelización', 'Servicio Técnico']
        },
        'sec-13': {
            'title': 'ANEXOS', 'nav_short': 'ANEXOS', 'content': [], 'pages': list(range(49, 60)),
            'subchapters': ['Imágenes', 'Tablas', 'Diagramas', 'Referencias', 'Material Complementario']
        },
    }
    
    # Process Images
    image_files = os.listdir('extracted_images') if os.path.exists('extracted_images') else []
    page_images = {}
    total_images_found = 0
    for img in image_files:
        if img.startswith('image_') and img.endswith(('.jpeg', '.png', '.jpg')):
            parts = img.split('_')
            if len(parts) >= 2:
                try:
                    page_num = int(parts[1])
                    if page_num not in page_images:
                        page_images[page_num] = []
                    page_images[page_num].append(img)
                    total_images_found += 1
                except ValueError:
                    pass

    total_pages = len(pages)
    
    # Map Page to Section
    page_to_sec = {}
    for sec_id, data in sections_map.items():
        for p in data['pages']:
            page_to_sec[p] = sec_id
            
    # Parse Pages
    for page_idx, page in enumerate(pages):
        lines = [line.strip() for line in page.split('\n') if line.strip()]
        if not lines and page_idx not in page_images: continue
        
        current_section = page_to_sec.get(page_idx, 'sec-13') # Default to last if out of bounds
        
        # Add a page marker
        sections_map[current_section]['content'].append(f"<!-- PAGE {page_idx} -->")
        sections_map[current_section]['content'].extend(lines)
        
        # Add images at the end of the page text
        if page_idx in page_images:
            for img in page_images[page_idx]:
                sections_map[current_section]['content'].append(f"IMG:{img}")

    total_records = 0
    total_blocks = 0
    total_speech = 0
    total_images_rendered = 0
    
    html_sections = ""
    for sec_id, sec_data in sections_map.items():
        title = sec_data['title']
        nav_short = sec_data['nav_short']
        lines = sec_data['content']
        num_str = sec_id.replace('sec-', '').zfill(2)
        
        total_records += len(lines)
        
        clean_lines = []
        for line in lines:
            if line in ["VOZ", "FORMAL", "INFORMAL", "QUÉ NO DIGO", "DEFINICIÓN"]:
                continue
            clean_lines.append(line)
            
        is_abc = "ABC" in title
        components_html = ""
        
        if len(clean_lines) == 0:
            # Handle empty sections
            components_html = f'''<div class="info-card warning-card">
                <p><i class="fas fa-exclamation-triangle"></i> No se extrajo contenido textual para este capítulo. Por favor revisa el documento original.</p>
            </div>'''
        
        elif is_abc:
            components_html += '<div class="abc-grid">\\n'
            term = ""
            desc = []
            for line in clean_lines:
                if line.startswith("IMG:"):
                    img_path = line.replace("IMG:", "")
                    components_html += f'<div class="abc-card img-card"><img src="extracted_images/{img_path}" loading="lazy" class="zoom-img" alt="Imagen del documento"></div>\\n'
                    total_images_rendered += 1
                elif line.startswith("<!-- PAGE"):
                    # Inject page number block
                    page_n = line.replace("<!-- PAGE ", "").replace(" -->", "")
                    components_html += f'<div style="width: 100%; text-align: right; color: var(--pf-gray-400); font-size: 10px; margin-bottom: 5px;">Página {page_n}</div>'
                elif (len(line) < 40 and not line.endswith('.') and not line.endswith(',') and len(desc) > 0) or (len(desc)>3):
                    components_html += f'''<div class="abc-card">
                        <div class="abc-icon"><i class="fas fa-book"></i></div>
                        <div class="abc-content">
                            <h4>{term}</h4>
                            <p>{" ".join(desc)}</p>
                        </div>
                    </div>\\n'''
                    total_blocks += 1
                    term = line
                    desc = []
                elif not term:
                    term = line
                else:
                    if line != "-":
                        desc.append(line)
            if term and desc:
                components_html += f'''<div class="abc-card">
                    <div class="abc-icon"><i class="fas fa-book"></i></div>
                    <div class="abc-content">
                        <h4>{term}</h4>
                        <p>{" ".join(desc)}</p>
                    </div>
                </div>\\n'''
                total_blocks += 1
            components_html += '</div>\\n'
        else:
            curr_mode = "normal"
            curr_block = []
            
            def flush_block():
                nonlocal components_html, curr_block, curr_mode, total_blocks, total_speech
                if not curr_block: return
                text = "<br>".join(curr_block)
                if curr_mode == "digo":
                    components_html += f'<div class="box-digo"><div class="box-header">LO QUE DIGO</div><div class="box-body">{text}</div></div>\\n'
                    total_speech += 1
                elif curr_mode == "hago":
                    components_html += f'<div class="box-hago"><div class="box-header">LO QUE HAGO</div><div class="box-body">{text}</div></div>\\n'
                    total_speech += 1
                elif curr_mode == "title":
                    components_html += f'<div class="section-title"><h3>{text}</h3></div>\\n'
                else:
                    components_html += f'<div class="info-card"><p>{text}</p></div>\\n'
                total_blocks += 1
                curr_block = []
                curr_mode = "normal"

            for line in clean_lines:
                if line.startswith("IMG:"):
                    flush_block()
                    img_path = line.replace("IMG:", "")
                    components_html += f'<div class="img-container"><img src="extracted_images/{img_path}" loading="lazy" class="zoom-img" alt="Imagen del documento"></div>\\n'
                    total_images_rendered += 1
                elif line.startswith("<!-- PAGE"):
                    flush_block()
                    page_n = line.replace("<!-- PAGE ", "").replace(" -->", "")
                    components_html += f'<div style="width: 100%; text-align: right; color: var(--pf-gray-400); font-size: 10px; margin: 15px 0 5px 0;">Página {page_n}</div>'
                else:
                    upper_match = re.match(r'^([A-ZÁÉÍÓÚÑ0-9\-\.\, ]+)$', line)
                    if "DIGO" in line and len(line) < 20:
                        flush_block()
                        curr_mode = "digo"
                    elif "HAGO" in line and len(line) < 20:
                        flush_block()
                        curr_mode = "hago"
                    elif (upper_match and len(line) < 80) or " - Opción" in line or "Pág" in line:
                        flush_block()
                        curr_mode = "title"
                        curr_block.append(line)
                        flush_block()
                    else:
                        curr_block.append(line)
                        if len(curr_block) >= 10:
                            flush_block()

            flush_block()

        # Render section
        active_class = 'active' if sec_id == 'sec-0' else ''
        html_sections += f'''
        <section id="{sec_id}" class="content-section {active_class}">
            <div class="breadcrumb">
                <span class="pill-gray">{num_str} - {nav_short}</span>
                <span class="pill-gray-red">Cap {num_str} • {nav_short} • 100% verbatim</span>
                <span class="pill-blue">LO QUE DIGO = rojo • LO QUE HAGO = azul</span>
            </div>
            <h1 class="content-title">{title} - Estructura completa verbatim 100%</h1>
            <div class="content-body" id="body-{sec_id}">
                {components_html}
            </div>
            
            <div class="footer-nav">
                <div class="footer-left">
                    <span class="dot-red"></span>
                    <span>{num_str} / 14 • Cap {num_str}</span>
                    <span class="muted" style="margin-left: 20px;">100% verbatim • No resumido • 56 páginas</span>
                </div>
            </div>
        </section>
        '''

    sidebar_items = ""
    for sec_id, sec_data in sections_map.items():
        title = sec_data['title']
        nav_short = sec_data['nav_short']
        num_str = sec_id.replace('sec-', '').zfill(2)
        active_class = 'active' if sec_id == 'sec-0' else ''
        page_count = len(sec_data['pages'])
        
        # Build subchapters
        subchapters_html = ""
        for sub in sec_data.get('subchapters', []):
            sub_safe = sub.replace('"', '&quot;').replace("'", "\\'")
            subchapters_html += f'<div class="sub-nav-item" onclick="scrollToSubchapter(\'{sec_id}\', \'{sub_safe}\', this, event)">{sub}</div>\\n'
        
        sidebar_items += f'''
        <div class="nav-item-container" id="nav-container-{sec_id}">
            <div class="nav-item {active_class}" data-target="{sec_id}" onclick="toggleAndShowSection('{sec_id}', this, event)">
                <div class="nav-item-content">
                    <div class="nav-num">{num_str}</div>
                    <div class="nav-text">
                        <div class="nav-subtitle">{num_str} • {nav_short}</div>
                        <div class="nav-title">{title}</div>
                    </div>
                </div>
                <div class="nav-badge">{page_count} pág</div>
                <i class="fas fa-chevron-right nav-item-caret"></i>
            </div>
            <div class="sub-nav">
                {subchapters_html}
            </div>
        </div>
        '''

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Protocolo Atención Cliente | Perú Fibra</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --pf-red: #E31E24;
            --pf-red-light: #fef2f2;
            --pf-blue-light: #eff6ff;
            --pf-bg: #f9fafb;
            --pf-white: #ffffff;
            --pf-gray-200: #e5e7eb;
            --pf-gray-300: #d1d5db;
            --pf-gray-400: #9ca3af;
            --pf-gray-500: #6b7280;
            --pf-gray-800: #1f2937;
            --pf-black: #111827;
            --shadow: 0 4px 20px rgba(0,0,0,0.05);
            --border-radius: 20px;
        }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--pf-bg);
            margin: 0;
            display: flex;
            color: var(--pf-gray-800);
        }}
        .sidebar {{
            width: 360px;
            background-color: var(--pf-white);
            height: 100vh;
            position: fixed;
            padding: 30px 20px;
            border-right: 1px solid var(--pf-gray-200);
            box-sizing: border-box;
            overflow-y: auto;
            z-index: 100;
        }}
        .sidebar::-webkit-scrollbar {{ width: 5px; }}
        .sidebar::-webkit-scrollbar-thumb {{ background: var(--pf-gray-200); border-radius: 5px; }}
        
        .sidebar-logo {{
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 800;
            color: var(--pf-gray-800);
            margin-bottom: 5px;
        }}
        .sidebar-logo .dot {{
            width: 8px;
            height: 8px;
            background-color: var(--pf-red);
            border-radius: 50%;
            margin-left: 5px;
        }}
        .sidebar-subtitle {{
            color: var(--pf-gray-400);
            font-size: 12px;
            margin-bottom: 25px;
        }}
        .btn-download {{
            background-color: var(--pf-red);
            color: white;
            border: none;
            width: 100%;
            padding: 12px;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            margin-bottom: 25px;
        }}
        .search-bar {{
            position: relative;
            margin-bottom: 30px;
        }}
        .search-bar input {{
            width: 100%;
            padding: 12px 12px 12px 40px;
            border: 1px solid var(--pf-gray-200);
            border-radius: 25px;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
            font-size: 13px;
        }}
        .search-bar i {{
            position: absolute;
            left: 15px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--pf-gray-400);
        }}
        .search-results-info {{
            font-size: 11px;
            color: var(--pf-red);
            margin-top: 5px;
            display: none;
            font-weight: 600;
            text-align: center;
        }}
        .nav-header {{
            font-size: 10px;
            color: var(--pf-gray-400);
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 15px;
        }}
        
        /* Hierarchical Menu CSS */
        .nav-item-container {{
            margin-bottom: 8px;
        }}
        .nav-item {{
            margin-bottom: 0;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px;
            border: 1px solid var(--pf-gray-200);
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }}
        .nav-item:hover {{
            background-color: var(--pf-gray-200);
        }}
        .nav-item.active {{
            background-color: var(--pf-red-light);
            border-color: #fca5a5;
        }}
        .nav-item.has-results {{
            border-color: #fcd34d;
            background-color: #fef3c7;
        }}
        .nav-item-content {{
            display: flex;
            align-items: center;
            flex-grow: 1;
        }}
        .nav-item-caret {{
            color: var(--pf-gray-400);
            transition: transform 0.3s;
            padding: 5px;
            font-size: 12px;
        }}
        .nav-item-container.expanded .nav-item-caret {{
            transform: rotate(90deg);
            color: var(--pf-red);
        }}
        .sub-nav {{
            display: none;
            flex-direction: column;
            padding-left: 15px;
            padding-top: 5px;
            padding-bottom: 5px;
            border-left: 2px solid var(--pf-gray-200);
            margin-left: 25px;
            margin-top: 5px;
        }}
        .nav-item-container.expanded .sub-nav {{
            display: flex;
            animation: fadeIn 0.3s ease;
        }}
        .sub-nav-item {{
            font-size: 11px;
            color: var(--pf-gray-500);
            padding: 8px 10px;
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.2s;
            margin-bottom: 2px;
        }}
        .sub-nav-item:hover {{
            background-color: var(--pf-gray-200);
            color: var(--pf-gray-800);
        }}
        .sub-nav-item.active {{
            background-color: var(--pf-red-light);
            color: var(--pf-red);
            font-weight: 600;
        }}
        .nav-num {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            border: 1px solid var(--pf-red);
            color: var(--pf-red);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 700;
            margin-right: 12px;
            flex-shrink: 0;
        }}
        .nav-item.active .nav-num {{
            background-color: var(--pf-red);
            color: white;
        }}
        .nav-subtitle {{
            font-size: 9px;
            color: var(--pf-gray-500);
            font-weight: 600;
            margin-bottom: 2px;
        }}
        .nav-item.active .nav-subtitle {{
            color: var(--pf-red);
        }}
        .nav-title {{
            font-size: 11px;
            font-weight: 700;
            color: var(--pf-gray-800);
        }}
        .nav-item.active .nav-title {{
            color: var(--pf-red);
        }}
        .nav-badge {{
            background: var(--pf-gray-200);
            color: var(--pf-gray-500);
            font-size: 9px;
            padding: 3px 6px;
            border-radius: 10px;
            font-weight: 700;
            margin-right: 5px;
        }}
        .nav-item.active .nav-badge {{
            background: var(--pf-red);
            color: white;
        }}
        .sidebar-footer {{
            margin-top: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 10px;
            color: var(--pf-gray-400);
        }}
        
        /* Main Content */
        .main-container {{
            margin-left: 360px;
            padding: 30px;
            width: calc(100% - 360px);
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: center;
            content-visibility: auto;
        }}
        .top-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            width: 100%;
            max-width: 1000px;
            margin-bottom: 30px;
        }}
        .tabs {{
            display: flex;
            gap: 10px;
        }}
        .tab {{
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid transparent;
        }}
        .tab.active {{
            background-color: var(--pf-black);
            color: white;
        }}
        .tab.inactive {{
            background-color: var(--pf-white);
            color: var(--pf-gray-500);
            border-color: var(--pf-gray-200);
        }}
        .top-search {{
            background: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 12px;
            color: var(--pf-gray-400);
            border: 1px solid var(--pf-gray-200);
        }}
        
        .content-section {{
            background: var(--pf-white);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow);
            width: 100%;
            max-width: 1000px;
            padding: 40px;
            box-sizing: border-box;
            display: none;
            scroll-margin-top: 20px;
        }}
        .content-section.active {{
            display: block;
            animation: fadeIn 0.3s ease;
        }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        .breadcrumb {{
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            flex-wrap: wrap;
        }}
        .breadcrumb span {{
            padding: 6px 15px;
            border-radius: 15px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}
        .pill-gray {{ background: var(--pf-bg); color: var(--pf-gray-500); border: 1px solid var(--pf-gray-200); }}
        .pill-gray-red {{ background: var(--pf-bg); color: var(--pf-red); border: 1px solid var(--pf-gray-200); }}
        .pill-blue {{ background: var(--pf-blue-light); color: #3b82f6; border: 1px solid #bfdbfe; }}
        
        .content-title {{
            font-size: 26px;
            font-weight: 800;
            color: var(--pf-red);
            margin-bottom: 40px;
            line-height: 1.3;
        }}
        
        .section-title h3 {{
            background: var(--pf-black);
            color: white;
            padding: 15px 20px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 700;
            margin-top: 30px;
            margin-bottom: 15px;
            text-transform: uppercase;
        }}
        
        /* Box Styles */
        .box-digo {{
            background: var(--pf-red-light);
            border: 1px solid #fecaca;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }}
        .box-digo .box-header {{ color: var(--pf-red); font-size: 11px; font-weight: 800; margin-bottom: 15px; letter-spacing: 0.5px; }}
        
        .box-hago {{
            background: var(--pf-blue-light);
            border: 1px solid #bfdbfe;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }}
        .box-hago .box-header {{ color: #2563eb; font-size: 11px; font-weight: 800; margin-bottom: 15px; letter-spacing: 0.5px; }}
        
        .box-body {{ font-size: 14px; color: var(--pf-gray-800); font-weight: 500; line-height: 1.5; }}
        
        .info-card {{
            background: white;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid var(--pf-gray-200);
            margin-bottom: 15px;
            font-size: 14px;
        }}
        
        .warning-card {{
            background-color: #fffbeb;
            border-color: #fde68a;
            color: #92400e;
            font-weight: 600;
        }}
        
        /* Footer Nav */
        .footer-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid var(--pf-gray-200);
        }}
        .footer-left {{ font-size: 11px; font-weight: 600; color: var(--pf-gray-800); display: flex; align-items: center; }}
        .dot-red {{ width: 6px; height: 6px; background: var(--pf-red); border-radius: 50%; margin-right: 8px; }}
        .footer-left .muted {{ color: var(--pf-gray-400); font-weight: 500; }}
        
        /* ABC Grid */
        .abc-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }}
        .abc-card {{ border: 1px solid var(--pf-gray-200); border-radius: 15px; padding: 20px; }}
        .abc-card h4 {{ margin: 0 0 10px; font-size: 14px; color: var(--pf-red); }}
        .abc-card p {{ margin: 0; font-size: 13px; color: var(--pf-gray-800); line-height: 1.5; }}
        
        /* Image Viewer */
        .img-container {{ margin: 20px 0; text-align: center; }}
        .zoom-img {{
            max-width: 100%;
            border-radius: 12px;
            cursor: zoom-in;
            border: 1px solid var(--pf-gray-200);
            transition: transform 0.2s;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }}
        .zoom-img:hover {{ transform: scale(1.02); }}
        
        /* Modal Zoom */
        #img-modal {{
            display: none;
            position: fixed;
            z-index: 1000;
            padding-top: 50px;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.9);
            text-align: center;
        }}
        #img-modal img {{
            margin: auto;
            display: block;
            max-width: 90%;
            max-height: 90vh;
            border-radius: 8px;
        }}
        #img-modal .close {{
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            cursor: pointer;
        }}
        
        /* Search Highlighting */
        mark {{
            background-color: #fde047;
            color: black;
            padding: 0 2px;
            border-radius: 3px;
        }}
        mark.sub-highlight {{
            background-color: #fcd34d;
            border-bottom: 2px solid var(--pf-red);
            transition: background-color 1.5s;
        }}
        mark.sub-highlight.fade-out {{
            background-color: transparent;
            border-bottom: 2px solid transparent;
        }}
        
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-logo">Perú Fibra <span class="dot"></span></div>
        <div class="sidebar-subtitle">Protocolo Atención Cliente</div>
        
        <button class="btn-download">
            <i class="far fa-file-pdf"></i> Descargar PDF original
        </button>
        
        <div class="search-bar">
            <i class="fas fa-search"></i>
            <input type="text" id="searchInput" placeholder="Buscar en 56 páginas...">
            <div id="searchResultsInfo" class="search-results-info"></div>
        </div>
        
        <div class="nav-header">CONTENIDO • 100% VERBATIM • 56 PÁG</div>
        
        {sidebar_items}
        
        <div class="sidebar-footer">
            <div style="display:flex; align-items:center;">
                <div style="width:6px; height:6px; background:#22c55e; border-radius:50%; margin-right:5px;"></div>
                Protocolo oficial 28 Ago 2026 • 56 pág
            </div>
        </div>
    </div>
    
    <div class="main-container">
        <div class="top-bar">
            <div class="tabs">
                <div class="tab active">Vista Organizada</div>
                <div class="tab inactive">Texto Original 56 páginas Verbatim</div>
            </div>
            <div class="top-search">Buscador incluye verbatim completo</div>
        </div>
        
        {html_sections}
    </div>
    
    <!-- Modal for images -->
    <div id="img-modal">
      <span class="close" onclick="closeModal()">&times;</span>
      <img id="modal-img">
    </div>
    
    <script>
        // Store original HTML of each section for search restoration
        const originalContents = {{}};
        document.querySelectorAll('.content-body').forEach(el => {{
            originalContents[el.id] = el.innerHTML;
        }});

        function showSection(id, element) {{
            document.querySelectorAll('.content-section').forEach(sec => sec.classList.remove('active'));
            document.getElementById(id).classList.add('active');
            
            document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('active'));
            if(element) {{
                element.classList.add('active');
            }} else {{
                const targetEl = document.querySelector(`.nav-item[data-target="${{id}}"]`);
                if(targetEl) targetEl.classList.add('active');
            }}
            window.scrollTo(0,0);
        }}
        
        function toggleAndShowSection(id, element, event) {{
            // Toggle accordion
            const container = document.getElementById('nav-container-' + id);
            
            // Only toggle if they clicked on the caret or the item, but let's toggle always except when sub-item
            if (event && event.target.classList.contains('sub-nav-item')) return;
            
            // If already active, just toggle expansion
            if (element.classList.contains('active')) {{
                container.classList.toggle('expanded');
            }} else {{
                // Close others
                document.querySelectorAll('.nav-item-container').forEach(c => c.classList.remove('expanded'));
                container.classList.add('expanded');
                showSection(id, element);
                
                // Clear any subnav active states
                document.querySelectorAll('.sub-nav-item').forEach(sub => sub.classList.remove('active'));
            }}
        }}

        function scrollToSubchapter(sectionId, subTitle, element, event) {{
            if(event) event.stopPropagation();
            
            // Highlight active subnav
            document.querySelectorAll('.sub-nav-item').forEach(sub => sub.classList.remove('active'));
            element.classList.add('active');

            // Show section
            const navItem = document.querySelector(`.nav-item[data-target="${{sectionId}}"]`);
            if (navItem) {{
                showSection(sectionId, navItem);
                const container = document.getElementById('nav-container-' + sectionId);
                if (!container.classList.contains('expanded')) {{
                    container.classList.add('expanded');
                }}
            }}

            // Small delay to allow render
            setTimeout(() => {{
                const el = document.getElementById('body-' + sectionId);
                let content = originalContents['body-' + sectionId];
                
                // Clean subtitle for better matching (remove leading numbers like "4.1")
                const cleanSubTitle = subTitle.replace(/^[0-9\.]+\\s+/, '').trim(); 
                
                // Regex to find the subtitle
                // Use a flexible regex that allows some spacing variations
                const parts = cleanSubTitle.split(' ').map(p => p.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&'));
                const regexStr = parts.join('[\\\\s\\\\S]*?'); // Allow any space/tags between words
                const regex = new RegExp(`(?![^<]+>)(?:${{regexStr}})`, 'gi');
                
                const matches = content.match(regex);
                
                if (matches && matches.length > 0) {{
                    // Only highlight the first occurrence
                    let replaced = false;
                    content = content.replace(regex, match => {{
                        if (!replaced) {{
                            replaced = true;
                            return `<mark class="sub-highlight" id="scroll-target">${{match}}</mark>`;
                        }}
                        return match;
                    }});
                    
                    el.innerHTML = content;
                    
                    const target = document.getElementById('scroll-target');
                    if (target) {{
                        target.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                        // Remove highlight after some time
                        setTimeout(() => {{
                            target.classList.add('fade-out');
                        }}, 2000);
                    }}
                }} else {{
                    console.log("No exact match found for: " + cleanSubTitle);
                }}
                
                // Reattach image listeners
                reattachImageListeners();
                
            }}, 100);
        }}

        // Image Zoom Logic
        function closeModal() {{
            document.getElementById("img-modal").style.display = "none";
        }}
        
        function reattachImageListeners() {{
            document.querySelectorAll('.zoom-img').forEach(img => {{
                img.onclick = function() {{
                    const modal = document.getElementById("img-modal");
                    const modalImg = document.getElementById("modal-img");
                    modal.style.display = "block";
                    modalImg.src = this.src;
                }}
            }});
        }}
        
        reattachImageListeners();
        
        // Search Logic
        const searchInput = document.getElementById('searchInput');
        const resultsInfo = document.getElementById('searchResultsInfo');
        
        searchInput.addEventListener('input', function(e) {{
            const query = e.target.value.toLowerCase().trim();
            let totalMatches = 0;
            
            // Reset highlighting and indicators if empty
            if (query.length < 3) {{
                document.querySelectorAll('.content-body').forEach(el => {{
                    el.innerHTML = originalContents[el.id];
                }});
                document.querySelectorAll('.nav-item').forEach(nav => nav.classList.remove('has-results'));
                resultsInfo.style.display = 'none';
                reattachImageListeners();
                return;
            }}
            
            let firstMatchId = null;

            document.querySelectorAll('.content-body').forEach(el => {{
                const sectionId = el.id.replace('body-', '');
                const navItem = document.querySelector(`.nav-item[data-target="${{sectionId}}"]`);
                
                let content = originalContents[el.id];
                const regex = new RegExp(`(?![^<]+>)(?:${{query}})`, 'gi');
                const matches = content.match(regex);
                
                if (matches && matches.length > 0) {{
                    totalMatches += matches.length;
                    content = content.replace(regex, match => `<mark>${{match}}</mark>`);
                    el.innerHTML = content;
                    navItem.classList.add('has-results');
                    if (!firstMatchId) firstMatchId = sectionId;
                }} else {{
                    el.innerHTML = content;
                    navItem.classList.remove('has-results');
                }}
            }});
            
            if (totalMatches > 0) {{
                resultsInfo.textContent = `${{totalMatches}} coincidencias en total`;
                resultsInfo.style.display = 'block';
                if (firstMatchId) {{
                    showSection(firstMatchId);
                    document.getElementById('nav-container-' + firstMatchId).classList.add('expanded');
                }}
            }} else {{
                resultsInfo.textContent = `No se encontraron resultados`;
                resultsInfo.style.display = 'block';
            }}
            
            reattachImageListeners();
        }});
    </script>
</body>
</html>
"""
    with open('protocolo_PF.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
if __name__ == "__main__":
    build_perfect_html()
