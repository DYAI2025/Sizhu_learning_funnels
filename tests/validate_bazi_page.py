#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HTML_PATH=ROOT/'public'/'learn'/'bazi'/'index.html'
CSS_PATH=ROOT/'public'/'learn'/'bazi'/'styles.css'
JS_PATH=ROOT/'public'/'learn'/'bazi'/'app.js'
class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1=0; self.ids=set(); self.links=[]; self.tables=0; self.captions=0; self.landmarks=set(); self.lang=None; self.canonical=None; self.jsonld=[]; self._j=False; self._b=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='html': self.lang=a.get('lang')
        if tag=='h1': self.h1+=1
        if 'id' in a: self.ids.add(a['id'])
        if tag=='a' and a.get('href'): self.links.append(a['href'])
        if tag=='table': self.tables+=1
        if tag=='caption': self.captions+=1
        if tag in {'header','nav','main','article','aside','footer'}: self.landmarks.add(tag)
        if tag=='link' and a.get('rel')=='canonical': self.canonical=a.get('href')
        if tag=='script' and a.get('type')=='application/ld+json': self._j=True; self._b=[]
    def handle_data(self,data):
        if self._j: self._b.append(data)
    def handle_endtag(self,tag):
        if tag=='script' and self._j: self.jsonld.append(''.join(self._b)); self._j=False

def main():
    errors=[]
    for path in [HTML_PATH,CSS_PATH,JS_PATH]:
        if not path.exists(): errors.append(f'missing file: {path.relative_to(ROOT)}')
    if errors:
        print(json.dumps({'status':'FAIL','errors':errors},indent=2)); return 1
    html=HTML_PATH.read_text(encoding='utf-8'); css=CSS_PATH.read_text(encoding='utf-8'); js=JS_PATH.read_text(encoding='utf-8')
    p=P(); p.feed(html)
    checks=[(p.lang=='en','html lang must be en'),(p.h1==1,f'expected one h1, found {p.h1}'),(p.canonical=='https://sizhuatelier.shop/learn/bazi/','canonical mismatch'),(p.tables==p.captions,'every table needs caption'),({'header','nav','main','article','aside','footer'}.issubset(p.landmarks),'landmarks incomplete'),('class="skip-link"' in html,'skip link missing'),('prefers-reduced-motion' in css,'reduced motion missing'),(':focus-visible' in css,'focus-visible missing'),('overflow-x: auto' in css,'table overflow missing')]
    for ok,msg in checks:
        if not ok: errors.append(msg)
    for term in ['八字','四柱','干支','天干','地支','日主','藏干','五行','节气','立春','大运','合婚','bāzì','sìzhù','gānzhī','tiāngān','dìzhī','rìzhǔ','cánggān','wǔxíng','jiéqì','lìchūn','dà yùn','héhūn']:
        if term not in html: errors.append(f'missing term: {term}')
    for event in ['learn_hub_click','related_page_click','cta_shop_click','cta_etsy_click','cta_bazi_chart_click','section_view','scroll_depth_25','scroll_depth_50','scroll_depth_75','scroll_depth_100','diagram_interaction']:
        if event not in html and event not in js: errors.append(f'missing event: {event}')
    for pat in [r'scientifically proven',r'clinically validated',r'guaranteed compatibility',r'will definitely']:
        if re.search(pat,html,re.I): errors.append(f'forbidden claim: {pat}')
    for raw in p.jsonld: json.loads(raw)
    if not p.jsonld: errors.append('JSON-LD missing')
    for href in [x for x in p.links if x.startswith('#')]:
        if href[1:] not in p.ids: errors.append(f'broken anchor: {href}')
    print(json.dumps({'status':'PASS' if not errors else 'FAIL','evidence':'STATIC_VALIDATED' if not errors else 'BLOCKED_QUALITY_GATE','errors':errors},ensure_ascii=False,indent=2))
    return 0 if not errors else 1
if __name__=='__main__': sys.exit(main())
