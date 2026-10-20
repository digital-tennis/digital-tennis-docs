#!/usr/bin/env python3
"""Validate local GitBook content, original WBS and beginner assignment navigation."""
import collections,json,pathlib,re,urllib.parse
root=pathlib.Path(__file__).resolve().parents[1];docs=root/'docs';errors=[];links=0
def fail(message):errors.append(message)
def anchor(text):return re.sub(r'[^\w\- ]','',text.strip().lower()).replace(' ','-')
for config in (root/'.gitbook.yaml',docs/'.gitbook.yaml'):
    content=config.read_text();match=re.search(r'^root:\s*(.+)$',content,re.M)
    if not match:fail('Missing root '+str(config));continue
    base=(config.parent/match[1].strip().strip('"\'')).resolve()
    if base!=docs.resolve():fail('Unexpected content root '+str(config))
    for field in ('readme','summary'):
        target=re.search(r'^\s+'+field+r':\s*(.+)$',content,re.M)
        if not target or not (base/target[1].strip()).is_file():fail('Invalid '+field+' in '+str(config))
for page in docs.rglob('*.md'):
    text=re.sub(r'```.*?```','',page.read_text(),flags=re.S)
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',text):
        target=target.strip().split(' "',1)[0].strip('<>');url=urllib.parse.urlsplit(target)
        if url.scheme or target.startswith('//'):continue
        destination=(page.parent/urllib.parse.unquote(url.path)).resolve() if url.path else page.resolve();links+=1
        if not destination.is_relative_to(docs.resolve()) or not destination.exists():fail(str(page.relative_to(root))+': missing/escaping '+target);continue
        if url.fragment and destination.suffix=='.md':
            headings={anchor(value) for value in re.findall(r'^#{1,6}\s+(.+)$',destination.read_text(),re.M)}
            if urllib.parse.unquote(url.fragment) not in headings:fail(str(page.relative_to(root))+': missing anchor '+target)
wbs=json.loads((docs/'planning/wbs.json').read_text());items=wbs['items']
if (wbs['developers'],wbs['days'],wbs['total_pd'])!=(3,12,36):fail('Preserve original 12 days / 3 people / 36PD')
if len(items)!=72 or sum(x['pd'] for x in items)!=36:fail('Original WBS slots/effort changed')
effort=collections.Counter()
for item in items:effort[item['owner']]+=item['pd']
if effort!=collections.Counter({'A':12,'B':12,'C':12}):fail('Original developer effort changed')
tasks={match for page in (docs/'products').glob('digital-tennis-*.md') for match in re.findall(r'^## ((?:FW|PR|BL|GM|AI|MS|DC)-\d+)',page.read_text(),re.M)}
if len(tasks)!=37 or {x['task'] for x in items}-tasks:fail('Missing original beginner assignment')
vectors=json.loads((docs/'testing/protocol-vectors.json').read_text())
if vectors.get('wire_versions')!=[1,2,3]:fail('Current controller version vectors missing')
if errors:raise SystemExit('\n'.join(errors))
print(json.dumps({'passed':True,'markdownPages':len(list(docs.rglob('*.md'))),'localLinks':links,'originalAssignments':len(tasks),'originalWbsSlots':len(items),'scope':'GitBook files/navigation and original planning integrity; actual account publication is separate'}))
