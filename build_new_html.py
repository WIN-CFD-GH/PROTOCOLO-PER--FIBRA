import re
import os
import json

def process_text_into_components(text):
    # This function will attempt to identify speeches, steps, and alerts to wrap them in modern HTML
    # Speeches often start with "Speech:", "Speech" or are in quotes.
    lines = text.split('\n')
    new_lines = []
    in_speech = False
    in_list = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        if stripped.startswith("Speech:") or stripped.startswith("Speech"):
            speech_content = stripped.replace("Speech:", "").replace("Speech", "").strip()
            if speech_content:
                new_lines.append(f'''<div class="speech-card">
    <div class="speech-header">
        <span class="speech-title"><i class="fas fa-comment-dots"></i> Speech</span>
        <button class="btn-copy" onclick="copyText(this)">Copiar</button>
    </div>
    <div class="speech-body">{speech_content}</div>
</div>''')
            else:
                in_speech = True
                new_lines.append('''<div class="speech-card">
    <div class="speech-header">
        <span class="speech-title"><i class="fas fa-comment-dots"></i> Speech</span>
        <button class="btn-copy" onclick="copyText(this)">Copiar</button>
    </div>
    <div class="speech-body">''')
        elif in_speech:
            if stripped == "":
                in_speech = False
                new_lines.append('</div></div>')
            else:
                new_lines.append(stripped)
        elif re.match(r'^(Paso \d+|PASO \d+)', stripped, re.IGNORECASE):
            # Attempt to convert to timeline step
            step_match = re.match(r'^(Paso \d+|PASO \d+)[\s:-]*(.*)', stripped, re.IGNORECASE)
            if step_match:
                step_title = step_match.group(1).upper()
                step_desc = step_match.group(2)
                new_lines.append(f'''<div class="timeline-item">
    <div class="timeline-marker"></div>
    <div class="timeline-content">
        <h4 class="timeline-title">{step_title}</h4>
        <p class="timeline-desc">{step_desc}</p>
    </div>
</div>''')
        elif re.match(r'^(\d+\.\d+|\d+\.)', stripped):
            new_lines.append(f'<h3 class="section-subtitle">{stripped}</h3>')
        elif stripped.startswith('-') or stripped.startswith('•'):
            if not in_list:
                new_lines.append('<ul class="modern-list">')
                in_list = True
            new_lines.append(f'<li>{stripped[1:].strip()}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(f'<p>{stripped}</p>')
            
    if in_speech:
        new_lines.append('</div></div>')
    if in_list:
        new_lines.append('</ul>')
        
    return "\n".join(new_lines)


def main():
    file_path = 'protocolo_PF.html'
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Extract sections
    sections = re.findall(r'<section class="slide"(.*?)</section>', html, re.DOTALL)
    
    parsed_sections = []
    
    for i, sec in enumerate(sections):
        id_match = re.search(r'id="(.*?)"', sec)
        sec_id = id_match.group(1) if id_match else f"section-{i}"
        
        # Extract title
        title_match = re.search(r'<h2>(.*?)</h2>', sec)
        if not title_match:
            title_match = re.search(r'<h1>(.*?)</h1>', sec)
            
        title = title_match.group(1) if title_match else f"Sección {i}"
        
        # Extract text content from cards
        card_content = ""
        cards = re.findall(r'<div class="card".*?>(.*?)</div>', sec, re.DOTALL)
        if cards:
            for card in cards:
                card_content += card + "\n"
        else:
            # Maybe it's the cover
            if "cover" in sec:
                pass # We will replace the cover entirely
        
        parsed_sections.append({
            'id': sec_id,
            'title': title,
            'raw_content': card_content.strip()
        })
        
    print(f"Extracted {len(parsed_sections)} sections.")
    
    # We will build the new HTML
    
    new_html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Centro de Conocimiento | Perú Fibra</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --pf-red: #E31E24;
            --pf-red-light: #fef2f2;
            --pf-red-hover: #cc1b20;
            --pf-white: #ffffff;
            --pf-bg: #f8fafc;
            --pf-gray-50: #f9fafb;
            --pf-gray-100: #f3f4f6;
            --pf-gray-200: #e5e7eb;
            --pf-gray-300: #d1d5db;
            --pf-gray-600: #4b5563;
            --pf-gray-800: #1f2937;
            --pf-gray-900: #111827;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --radius-md: 12px;
            --radius-lg: 16px;
            --transition: all 0.2s ease-in-out;
            
            --sidebar-width: 280px;
            --header-height: 70px;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--pf-bg);
            color: var(--pf-gray-800);
            line-height: 1.6;
            overflow-x: hidden;
            scroll-behavior: smooth;
        }

        /* HEADER */
        .app-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--header-height);
            background: var(--pf-white);
            border-bottom: 1px solid var(--pf-gray-200);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            z-index: 1000;
            box-shadow: var(--shadow-sm);
        }

        .header-left {
            display: flex;
            align-items: center;
            gap: 20px;
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .logo-container img {
            height: 36px;
            width: auto;
        }

        .header-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--pf-gray-900);
            margin-left: 12px;
            padding-left: 12px;
            border-left: 1px solid var(--pf-gray-300);
            display: none;
        }
        @media(min-width: 768px) {
            .header-title { display: block; }
        }

        .header-search {
            position: relative;
            width: 300px;
            margin-left: 20px;
        }
        .header-search input {
            width: 100%;
            padding: 10px 16px 10px 40px;
            border: 1px solid var(--pf-gray-300);
            border-radius: 20px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            background-color: var(--pf-gray-50);
            transition: var(--transition);
        }
        .header-search input:focus {
            outline: none;
            border-color: var(--pf-red);
            background-color: var(--pf-white);
            box-shadow: 0 0 0 3px rgba(227, 30, 36, 0.1);
        }
        .header-search i {
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--pf-gray-600);
        }

        .header-right {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        .header-date {
            font-size: 13px;
            color: var(--pf-gray-600);
            font-weight: 500;
        }
        .user-profile {
            display: flex;
            align-items: center;
            gap: 10px;
            cursor: pointer;
        }
        .avatar {
            width: 36px;
            height: 36px;
            background-color: var(--pf-red);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 14px;
        }
        .user-info {
            display: none;
            flex-direction: column;
        }
        @media(min-width: 768px) {
            .user-info { display: flex; }
        }
        .user-name {
            font-size: 14px;
            font-weight: 600;
            color: var(--pf-gray-900);
        }
        .user-role {
            font-size: 12px;
            color: var(--pf-gray-600);
        }

        /* SIDEBAR */
        .sidebar {
            position: fixed;
            top: var(--header-height);
            left: 0;
            width: var(--sidebar-width);
            height: calc(100vh - var(--header-height));
            background: var(--pf-white);
            border-right: 1px solid var(--pf-gray-200);
            overflow-y: auto;
            z-index: 900;
            transition: var(--transition);
            padding: 24px 0;
            /* Scrollbar styles */
            scrollbar-width: thin;
            scrollbar-color: var(--pf-gray-300) transparent;
        }
        .sidebar::-webkit-scrollbar { width: 6px; }
        .sidebar::-webkit-scrollbar-track { background: transparent; }
        .sidebar::-webkit-scrollbar-thumb { background-color: var(--pf-gray-300); border-radius: 20px; }
        
        .sidebar.collapsed {
            transform: translateX(-100%);
        }

        .nav-category {
            margin-bottom: 24px;
        }
        .nav-category-title {
            padding: 0 24px;
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 700;
            color: var(--pf-gray-600);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .nav-item {
            display: flex;
            align-items: center;
            padding: 10px 24px 10px 48px;
            color: var(--pf-gray-800);
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: var(--transition);
            border-left: 3px solid transparent;
            cursor: pointer;
        }
        .nav-item:hover {
            background-color: var(--pf-gray-50);
            color: var(--pf-red);
        }
        .nav-item.active {
            background-color: var(--pf-red-light);
            color: var(--pf-red);
            border-left-color: var(--pf-red);
            font-weight: 600;
        }

        /* MAIN CONTENT */
        .main-content {
            margin-left: var(--sidebar-width);
            margin-top: var(--header-height);
            min-height: calc(100vh - var(--header-height));
            padding: 40px;
            transition: var(--transition);
            max-width: 1200px;
        }
        .main-content.expanded {
            margin-left: 0;
        }

        .content-section {
            display: none;
            animation: fadeIn 0.4s ease-out;
        }
        .content-section.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* BREADCRUMB */
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: var(--pf-gray-600);
            margin-bottom: 24px;
        }
        .breadcrumb i { font-size: 10px; }
        .breadcrumb span.current { color: var(--pf-red); font-weight: 600; }

        /* PORTADA / COVER */
        .cover-header {
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, var(--pf-red) 0%, #b3161a 100%);
            border-radius: var(--radius-lg);
            color: white;
            margin-bottom: 40px;
            box-shadow: var(--shadow-md);
            position: relative;
            overflow: hidden;
        }
        .cover-header::after {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 60%);
            pointer-events: none;
        }
        .cover-header h1 {
            font-size: 42px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin-bottom: 16px;
        }
        .cover-header p {
            font-size: 18px;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }

        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        .kpi-card {
            background: var(--pf-white);
            padding: 24px;
            border-radius: var(--radius-md);
            box-shadow: var(--shadow-sm);
            border: 1px solid var(--pf-gray-200);
            display: flex;
            align-items: center;
            gap: 16px;
            transition: var(--transition);
        }
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: var(--shadow-md);
        }
        .kpi-icon {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: var(--pf-red-light);
            color: var(--pf-red);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }
        .kpi-info h4 {
            font-size: 13px;
            color: var(--pf-gray-600);
            margin-bottom: 4px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .kpi-info p {
            font-size: 24px;
            font-weight: 800;
            color: var(--pf-gray-900);
        }

        .quick-access {
            margin-bottom: 40px;
        }
        .section-title {
            font-size: 24px;
            font-weight: 700;
            color: var(--pf-gray-900);
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .qa-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .qa-card {
            background: var(--pf-white);
            border: 1px solid var(--pf-gray-200);
            border-radius: var(--radius-md);
            padding: 24px;
            cursor: pointer;
            transition: var(--transition);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .qa-card:hover {
            border-color: var(--pf-red);
            box-shadow: var(--shadow-md);
            transform: translateY(-3px);
        }
        .qa-header {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .qa-header i {
            font-size: 24px;
            color: var(--pf-red);
        }
        .qa-header h3 {
            font-size: 18px;
            font-weight: 700;
            color: var(--pf-gray-900);
        }
        .qa-card p {
            font-size: 14px;
            color: var(--pf-gray-600);
        }

        /* CONTENT STYLES */
        .content-title {
            font-size: 32px;
            font-weight: 800;
            color: var(--pf-gray-900);
            margin-bottom: 32px;
            padding-bottom: 16px;
            border-bottom: 2px solid var(--pf-gray-200);
        }
        
        .section-subtitle {
            font-size: 20px;
            font-weight: 700;
            color: var(--pf-red);
            margin: 32px 0 16px;
        }

        .content-section p {
            margin-bottom: 16px;
            font-size: 15px;
            color: var(--pf-gray-800);
        }

        /* SPEECH CARD */
        .speech-card {
            background-color: var(--pf-gray-50);
            border-left: 4px solid var(--pf-red);
            border-radius: 0 var(--radius-md) var(--radius-md) 0;
            margin: 24px 0;
            box-shadow: var(--shadow-sm);
            overflow: hidden;
            border: 1px solid var(--pf-gray-200);
            border-left-width: 4px;
        }
        .speech-header {
            background-color: var(--pf-white);
            padding: 12px 20px;
            border-bottom: 1px solid var(--pf-gray-200);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .speech-title {
            font-weight: 700;
            font-size: 14px;
            color: var(--pf-gray-900);
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .speech-title i { color: var(--pf-red); }
        .btn-copy {
            background: var(--pf-gray-100);
            border: 1px solid var(--pf-gray-300);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            color: var(--pf-gray-800);
            cursor: pointer;
            transition: var(--transition);
        }
        .btn-copy:hover {
            background: var(--pf-gray-200);
        }
        .speech-body {
            padding: 20px;
            font-style: italic;
            color: var(--pf-gray-800);
            font-size: 15px;
            line-height: 1.7;
        }

        /* TIMELINE (PROCEDURES) */
        .timeline {
            position: relative;
            margin: 32px 0;
            padding-left: 24px;
        }
        .timeline::before {
            content: '';
            position: absolute;
            left: 5px;
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: var(--pf-gray-300);
        }
        .timeline-item {
            position: relative;
            margin-bottom: 24px;
        }
        .timeline-marker {
            position: absolute;
            left: -24px;
            top: 4px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: var(--pf-red);
            border: 2px solid var(--pf-white);
            box-shadow: 0 0 0 2px var(--pf-red-light);
        }
        .timeline-content {
            background: var(--pf-white);
            padding: 16px 20px;
            border-radius: var(--radius-md);
            border: 1px solid var(--pf-gray-200);
            box-shadow: var(--shadow-sm);
        }
        .timeline-title {
            font-size: 15px;
            font-weight: 700;
            color: var(--pf-gray-900);
            margin-bottom: 8px;
        }
        .timeline-desc {
            font-size: 14px;
            color: var(--pf-gray-600);
            margin: 0;
        }

        /* LISTS */
        .modern-list {
            list-style: none;
            margin: 16px 0;
        }
        .modern-list li {
            position: relative;
            padding-left: 24px;
            margin-bottom: 10px;
            font-size: 15px;
        }
        .modern-list li::before {
            content: '\\f058'; /* fa-circle-check */
            font-family: 'Font Awesome 6 Free';
            font-weight: 900;
            position: absolute;
            left: 0;
            top: 2px;
            color: var(--pf-red);
            font-size: 14px;
        }

        /* ALERTS */
        .alert {
            padding: 16px 20px;
            border-radius: var(--radius-md);
            margin: 24px 0;
            display: flex;
            gap: 16px;
            font-size: 15px;
        }
        .alert i { font-size: 20px; }
        .alert-info { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e3a8a; }
        .alert-info i { color: #3b82f6; }
        .alert-warning { background: #fefce8; border: 1px solid #fef08a; color: #713f12; }
        .alert-warning i { color: #eab308; }

        /* PROGRESS BAR */
        .reading-progress-container {
            position: fixed;
            top: var(--header-height);
            left: 0;
            width: 100%;
            height: 3px;
            background: transparent;
            z-index: 1000;
        }
        .reading-progress-bar {
            height: 100%;
            background: var(--pf-red);
            width: 0%;
        }

        /* BACK TO TOP */
        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: var(--pf-red);
            color: white;
            border: none;
            box-shadow: var(--shadow-lg);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            opacity: 0;
            visibility: hidden;
            transition: var(--transition);
            z-index: 999;
        }
        .back-to-top.visible {
            opacity: 1;
            visibility: visible;
        }
        .back-to-top:hover {
            background: var(--pf-red-hover);
            transform: translateY(-3px);
        }

        /* HAMBURGER */
        .btn-menu {
            display: none;
            background: transparent;
            border: none;
            font-size: 24px;
            color: var(--pf-gray-800);
            cursor: pointer;
        }
        @media(max-width: 1024px) {
            .btn-menu { display: block; }
            .sidebar { transform: translateX(-100%); }
            .sidebar.active { transform: translateX(0); }
            .main-content { margin-left: 0; }
        }
    </style>
</head>
<body>

    <div class="reading-progress-container">
        <div class="reading-progress-bar" id="readingProgress"></div>
    </div>

    <!-- HEADER -->
    <header class="app-header">
        <div class="header-left">
            <button class="btn-menu" onclick="toggleSidebar()">
                <i class="fas fa-bars"></i>
            </button>
            <div class="logo-container">
                <!-- Replace with correct logo -->
                <span style="font-weight:800;color:var(--pf-red);font-size:24px;">PERÚ FIBRA</span>
            </div>
            <div class="header-title">Centro de Conocimiento</div>
            <div class="header-search">
                <i class="fas fa-search"></i>
                <input type="text" id="searchInput" placeholder="Buscar protocolos, speech, etc...">
            </div>
        </div>
        <div class="header-right">
            <div class="header-date">Act. Ago 2026</div>
            <div class="user-profile">
                <div class="user-info">
                    <span class="user-name">Asesor ATC</span>
                    <span class="user-role">Fidelización</span>
                </div>
                <div class="avatar">A</div>
            </div>
        </div>
    </header>

    <!-- SIDEBAR -->
    <nav class="sidebar" id="sidebar">
        <div class="nav-category">
            <div class="nav-category-title"><i class="fas fa-book-open"></i> Introducción</div>
            <a class="nav-item active" onclick="showSection('portada', this)">Portada</a>
            <a class="nav-item" onclick="showSection('sec-1', this)">Nuestros Lineamientos</a>
            <a class="nav-item" onclick="showSection('sec-2', this)">ABC Perú Fibra</a>
            <a class="nav-item" onclick="showSection('sec-3', this)">ABC Gamer</a>
        </div>
        
        <div class="nav-category">
            <div class="nav-category-title"><i class="fas fa-headset"></i> Atención al Cliente</div>
            <a class="nav-item" onclick="showSection('sec-4', this)">Protocolo de Llamada</a>
            <a class="nav-item" onclick="showSection('sec-5', this)">Validaciones de Datos</a>
            <a class="nav-item" onclick="showSection('sec-6', this)">Seguridad y Retención</a>
        </div>

        <div class="nav-category">
            <div class="nav-category-title"><i class="fas fa-user-times"></i> Bajas y Modificaciones</div>
            <a class="nav-item" onclick="showSection('sec-7', this)">Protocolo de Baja</a>
            <a class="nav-item" onclick="showSection('sec-8', this)">Cambio de Plan</a>
        </div>

        <div class="nav-category">
            <div class="nav-category-title"><i class="fas fa-tools"></i> Soporte Técnico</div>
            <a class="nav-item" onclick="showSection('sec-9', this)">Pérdida de Servicio</a>
            <a class="nav-item" onclick="showSection('sec-10', this)">Ancho de Banda / WiFi</a>
        </div>

        <div class="nav-category">
            <div class="nav-category-title"><i class="fas fa-cogs"></i> Gestiones y Otros</div>
            <a class="nav-item" onclick="showSection('sec-11', this)">Cliente Difícil</a>
            <a class="nav-item" onclick="showSection('sec-12', this)">Contingencias</a>
            <a class="nav-item" onclick="showSection('sec-13', this)">Traslados y Suspensión</a>
            <a class="nav-item" onclick="showSection('sec-14', this)">Facturación</a>
            <a class="nav-item" onclick="showSection('sec-15', this)">Escalación Supervisor</a>
            <a class="nav-item" onclick="showSection('sec-16', this)">Formatos de Cesión</a>
        </div>
    </nav>

    <!-- MAIN CONTENT -->
    <main class="main-content" id="mainContent">
        
        <!-- COVER SECTION -->
        <section id="portada" class="content-section active">
            <div class="cover-header">
                <h1>Protocolo de Atención al Cliente</h1>
                <p>Guía operativa interactiva para asesores de atención, soporte y fidelización.</p>
            </div>

            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-icon"><i class="fas fa-file-alt"></i></div>
                    <div class="kpi-info">
                        <h4>Protocolos</h4>
                        <p>16</p>
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon"><i class="fas fa-clock"></i></div>
                    <div class="kpi-info">
                        <h4>Última Act.</h4>
                        <p>Ago 2026</p>
                    </div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-icon"><i class="fas fa-check-circle"></i></div>
                    <div class="kpi-info">
                        <h4>Estado</h4>
                        <p>Vigente</p>
                    </div>
                </div>
            </div>

            <h2 class="section-title"><i class="fas fa-bolt"></i> Accesos Rápidos</h2>
            <div class="qa-grid">
                <div class="qa-card" onclick="document.querySelector('a[onclick*=\\'sec-4\\']').click()">
                    <div class="qa-header">
                        <i class="fas fa-phone-alt"></i>
                        <h3>Atención General</h3>
                    </div>
                    <p>Estructura de llamada, validaciones y protocolo inicial.</p>
                </div>
                <div class="qa-card" onclick="document.querySelector('a[onclick*=\\'sec-9\\']').click()">
                    <div class="qa-header">
                        <i class="fas fa-wifi"></i>
                        <h3>Soporte Técnico</h3>
                    </div>
                    <p>Problemas de conexión, lentitud, router y mesh.</p>
                </div>
                <div class="qa-card" onclick="document.querySelector('a[onclick*=\\'sec-14\\']').click()">
                    <div class="qa-header">
                        <i class="fas fa-file-invoice-dollar"></i>
                        <h3>Facturación</h3>
                    </div>
                    <p>Ajustes, deudas, pagos y recibos.</p>
                </div>
                <div class="qa-card" onclick="document.querySelector('a[onclick*=\\'sec-7\\']').click()">
                    <div class="qa-header">
                        <i class="fas fa-times-circle"></i>
                        <h3>Bajas</h3>
                    </div>
                    <p>Procesos de retención y solicitudes de baja.</p>
                </div>
            </div>
        </section>

"""
    
    # We will map the old slide indices to new section IDs
    # Based on the original nav items
    
    for section in parsed_sections:
        if "slide-0" in section['id']:
            continue # Skip old cover
            
        # extract ID number
        idx_match = re.search(r'\d+', section['id'])
        if not idx_match: continue
        sec_num = idx_match.group(0)
        
        new_id = f"sec-{sec_num}"
        
        processed_content = process_text_into_components(section['raw_content'])
        
        # Wrap all timeline items correctly
        processed_content = re.sub(r'(<div class="timeline-item">.*?</div>\s*</div>)', r'\1', processed_content, flags=re.DOTALL)
        
        # Simple wrap of timeline blocks
        if '<div class="timeline-item">' in processed_content:
            processed_content = processed_content.replace('<div class="timeline-item">', '<div class="timeline">\n<div class="timeline-item">', 1)
            # Find the last </div> belonging to the last timeline-item and close .timeline
            processed_content += "\n</div><!-- close timeline -->"
            
        new_html += f"""
        <section id="{new_id}" class="content-section">
            <div class="breadcrumb">
                <span>Introducción</span> <i class="fas fa-chevron-right"></i> <span class="current">{section['title']}</span>
            </div>
            <h1 class="content-title">{section['title']}</h1>
            
            <div class="content-body">
                {processed_content}
            </div>
        </section>
"""

    new_html += """
    </main>

    <button class="back-to-top" id="backToTop" onclick="window.scrollTo(0,0)">
        <i class="fas fa-arrow-up"></i>
    </button>

    <script>
        // NAVIGATION LOGIC
        function showSection(sectionId, navElement) {
            // Hide all sections
            document.querySelectorAll('.content-section').forEach(sec => {
                sec.classList.remove('active');
            });
            
            // Show target section
            const target = document.getElementById(sectionId);
            if (target) {
                target.classList.add('active');
            }

            // Update active state in sidebar
            if (navElement) {
                document.querySelectorAll('.nav-item').forEach(nav => {
                    nav.classList.remove('active');
                });
                navElement.classList.add('active');
            }

            // Update breadcrumb category
            if(target) {
                const categoryText = navElement ? navElement.closest('.nav-category').querySelector('.nav-category-title').innerText : 'Categoría';
                const breadcrumbCat = target.querySelector('.breadcrumb span:first-child');
                if(breadcrumbCat) {
                    breadcrumbCat.innerText = categoryText.trim();
                }
            }

            // Close sidebar on mobile
            if (window.innerWidth <= 1024) {
                document.getElementById('sidebar').classList.remove('active');
            }

            window.scrollTo(0,0);
        }

        // SIDEBAR TOGGLE
        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        // COPY TO CLIPBOARD
        function copyText(btn) {
            const speechBody = btn.parentElement.nextElementSibling;
            const textToCopy = speechBody.innerText;

            navigator.clipboard.writeText(textToCopy).then(() => {
                const originalText = btn.innerText;
                btn.innerText = '¡Copiado!';
                btn.style.backgroundColor = '#10b981';
                btn.style.color = '#fff';
                
                setTimeout(() => {
                    btn.innerText = originalText;
                    btn.style.backgroundColor = '';
                    btn.style.color = '';
                }, 2000);
            });
        }

        // SCROLL PROGRESS & BACK TO TOP
        window.addEventListener('scroll', () => {
            // Progress Bar
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById("readingProgress").style.width = scrolled + "%";

            // Back to Top button
            const backToTop = document.getElementById('backToTop');
            if (winScroll > 300) {
                backToTop.classList.add('visible');
            } else {
                backToTop.classList.remove('visible');
            }
        });
        
        // SEARCH FUNCTIONALITY (Basic filter)
        document.getElementById('searchInput').addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase();
            const navItems = document.querySelectorAll('.nav-item');
            
            navItems.forEach(item => {
                if (item.innerText.toLowerCase().includes(query)) {
                    item.style.display = 'flex';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    </script>
</body>
</html>
"""

    with open('protocolo_PF_new.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully created protocolo_PF_new.html")

if __name__ == "__main__":
    main()
