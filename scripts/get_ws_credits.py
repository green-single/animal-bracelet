# -*- coding: utf-8 -*-
"""获取5张照片的author+license"""
import json, urllib.request, urllib.parse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 AnimalBracelet/1.0'
titles = [
    "File:7989 S Africa white shark JF.jpg",
    "File:Great white Dyer island 2010-07.jpg",
    "File:Carcharodon carcharias, Gansbaai (South Africa).jpg",
    "File:Great White Shark (14730693310).jpg",
    "File:Great white aqurium.jpg",
]
for t in titles:
    api = ('https://commons.wikimedia.org/w/api.php?action=query&titles=' +
           urllib.parse.quote(t) +
           '&prop=imageinfo&iiprop=url%7Cextmetadata&format=json')
    req = urllib.request.Request(api, headers={'User-Agent': UA})
    d = json.loads(urllib.request.urlopen(req, timeout=30).read().decode('utf-8'))
    for p in d['query']['pages'].values():
        ii = p.get('imageinfo', [{}])[0]
        md = ii.get('extmetadata', {})
        artist = md.get('Artist', {}).get('value', '?')
        lic = md.get('LicenseShortName', {}).get('value', '?')
        # 清理HTML标签
        import re
        artist = re.sub(r'<[^>]+>', '', artist).strip()[:80]
        print(t)
        print('  作者:', artist)
        print('  许可:', lic)
