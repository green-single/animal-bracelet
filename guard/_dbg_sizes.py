# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
for f in ['app/static/animal.html', 'app/static/index.html', 'app/static/claim.html', 'app/static/admin.html']:
    c = open(f, encoding='utf-8', newline='').read()
    n = len(c)
    style_n = 0; script_n = 0
    import re
    for m in re.finditer(r'<style[^>]*>(.*?)</style>', c, re.S):
        style_n += len(m.group(1))
    for m in re.finditer(r'<script(?![^>]*src)[^>]*>(.*?)</script>', c, re.S):
        script_n += len(m.group(1))
    print(f'{f}: {n//1024}KB | style {style_n//1024}KB | inline_script {script_n//1024}KB | CRLF {"\\r\\n" in c}')
    # head前120字符
    i = c.find('<head')
    print('  head片段:', repr(c[i:i+150]))
