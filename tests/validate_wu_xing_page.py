from html.parser import HTMLParser
from pathlib import Path
import json, re, sys

PAGE = Path(__file__).resolve().parents[1] / "public" / "learn" / "wu-xing" / "index.html"

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.lang=None; self.h1=0; self.ids=set(); self.hrefs=[]; self.jsonld=[]; self._json=False; self._buf=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=="html": self.lang=a.get("lang")
        if tag=="h1": self.h1+=1
        if "id" in a: self.ids.add(a["id"])
        if tag=="a" and "href" in a: self.hrefs.append(a["href"])
        if tag=="script" and a.get("type")=="application/ld+json": self._json=True; self._buf=[]
    def handle_data(self, data):
        if self._json: self._buf.append(data)
    def handle_endtag(self, tag):
        if tag=="script" and self._json: self.jsonld.append("".join(self._buf)); self._json=False

html=PAGE.read_text(encoding="utf-8"); p=Parser(); p.feed(html); errors=[]
if p.lang!="en": errors.append("html lang must be en")
if p.h1!=1: errors.append(f"expected one h1, found {p.h1}")
missing=[h for h in p.hrefs if h.startswith("#") and h[1:] not in p.ids]
if missing: errors.append(f"missing anchors: {missing}")
if "https://sizhuatelier.shop/learn/wu-xing/" not in html: errors.append("canonical route missing")
if "bazodiac.space/learn/wu-xing-five-phases" in html: errors.append("obsolete canonical remains")
for token in ["五行","木","火","土","金","水","相生","相克"]:
    if token not in html: errors.append(f"missing token {token}")
for event in ["learn_wuxing_cta_shop_click","learn_wuxing_cta_etsy_click","learn_wuxing_internal_link_click","learn_wuxing_scroll_depth"]:
    if event not in html: errors.append(f"missing analytics event {event}")
for raw in p.jsonld: json.loads(raw)
if not p.jsonld: errors.append("JSON-LD missing")
if re.search(r'creativeWorkStatus\s*"\s*:\s*"Draft', html): errors.append("draft status remains")
print(json.dumps({"status":"PASS" if not errors else "FAIL","errors":errors},ensure_ascii=False,indent=2))
sys.exit(1 if errors else 0)
