import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import zipfile

import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/jskills'
SOURCE = json.loads((PLUGIN / 'sources.json').read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate_sources():
    expected_names = {item['name'] for item in SOURCE['skills']}
    actual_names = {path.name for path in (PLUGIN / 'skills').iterdir()}
    if actual_names != expected_names:
        raise ValueError('Skill selection differs from audited source manifest')
    forbidden = re.compile(r'/Users/[A-Za-z0-9_.-]+/|/home/[A-Za-z0-9_.-]+/|github_pat_|gh[pousr]_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
    for skill in SOURCE['skills']:
        folder = PLUGIN / 'skills' / skill['name']
        actual = {}
        for path in sorted(folder.rglob('*')):
            if path.is_symlink():
                raise ValueError('Original skill folders must contain no symlinks')
            if path.is_file():
                data = path.read_bytes()
                if forbidden.search(data.decode('utf-8')):
                    raise ValueError(f'Private content indicator in {skill["name"]}/{path.name}')
                actual[str(path.relative_to(folder))] = digest(data)
        if actual != skill['sha256']:
            raise ValueError(f'Original files changed or supporting files missing: {skill["name"]}')
    expected_files = {'sources.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json'} | set(SOURCE['licenses'])
    for skill in SOURCE['skills']:
        expected_files.update('skills/' + skill['name'] + '/' + name for name in skill['sha256'])
    actual_files = set()
    if PLUGIN.is_symlink():
        raise ValueError('Package root must not be a symlink')
    for path in PLUGIN.rglob('*'):
        if path.is_symlink():
            raise ValueError('Package must contain no symlinks')
        if path.is_file():
            actual_files.add(str(path.relative_to(PLUGIN)))
            if forbidden.search(path.read_text()):
                raise ValueError('Private content indicator in package metadata')
    if actual_files != expected_files:
        raise ValueError('Package contains unexpected or missing files')
    for name, expected in SOURCE['licenses'].items():
        if digest((PLUGIN / name).read_bytes()) != expected:
            raise ValueError('Original MIT notice changed or is missing')
    return expected_files


def archive(path, entries, executable_names=()):
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED) as bundle:
        for name, data in sorted(entries.items()):
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (0o100755 if name in executable_names else 0o100644) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(entry, data)


def version_assets(text, output):
    for path in sorted(output.rglob('*')):
        if not path.is_file():
            continue
        relative = str(path.relative_to(output))
        version = digest(path.read_bytes())[:12]
        for url in [relative, 'https://pages.onul.me/jskills/' + relative]:
            for attribute in ['href', 'src']:
                text = text.replace(f'{attribute}="{url}"', f'{attribute}="{url}?v={version}"')
            text = text.replace(f']({url})', f']({url}?v={version})')
    return text


def build(output):
    allowed_files = validate_sources()
    output.mkdir(parents=True, exist_ok=False)
    downloads = output / 'downloads'
    downloads.mkdir()
    entries = {}
    executable_names = {'jskills/' + name for name in SOURCE['executable_files']}
    for relative in sorted(allowed_files):
        path = PLUGIN / relative
        name = 'jskills/' + relative
        entries[name] = path.read_bytes()
    archive(downloads / 'jskills.zip', entries, executable_names)
    links = []
    for skill in SOURCE['skills']:
        name = skill['name']
        prefix = 'jskills/skills/' + name + '/'
        files = {name + '/' + key[len(prefix):]: data for key, data in entries.items() if key.startswith(prefix)}
        files[name + '/LICENSE'] = (PLUGIN / skill['license']).read_bytes()
        archive(downloads / (name + '.zip'), files, {name + '/' + key[len(prefix):] for key in executable_names if key.startswith(prefix)})
        links.append(f'<a class="skill-download" href="downloads/{name}.zip" download>{html.escape(name)} <span>ZIP ↓</span></a>')
    for name in [*SOURCE['licenses'], 'sources.json']:
        shutil.copyfile(PLUGIN / name, downloads / name)
    checksums = ''.join(f'{digest(path.read_bytes())}  {path.name}\n' for path in sorted(downloads.glob('*.zip')))
    (downloads / 'SHA256SUMS.txt').write_text(checksums)
    known_skills = {skill['name'] for skill in SOURCE['skills']}
    shutil.copyfile(ROOT / 'site/jskills/style.css', output / 'style.css')
    shutil.copyfile(ROOT / 'site/jskills/tabs.js', output / 'tabs.js')
    download_html = '<section id="downloads" aria-labelledby="download-title"><div class="section-head"><h2 id="download-title">스킬 다운로드</h2><a href="downloads/SHA256SUMS.txt">SHA-256 확인</a></div><p>전체 ZIP 또는 필요한 스킬을 선택합니다.</p><div class="downloads">' + '\n'.join(links) + '</div><div class="download-notes"><a href="guide.md" download>가이드 Markdown 받기</a><a href="downloads/sources.json">출처와 파일 해시</a><a href="downloads/LICENSE">MIT license</a></div></section>'
    panels = []
    legacy = json.loads((ROOT / 'site/jskills/legacy-fragments.json').read_text())
    restored_fragments = set()
    guide_parts = []
    purposes = [
        ('mac', 'macos.md', 'macos-workflow.json', 'macOS 오디오 앱 개발', '음향 작업에 필요한 Mac 앱을 기획하고 구현하는 절차입니다. 인터뷰, TDD, 오디오 검증과 Native UI 리뷰를 함께 다룹니다.'),
        ('product', 'guide.md', 'workflow.json', 'AI 기반 제품 개발 가이드', '기획, 구현, 리뷰와 검증에 필요한 스킬을 작업 단계에 맞춰 사용합니다.'),
        ('installation', 'installation.md', None, '설치와 스킬', 'Codex와 Claude Code에서 사용할 플러그인과 스킬 ZIP, 설치 방법을 확인합니다.'),
    ]
    for purpose, filename, workflow_file, title, description in purposes:
        guide = (ROOT / 'site/jskills' / filename).read_text()
        diagram_html, diagram_md = '', ''
        if workflow_file:
            workflow = json.loads((ROOT / 'site/jskills' / workflow_file).read_text())
            nodes, mermaid = [], ['flowchart TD']
            for index, phase in enumerate(workflow, 1):
                if not set(phase['skills']).issubset(known_skills):
                    raise ValueError('Workflow names an unavailable skill')
                names = ', '.join(phase['skills'])
                nodes.append(f'<li><span class="phase-number">{index:02d}</span><h3>{html.escape(phase["title"])}</h3><p>{html.escape(names)}</p></li>')
                mermaid.append(f'  N{index}["{phase["title"]}<br/>{names}"]')
                if index > 1:
                    mermaid.append(f'  N{index - 1} --> N{index}')
            mermaid.extend(['  N5 -- "오류 수정" --> N4', '  N6 -- "확인된 지적 수정" --> N4'])
            diagram_md = '```mermaid\n' + '\n'.join(mermaid) + '\n```'
            diagram_html = '<div class="workflow" aria-label="개발 단계와 사용하는 스킬"><ol class="workflow-steps">' + ''.join(nodes) + '</ol><p class="workflow-return">검증이나 리뷰에서 확인한 문제를 수정한 뒤 다시 검증합니다.</p></div>'
        md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'], extension_configs={'toc': {'permalink': False, 'slugify': lambda value, separator, prefix=purpose: prefix + '-' + slugify_unicode(value, separator)}})
        content = md.convert(guide).replace('<!-- workflow-diagram -->', diagram_html).replace('<!-- skill-downloads -->', download_html)
        content = re.sub(r'<h1[^>]*>.*?</h1>', '', content, count=1)
        for alias, target in legacy.items():
            marker = f'<h([2-6]) id="{re.escape(target)}"'
            content, count = re.subn(marker, lambda match: f'<span id="{html.escape(alias, quote=True)}" class="fragment-alias" aria-hidden="true"></span>' + match.group(0), content, count=1)
            if count:
                restored_fragments.add(alias)
        toc = re.sub(r'<li><a href="#[^"]+">[^<]+</a>\s*<ul>', '<li><ul>', md.toc, count=1)
        hero_id = ' id="jskills"' if purpose == 'product' else ''
        panels.append(f'<section id="purpose-{purpose}" data-purpose="{purpose}" aria-labelledby="tab-{purpose}"><div class="hero"><div class="eyebrow">CODEX / CLAUDE CODE</div><h1{hero_id}>{title}</h1><p>{description}</p><div class="actions"><a class="primary" href="downloads/jskills.zip" download>전체 스킬 ZIP 받기 <span aria-hidden="true">↓</span></a><a class="secondary" href="#purpose-installation">설치 방법 보기 →</a></div></div><div class="guide-layout"><aside aria-label="{title} 목차">{toc}</aside><article>{content}</article></div></section>')
        portable = guide.replace('<!-- workflow-diagram -->', diagram_md).replace('<!-- skill-downloads -->', '[전체 스킬 ZIP](https://pages.onul.me/jskills/downloads/jskills.zip)')
        portable = re.sub(r'\[([^]]+)\]\(#purpose-(?:mac|product|installation)\)', r'\1', portable)
        guide_parts.append(portable)
    if restored_fragments != set(legacy):
        raise ValueError('A published guide fragment has no destination')
    (output / 'guide.md').write_text(version_assets('\n\n'.join(guide_parts), output))
    page = (ROOT / 'site/jskills/template.html').read_text().replace('{{PANELS}}', '\n'.join(panels))
    (output / 'index.html').write_text(version_assets(page, output))
    print(f'Built {output}: guide, full bundle, {len(SOURCE["skills"])} individual archives, source hashes and license')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / '.tmp/jskills-site')
    args = parser.parse_args()
    build(args.output)
