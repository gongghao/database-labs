"""Build only released course content for the GitHub Pages artifact."""
from pathlib import Path
from datetime import datetime, timezone
import html, json, shutil
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://gongghao.github.io/database-labs/'

def parse_time(value):
    if value is None: return None
    result = datetime.fromisoformat(value)
    if result.tzinfo is None: raise ValueError('All course times must include a timezone offset')
    return result

def is_released(project, now):
    if now.tzinfo is None: raise ValueError('Build time must be timezone-aware')
    release = parse_time(project['release_at'])
    return release is not None and now >= release

def display_time(value):
    return parse_time(value).strftime('%Y-%m-%d %H:%M') if value else '待通知'

def page(title, body, projects, current='home', prefix=''):
    nav = f'<a class="project {"active" if current == "home" else ""}" href="{prefix}index.html"><span>◫</span><div>实验安排<small>课程首页</small></div></a>'
    nav += f'<a class="project {"active" if current == "preparation" else ""}" href="{prefix}preparation.html"><span>00</span><div>实验准备<small>现在开放</small></div></a>'
    nav += '<div class="nav-label">PROJECTS</div>'
    for p in projects:
        n=p['id']; active=' active' if current==n else ''
        label='已开放' if p['_released'] else '未开放'
        nav += f'<a class="project{active}" href="{prefix}projects/project{n}/index.html"><span>{n:02}</span><div>{html.escape(p["title"])}<small>Project {n} · {label}</small></div></a>'
    favicon="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%232c4fea'/%3E%3Cpath d='M9 10h14v4H9zm0 8h14v4H9z' fill='white'/%3E%3C/svg%3E"
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="数据库实验课：实验准备、六次 Project 的教程与资料，按课程安排开放。"><title>{html.escape(title)} · DB Lab</title><link rel="icon" href="{favicon}"><link rel="stylesheet" href="{prefix}assets/style.css"></head><body><a class="skip" href="#main">跳转到正文</a><aside class="sidebar"><a class="brand" href="{prefix}index.html"><span class="brand-icon">DB</span><span>数据库实验课<small>DATABASE LAB</small></span></a><nav aria-label="课程导航">{nav}</nav><div class="sidebar-bottom"><span class="mini-label">2026 · 秋季学期</span><p>所有日期均为北京时间<br>Asia / Shanghai</p></div></aside><div class="page"><header class="topbar"><span>实验手册 <span class="slash">/</span> {html.escape(title)}</span><a href="{prefix}index.html">实验安排</a></header><main id="main">{body}<footer><span>DB LAB / 数据库实验课</span><span>提交渠道以本学期通知为准</span></footer></main></div></body></html>'''

def download_section(n, assets):
    links=[]
    for p in sorted(assets.iterdir()):
        if not p.is_file(): continue
        size=f'{p.stat().st_size/1024/1024:.1f} MB' if p.stat().st_size>=1048576 else f'{p.stat().st_size/1024:.1f} KB'
        links.append(f'<a class="download-card" href="materials/{quote(p.name)}" download><span class="file-icon">{p.suffix[1:].upper()}</span><div><h3>{html.escape(p.name)}</h3><p>{size} · 下载</p></div><span aria-hidden="true">↓</span></a>')
    return '<section class="section" id="resources"><div class="eyebrow">COURSE MATERIALS</div><h2>资料下载</h2><p>课件与示例保留原始内容，其中历史日期与邮箱不适用于本学期。</p><div class="download-grid">'+''.join(links)+'</div></section>'

def build(output=None, now=None):
    now=now or datetime.now(timezone.utc)
    output=Path(output or ROOT/'_site').resolve()
    # Never let cleanup target source files, the repository or unrelated paths.
    if output == ROOT or ROOT in output.parents and output.parts[len(ROOT.parts)] not in ('_site','.local'):
        raise ValueError('Unsafe output directory')
    if output.exists(): shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(ROOT/'public/assets',output/'assets')
    config=json.loads((ROOT/'config/course.json').read_text())
    projects=config['projects']
    for p in projects:
        parse_time(p['deadline']); p['_released']=is_released(p,now)
    cards=[]
    for p in projects:
        n=p['id']; released=p['_released']; label='已开放' if released else '未开放'
        deadline=parse_time(p['deadline'])
        if released and deadline and now >= deadline: label='提交已截止 · 可复习'
        cards.append(f'''<article class="course-card {"available" if released else "locked"}"><div class="card-top"><span class="eyebrow">PROJECT {n:02}</span><span class="status">{label}</span></div><h2>{html.escape(p['title'])}</h2><p>{html.escape(p['summary'])}</p><dl><div><dt>发布日期</dt><dd>{display_time(p['release_at'])}</dd></div><div><dt>提交截止</dt><dd>{display_time(p['deadline'])}</dd></div></dl><a class="button {"primary" if released else "secondary"}" href="projects/project{n}/index.html">{"进入实验" if released else "查看开放安排"} <span aria-hidden="true">↗</span></a></article>''')
        dest=output/f'projects/project{n}'; dest.mkdir(parents=True)
        if not released:
            release_text=f"将于 {display_time(p['release_at'])} 开放" if p['release_at'] else '发布日期待通知'
            body=f'''<section class="intro locked-intro"><div class="lock-icon" aria-hidden="true">⌑</div><div class="eyebrow">PROJECT {n:02} · 未开放</div><h1>{html.escape(p['title'])}</h1><p class="lead">{release_text}（北京时间）。<br>开放前暂不提供实验题目、教程和资料下载。</p><div class="release-info"><p><strong>发布日期</strong> {display_time(p['release_at'])}</p><p><strong>提交截止</strong> {display_time(p['deadline'])}</p></div><div class="actions"><a class="button primary" href="../../preparation.html">先完成实验准备</a><a class="button secondary" href="../../index.html">返回实验安排</a></div></section>'''
        else:
            source=ROOT/f'content/projects/project{n}'
            if n == 1 and not source.exists():
                source=ROOT/'docs/projects/project1'  # Previously published originals.
            shutil.copytree(source,dest,dirs_exist_ok=True)
            intro=f'''<section class="intro"><div class="eyebrow">PROJECT {n:02} · 已开放</div><h1>{html.escape(p['title'])}</h1><p class="lead">{html.escape(p['summary'])}</p><div class="facts"><div><span>实验环境</span><strong>{html.escape(p['environment'])}</strong></div><div><span>发布日期</span><strong>{display_time(p['release_at'])}</strong></div><div><span>提交截止（北京时间）</span><strong>{display_time(p['deadline'])}</strong></div></div></section>'''
            notice='<div class="notice"><span class="notice-label">提交说明</span><p>'
            if n==1: notice+='截止时间为 2026 年 10 月 19 日 00:00，即请在 10 月 18 日结束前提交。'
            else: notice+='提交时间以本页课程安排为准。'
            if deadline and now>=deadline: notice+=' 提交已截止，教程和资料仍可用于复习。'
            notice+='提交邮箱 / 平台以本学期通知为准；原课件的历史日期不适用。</p></div>'
            content=(ROOT/f'content/project{n}.html').read_text()
            content=content.replace(f'projects/project{n}/','')
            if n==1:
                content=content.replace('以下文件组织方式来自原始课件；邮箱、截止日期及最终要求以本学期通知为准。','提交截止时间见上方本学期安排；以下文件组织方式来自原始课件，提交邮箱 / 平台待通知。')
                # General environment setup belongs to the preparation page.
                import re
                content=re.sub(r'<article class="lesson" id="step1">.*?</article>', '<article class="lesson" id="step1"><div class="lesson-title"><span class="step-number">01</span><h3>创建 University 数据库</h3></div><p>先完成<a href="../../preparation.html">实验准备</a>。下载并解压本页数据包，在 Access 中选择“文件 → 新建 → 空白数据库”，保存为 <code>university_A1.accdb</code>。进入“创建 → 表设计”，开始定义数据表。</p></article>', content, flags=re.S)
            else: content+=download_section(n,dest/'materials')
            body=intro+notice+content
        (dest/'index.html').write_text(page(f'Project {n}',body,projects,n,'../../'))
    body='''<section class="intro"><div class="eyebrow">2026 FALL · DATABASE LAB</div><h1>数据库实验课</h1><p class="lead">实验准备与六次 Project，按课程进度依次开放。</p><div class="prep-banner"><div><span class="eyebrow">START HERE</span><h2>实验准备</h2><p>配置软件环境，建立实验目录，了解报告要求。</p></div><a class="button primary" href="preparation.html">现在开始 ↗</a></div></section><div class="notice"><span class="notice-label">课程安排</span><p>Project 1 于 10 月 5 日 00:00 开放，10 月 19 日 00:00 截止（10 月 18 日结束前提交）。其余 Project 日期待通知。所有时间均为北京时间。</p></div><section class="section"><div class="section-heading"><div><div class="eyebrow">PROJECTS</div><h2>实验安排</h2></div><span class="section-note">未开放的实验暂不提供题目与下载</span></div><div class="course-grid">'''+''.join(cards)+'</div></section>'
    (output/'index.html').write_text(page('实验安排',body,projects))
    (output/'preparation.html').write_text(page('实验准备',(ROOT/'content/preparation.html').read_text(),projects,'preparation'))
    (output/'404.html').write_text(f'<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>资料尚未开放 · DB Lab</title><body><h1>资料尚未开放或不存在</h1><p>实验资料按发布日期提供，请从课程首页查看安排。</p><a href="{BASE_URL}">返回实验安排</a></body></html>')
    (output/'.nojekyll').touch()
    return [p['id'] for p in projects if p['_released']]

if __name__=='__main__':
    print('Published project IDs:',build())
