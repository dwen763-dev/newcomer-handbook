# 生成《新人办事说明书》PDF：封面 → 使用说明 → 目录 → 各章（docs/ 下按章节顺序）→ 封底（抖音引流）
# 用法：python tools/build_pdf.py   （需要 pip install markdown；打印用 Playwright 的 Chromium，路径由环境变量 CHROME 指定）
import os, re, glob, json, subprocess, datetime
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_HTML = os.path.join(ROOT, 'downloads', 'source', '新人办事说明书.html')
OUT_PDF = os.path.join(ROOT, 'downloads', '新人办事说明书.pdf')
DOUYIN = '抖音 @牧林Mlin'
CFG = json.load(open(os.path.join(ROOT, 'project.json'), encoding='utf-8'))

def md(text):
    return markdown.markdown(text, extensions=['tables', 'sane_lists'])

def chapter_files():
    files = []
    for ch in CFG['chapters']:
        for page in ch['pages']:
            files.append((ch['title'], os.path.join(ROOT, 'docs', page)))
    return files

CSS = '''
@page { size: A4; margin: 18mm 16mm 20mm; }
* { box-sizing: border-box; }
body { font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif; color: #141414; font-size: 11pt; line-height: 1.75; }
h1 { font-size: 22pt; border-bottom: 3pt solid #141414; padding-bottom: 6pt; margin: 0 0 12pt; page-break-before: always; }
h2 { font-size: 15pt; margin: 18pt 0 8pt; padding-left: 8pt; border-left: 5pt solid #FF5A1F; }
h3 { font-size: 12.5pt; margin: 14pt 0 6pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0 12pt; font-size: 10.5pt; }
th { background: #141414; color: #fff; text-align: left; padding: 6pt 8pt; }
td { border-bottom: 1pt solid #c9c4b8; padding: 6pt 8pt; vertical-align: top; }
blockquote { margin: 8pt 0; padding: 6pt 12pt; background: #F6F4EE; border-left: 4pt solid #c9c4b8; color: #333; }
strong { color: #C2410C; }
hr { border: none; border-top: 1pt dashed #c9c4b8; margin: 16pt 0; }
.cta { margin: 14pt 0 0; padding: 10pt 14pt; background: #FFF1EA; border: 1.5pt solid #FF5A1F; font-weight: 700; }
.cover { page-break-after: always; height: 257mm; position: relative; background: #F6F4EE; margin: -18mm -16mm 0; padding: 26mm 20mm; }
.cover .brand { font-size: 42pt; font-weight: 900; letter-spacing: 2pt; line-height: 1.15; }
.cover .sub { font-size: 14pt; color: #555; margin-top: 10pt; }
.cover .bar { height: 5pt; background: #141414; margin: 18pt 0; }
.cover .big { font-size: 26pt; font-weight: 900; line-height: 1.4; }
.cover .big span { color: #FF5A1F; }
.cover .tags span { display: inline-block; border: 2pt solid #141414; padding: 3pt 10pt; margin: 0 6pt 8pt 0; font-weight: 900; background: #fff; }
.cover .dy { position: absolute; left: 20mm; right: 20mm; bottom: 26mm; background: #141414; color: #fff; padding: 14pt 18pt; font-size: 15pt; font-weight: 900; }
.cover .dy b { color: #FF5A1F; }
.cover .meta { position: absolute; left: 20mm; bottom: 14mm; font-size: 9pt; color: #777; }
.toc li { margin: 4pt 0; }
.back { page-break-before: always; text-align: center; padding-top: 60mm; }
.back .big { font-size: 24pt; font-weight: 900; }
.back .dy { display: inline-block; margin-top: 20pt; background: #FF5A1F; color: #fff; font-size: 20pt; font-weight: 900; padding: 12pt 24pt; }
'''

def build():
    today = datetime.date.today().isoformat()
    parts = [f'''<section class="cover">
<div class="brand">新人办事说明书</div><div class="sub">给应届生和职场新人：第一次办事，也能一次办对</div><div class="bar"></div>
<div class="big">签合同 · 试用期 · 工资社保<br>个税 · 租房 · 离职<br><span>每条都写明官方出处和核实日期</span></div>
<div class="tags" style="margin-top:18pt">{''.join(f'<span>{c["title"]}</span>' for c in CFG["chapters"])}</div>
<div class="dy">📺 视频版在 <b>{DOUYIN}</b> · 搜索「新人办事说明书」</div>
<div class="meta">版本 {today} · 文字内容采用 CC BY-NC-SA 4.0 · 仅供参考，不构成法律意见</div></section>''']
    guide = open(os.path.join(ROOT, '核实规则.md'), encoding='utf-8').read()
    parts.append('<h1>使用说明</h1>' + md('''- 每个主题先给**"照着做"清单或对照表**，可以直接截图。
- 每页末尾有**依据**：法律法规名称、条款号、原文摘录、核实日期。
- 各地不同的内容（最低工资、社保基数、公积金比例等）写明"各地不同"，并告诉你去哪查本地标准。
- 本说明书为普法科普，仅供参考，不构成法律意见。遇到纠纷可咨询当地劳动人事争议仲裁委员会，或拨打 12333。''')
                 + md(guide.replace('# 核实规则', '## 核实规则')) + f'<div class="cta">📺 每个主题都有视频版：{DOUYIN}</div>')
    toc = '<h1>目录</h1><ol class="toc">'
    for ch in CFG['chapters']:
        toc += f'<li><b>{ch["title"]}</b><ul>' + ''.join(f'<li>{p["title"]}</li>' for p in ch.get('page_meta', [])) + '</ul></li>'
    toc += '</ol>'
    parts.append(toc)
    for _, f in chapter_files():
        text = open(f, encoding='utf-8').read()
        text = re.sub(r'\]\((?!http)[^)]*\)', ']', text)                 # 去掉仓库内相对链接（PDF 里没法点）
        parts.append(md(text) + f'<div class="cta">📺 看视频版：{DOUYIN} · 新人办事说明书</div>')
    parts.append(f'<section class="back"><div class="big">第一次办事，先查说明书。</div><div class="dy">关注 {DOUYIN}</div>'
                 f'<p style="margin-top:24pt;color:#666">文字版持续更新：GitHub「新人办事说明书」 · 发现错误欢迎附官方出处提 Issue</p></section>')
    html = f'<!doctype html><html><head><meta charset="utf-8"><title>新人办事说明书</title><style>{CSS}</style></head><body>{"".join(parts)}</body></html>'
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    open(OUT_HTML, 'w', encoding='utf-8').write(html)
    subprocess.run(['node', os.path.join(ROOT, 'tools', 'print_pdf.cjs'), OUT_HTML, OUT_PDF], check=True)
    print('PDF ->', OUT_PDF)

if __name__ == '__main__':
    build()
