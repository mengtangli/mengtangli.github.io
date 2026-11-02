from pathlib import Path
import json, re
root=Path(__file__).resolve().parent.parent
records=json.loads((root/'assets/data/publications.json').read_text(encoding='utf-8'))
ids={r['id'] for r in records}
assert len(ids)==88
for name in ['index.html','generic.html','elements.html']:
    page=(root/name).read_text(encoding='utf-8')
    for url in re.findall(r'(?:href|src)="([^"]+)"',page):
        if url.startswith(('http:','https:','#','mailto:','data:')): continue
        assert (root/url.split('#')[0]).exists(), (name,url)
    if name=='generic.html':
        refs=re.findall(r'elements.html#([^"]+)',page)
        assert all(r in ids for r in refs)
        assert page.count('class="research-row"')==11
        assert page.count('class="related-papers"></ul>')==0
        assert 'Project Group:' not in page
        assert 'My Ph.D. project.' not in page
    if name=='elements.html':
        assert len(re.findall('class="publication"',page))==88
        assert 'data-copy' not in page
        assert 'Copy citation' not in page
        assert 'href="citations/' not in page
        assert 'BibTeX' not in page
        assert 'Permalink' not in page
        assert 'Page link' not in page
        assert 'scholar.google' not in page
        for record in records:
            entry=re.search(r'<li id="'+record['id']+r'".*?</li>',page,re.S).group()
            if record['url']:
                from html import escape
                import html
                links=re.findall(r'<a href="([^"]+)"[^>]*>Link</a>',entry)
                assert [html.unescape(url) for url in links]==[record['url']]
            else:
                assert '<a ' not in entry
assert not list((root/'citations').glob('*.bib'))
assert '<title>Mengtang Li - Vanderbilt University</title>' in (root/'index.html').read_text()
print('PASS: 88 unique citation records, 11 illustrated research rows, local assets and citation links.')

