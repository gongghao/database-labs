"""Check distributable links and data integrity without third-party packages."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import csv, hashlib, json, zipfile
ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.ids=set(); self.links=[]; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids, f'Duplicate id: {a["id"]}'
            self.ids.add(a['id'])
        for key in ('href','src'):
            if key in a:self.links.append(a[key])
count=0
for page in SITE.rglob('*.html'):
    doc=Document(page.read_text())
    for link in doc.links:
        parts=urlsplit(link)
        if parts.scheme or parts.netloc:continue
        target=(page.parent/unquote(parts.path)).resolve() if parts.path else page
        assert target.is_relative_to(SITE.resolve()), f'Escapes website: {link}'
        assert target.exists(), f'Missing: {link}'
        if parts.fragment:
            assert parts.fragment in Document(target.read_text()).ids, f'Missing anchor: {link}'
        count+=1
keys={'student':['sid'],'dept':['dname'],'prof':['pname'],'course':['cno','dname'],'major':['dname','sid'],'section':['dname','cno','sectno'],'enroll':['sid','dname','cno','sectno']}
base=SITE/'projects/project1'
manifest=json.loads((base/'data/manifest.json').read_text())
total=0
with zipfile.ZipFile(base/'materials/project1_data.zip') as archive:
    for item in manifest:
        path=base/'data'/item['file'];raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256']
        assert raw==archive.read(path.name), f'ZIP mismatch: {path.name}'
        rows=list(csv.DictReader(path.open(),delimiter='\t',skipinitialspace=True))
        assert len(rows)==item['rows']
        values=[tuple(row[k] for k in keys[path.stem]) for row in rows]
        assert len(values)==len(set(values)), f'Duplicate primary key in {path.name}'
        assert all(all(v!='' for v in key) for key in values)
        total+=len(rows)
assert total==371
print(f'PASS: {count} local links, 7 datasets, {total} rows; all primary keys and ZIP hashes match.')
