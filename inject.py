with open('protocolo_peru_fibra.html', encoding='utf-8') as f:
    html = f.read()

error_script = '''<script>
window.onerror = function(msg, url, lineNo, columnNo, error) {
    window.onload = function() {
        document.body.innerHTML = '<div style="padding: 20px; background: red; color: white; z-index: 99999; position: relative;"><h1>JS Error</h1><p>' + msg + '</p><p>Line: ' + lineNo + ':' + columnNo + '</p></div>';
    };
};
</script>
'''

if 'window.onerror' not in html:
    html = html.replace('<head>', '<head>\n' + error_script)
    with open('protocolo_peru_fibra.html', 'w', encoding='utf-8') as f:
        f.write(html)
