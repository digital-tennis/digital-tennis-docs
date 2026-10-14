"""Check local documentation links, assignment coverage, WBS totals and vectors."""
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit
import json
import re
import sys

root=Path(__file__).resolve().parents[1]
errors=[]
def require(ok,message):
    if not ok:errors.append(message)

def anchors(path):
    result=set()
    for title in re.findall(r'^#{1,6}\s+(.+)$',path.read_text(),re.M):
        title=re.sub(r'[^\w\s-]','',title.strip().lower()).replace(' ','-')
        result.add(title)
    return result

markdown=list(root.rglob('*.md'))
for path in markdown:
    if '.git' in path.parts:continue
    text=path.read_text()
    text=re.sub(r'```.*?```','',text,flags=re.S)
    for href in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
        target=urlsplit(href.split(' "')[0])
        if target.scheme or target.netloc:continue
        dest=(path.parent/unquote(target.path)).resolve() if target.path else path
        require(dest.is_file(),f'{path.relative_to(root)}: missing {href}')
        if target.fragment and dest.is_file() and dest.suffix=='.md':
            require(unquote(target.fragment).lower() in anchors(dest),f'{path.relative_to(root)}: missing anchor {href}')

summary=(root/'docs/SUMMARY.md').read_text()
nav=re.findall(r'\]\(([^)]+\.md)\)',summary)
require(len(nav)==len(set(nav)),'SUMMARY contains duplicate pages')
actual={str(p.relative_to(root/'docs')) for p in (root/'docs').rglob('*.md') if p.name!='SUMMARY.md'}
require(set(nav)==actual,f'SUMMARY coverage mismatch: {actual.symmetric_difference(set(nav))}')
require((root/'.gitbook.yaml').read_text().startswith('root: ./docs/'),'repo GitBook root must be docs/')
require((root/'docs/.gitbook.yaml').read_text().startswith('root: ./\n'),'mapped-space GitBook root must be ./')

tasks=set()
for path in (root/'docs/products').glob('digital-tennis-*.md'):
    ids=re.findall(r'^## ([A-Z]{2}-\d{2})$',path.read_text(),re.M)
    tasks.update(ids)
    for ident in ids:
        block=re.search(r'(?ms)^## '+ident+r'\n(.*?)(?=^## |\Z)',path.read_text()).group(1)
        for heading in ['구현할 동작','선행 조건과 입력','출력과 반환값','동작 규칙','입력과 기대 결과 예제','예외와 경계 조건','권장 구현 순서','완료 판정','제출할 결과']:
            require('### '+heading in block,f'{ident}: missing {heading}')
require(len(tasks)==37,'expected 37 product assignments')
wbs=json.loads((root/'docs/planning/wbs.json').read_text())
items=wbs['items']
require(len(items)==72,'expected 72 WBS items')
require(sum(x['pd'] for x in items)==36,'expected 36 person-days')
require(set(x['task'] for x in items)==tasks,'all assignment IDs must appear in WBS')
counts=Counter((x['owner'],x['day']) for x in items)
require(len(counts)==36 and all(x==2 for x in counts.values()),'expected 2 half-days for each person/day')
require(set(x['owner'] for x in items)=={'A','B','C'},'expected 3 developers')
require(set(x['day'] for x in items)==set(range(1,13)),'expected D1 to D12')
mdrows=re.findall(r'^\| W-\d{2} \|', (root/'docs/planning/wbs.md').read_text(), re.M)
require(len(mdrows)==72,'Markdown WBS must also contain 72 rows')

def crc8(data):
    value=0
    for byte in data:
        value^=byte
        for _ in range(8):
            value=((value*2)^7)&255 if value>=128 else (value*2)&255
    return value
require(crc8(b'123456789')==0xf4,'CRC known-answer check failed')
vectors=json.loads((root/'docs/testing/protocol-vectors.json').read_text())
for vector in vectors['cases']:
    data=bytes.fromhex(vector['hex'])
    if vector['expected_error']=='INVALID_LENGTH':
        require(len(data)!=20,'short packet example must be short')
        continue
    require(len(data)==20,f'{vector["name"]}: expected 20 bytes')
    crc_ok=crc8(data[:19])==data[19]
    require(crc_ok != (vector['expected_error']=='BAD_CRC'),f'{vector["name"]}: CRC mismatch')

avatar=root/'docs/assets/digital-tennis-github-avatar-500.png'
header=avatar.read_bytes()
require(header[:8]==b'\x89PNG\r\n\x1a\n','avatar must be PNG')
require(int.from_bytes(header[16:20],'big')==500 and int.from_bytes(header[20:24],'big')==500,'avatar must be 500x500')
require(avatar.stat().st_size<1_000_000,'avatar must be below 1 MB')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(markdown)} Markdown files, {len(tasks)} assignments, 72 half-day items, 36 person-days, {len(vectors["cases"])} packet vectors, GitBook navigation, PNG size.')
