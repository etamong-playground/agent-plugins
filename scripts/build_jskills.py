import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import zipfile

import markdown

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
            text = text.replace(f'href="{url}"', f'href="{url}?v={version}"')
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
    guide = (ROOT / 'site/jskills/guide.md').read_text()
    workflow = json.loads((ROOT / 'site/jskills/workflow.json').read_text())
    known_skills = {skill['name'] for skill in SOURCE['skills']}
    nodes = []
    mermaid = ['flowchart TD']
    for index, phase in enumerate(workflow, 1):
        if not set(phase['skills']).issubset(known_skills):
            raise ValueError('Workflow names an unavailable skill')
        names = ', '.join(phase['skills'])
        nodes.append(f'<li><span class="phase-number">{index:02d}</span><h3>{html.escape(phase["title"])}</h3><p>{html.escape(names)}</p></li>')
        mermaid.append(f'  N{index}["{phase["title"]}<br/>{names}"]')
        if index > 1:
            mermaid.append(f'  N{index - 1} --> N{index}')
    mermaid.extend(['  N5 -- "오류 수정" --> N4', '  N6 -- "확인된 지적 수정" --> N4'])
    markdown_diagram = '```mermaid\n' + '\n'.join(mermaid) + '\n```'
    shutil.copyfile(ROOT / 'site/jskills/style.css', output / 'style.css')
    (output / 'guide.md').write_text(version_assets(guide.replace('<!-- workflow-diagram -->', markdown_diagram), output))
    workflow_html = '<div class="workflow" aria-label="제품 개발 단계와 사용하는 스킬"><ol class="workflow-steps">' + ''.join(nodes) + '</ol><p class="workflow-return">검증 또는 리뷰에서 수정할 내용이 확인되면 구현 단계로 돌아가고, 수정 후에는 다시 검증합니다.</p></div>'
    md = markdown.Markdown(extensions=['tables', 'fenced_code', 'toc'], extension_configs={'toc': {'permalink': False}})
    content = md.convert(guide).replace('<!-- workflow-diagram -->', workflow_html)
    content = re.sub(r'<h1[^>]*>.*?</h1>', '', content, count=1)
    page = (ROOT / 'site/jskills/template.html').read_text()
    page = page.replace('{{CONTENT}}', content).replace('{{TOC}}', md.toc).replace('{{DOWNLOADS}}', '\n'.join(links))
    (output / 'index.html').write_text(version_assets(page, output))
    print(f'Built {output}: guide, full bundle, {len(SOURCE["skills"])} individual archives, source hashes and license')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / '.tmp/jskills-site')
    args = parser.parse_args()
    build(args.output)
