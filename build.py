# 由 wiki/catalog.json 與 Markdown 筆記生成靜態網站；僅用 Python 標準函式庫。
from pathlib import Path
import json, html, re
R=Path(__file__).resolve().parents[1]
E=html.escape
COURSES={'physics':'普通物理學','statistics':'統計學'}
def render(md):
    parts=[]; pending=None; in_list=False
    def close():
        nonlocal in_list
        if in_list: parts.append('</ul>'); in_list=False
    for line in md.splitlines():
        line=line.strip()
        if not line: close(); continue
        if line.startswith('# '): continue
        if line.startswith('## '):
            close(); parts.append('<h2>'+E(line[3:])+'</h2>')
        elif line.startswith('- '):
            if not in_list: parts.append('<ul>'); in_list=True
            parts.append('<li>'+E(line[2:])+'</li>')
        elif line.startswith('Q: '):
            close()
            if pending is not None: raise ValueError('題目缺少答案')
            pending=line[3:]
        elif line.startswith('A: '):
            close()
            if pending is None: raise ValueError('答案缺少題目')
            parts.append('<details><summary>'+E(pending)+'</summary><p>'+E(line[3:])+'</p></details>'); pending=None
        else: close(); parts.append('<p>'+E(line)+'</p>')
    close()
    if pending is not None: raise ValueError('題目缺少答案')
    return '\n'.join(parts)
def shell(title,body,base=''):
    return f'''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} | Study Journal</title><link rel="stylesheet" href="{base}assets/style.css"></head>
<body><header class="top"><a class="brand" href="{base}index.html">Study Journal<span>我的大學學習知識庫</span></a><nav><a href="{base}index.html">筆記首頁</a></nav></header>
<main>{body}</main><footer>Study Journal · 以課程講義為基礎，持續累積的學習筆記</footer></body></html>'''
def build():
    items=json.loads((R/'wiki/catalog.json').read_text(encoding='utf-8'))
    seen=set(); cards=[]
    for item in items:
        c,s=item['course'],item['slug']
        if c not in COURSES or not re.fullmatch(r'[a-z0-9-]+',s): raise ValueError('無效課程或命名')
        if (c,s) in seen: raise ValueError('重複筆記')
        seen.add((c,s))
        md=R/item['markdown']
        if md != R/f'wiki/{c}/{s}.md': raise ValueError('路徑不一致')
        raw=md.read_text(encoding='utf-8')
        if raw.splitlines()[0] != '# '+item['title']: raise ValueError('標題不一致')
        for sec in ['學習目標','核心觀念','重要公式','重點整理','自我測驗','資料來源']:
            if '## '+sec not in raw: raise ValueError(f'缺少 {sec}: {s}')
        out=R/f'notes/{c}/{s}.html'; out.parent.mkdir(parents=True,exist_ok=True)
        body=f'<a class="back" href="../../index.html">← 所有筆記</a><article><div class="eyebrow">{E(COURSES[c])} · {E(item["chapter"])}</div><h1>{E(item["title"])}</h1><p class="lead">{E(item["description"])}</p>{render(raw)}</article>'
        out.write_text(shell(item['title'],body,'../../'),encoding='utf-8')
        cards.append(f'<a class="card" data-course="{c}" data-search="{E(" ".join([item["title"],item["description"],COURSES[c],item["chapter"]]),quote=True)}" href="notes/{c}/{s}.html"><div class="eyebrow">{E(COURSES[c])} · {E(item["chapter"])}</div><h2>{E(item["title"])}</h2><p>{E(item["description"])}</p><span class="more">閱讀筆記 →</span></a>')
    controls=''.join(f'<button data-filter="{c}" type="button" aria-pressed="false">{E(label)}</button>' for c,label in COURSES.items())
    body=f'''<section class="hero"><p class="eyebrow">LEARN · REVIEW · GROW</p><h1>把每一堂課，<br>變成自己的知識。</h1><p class="lead">從課程講義出發，整理重要概念、公式與複習題。每一篇筆記都能追溯原始資料。</p><div class="stats"><span>{len(COURSES)} 門課程</span><span>{len(items)} 篇筆記</span><span>持續更新</span></div></section>
<section class="library"><h2>學習筆記</h2><label for="search">搜尋主題或關鍵字</label><input id="search" type="search" placeholder="例如：駐波、機率、信賴區間"><div class="filters"><button data-filter="all" type="button" aria-pressed="true">全部</button>{controls}</div><p id="count" aria-live="polite">顯示 {len(items)} 篇筆記</p><div class="cards">{"".join(cards)}</div><p id="empty" hidden>沒有符合的筆記，請試試其他關鍵字。</p></section><script src="assets/site.js"></script>'''
    (R/'index.html').write_text(shell('首頁',body),encoding='utf-8')
    (R/'wiki/index.md').write_text('# 知識庫索引\n\n'+'\n'.join(f'- [{i["title"]}]({i["course"]}/{i["slug"]}.md) — {COURSES[i["course"]]} {i["chapter"]}' for i in items)+'\n',encoding='utf-8')
    print(f'已生成首頁與 {len(items)} 篇筆記')
if __name__=='__main__': build()
