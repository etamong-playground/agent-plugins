"""Build self-contained skill editions from the reviewed canonical inventory."""
import hashlib
import json
from pathlib import Path
import re


IDENTIFIER = re.compile(r'[a-z][a-z0-9-]{0,63}')


def editions(root):
    catalog = json.loads((root / 'catalog.json').read_text())
    config = catalog.get('skillPackages')
    if config is None:
        return {}
    canonical = config['canonical']
    if not IDENTIFIER.fullmatch(canonical):
        raise ValueError('Invalid canonical package name')
    source = root / 'plugins' / canonical
    if source.is_symlink() or (source / 'skills').is_symlink() or (source / 'sources.json').is_symlink():
        raise ValueError('Canonical package must not use symlinks')
    manifest = json.loads((source / 'sources.json').read_text())
    skills = {item['name']: item for item in manifest['skills']}
    if len(skills) != len(manifest['skills']) or any(not IDENTIFIER.fullmatch(n) for n in skills):
        raise ValueError('Invalid or duplicate canonical skill')
    if {p.name for p in (source / 'skills').iterdir()} != set(skills):
        raise ValueError('Canonical skill inventory differs from reviewed manifest')
    resources = {}
    for name, item in skills.items():
        folder = source / 'skills' / name
        entries = {}
        if folder.is_symlink():
            raise ValueError('Canonical skill must not be a symlink')
        for p in sorted(folder.rglob('*')):
            if p.is_symlink():
                raise ValueError('Canonical resources must not be symlinks')
            if p.is_file():
                entries[p.relative_to(folder).as_posix()] = p.read_bytes()
        if {k: hashlib.sha256(v).hexdigest() for k, v in entries.items()} != item['sha256']:
            raise ValueError('Canonical files differ from reviewed manifest: ' + name)
        resources[name] = entries
    categories = config['categories']
    selected = [n for names in categories.values() for n in names]
    if len(selected) != len(set(selected)) or set(selected) != set(skills):
        raise ValueError('Categories must partition canonical skills exactly once')
    legacy = config.get('legacy', {})
    packages = {name: (names, {}) for name, names in categories.items()}
    packages.update({name: (list(skills), aliases) for name, aliases in legacy.items()})
    configured = {p['name'] for p in catalog['plugins'] if p.get('kind') == 'skills'}
    if set(packages) | {canonical} != configured:
        raise ValueError('Skill package configuration and catalog differ')
    generated = {}
    licenses = {}
    for name, expected in manifest['licenses'].items():
        if Path(name).name != name or (source / name).is_symlink():
            raise ValueError('Invalid license path')
        data = (source / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError('Reviewed license changed')
        licenses[name] = data
    for package, (names, aliases) in packages.items():
        if not IDENTIFIER.fullmatch(package) or package == canonical:
            raise ValueError('Invalid generated package name')
        if not set(aliases).issubset(skills) or any(not IDENTIFIER.fullmatch(n) for n in aliases.values()):
            raise ValueError('Invalid legacy name mapping')
        exports = [aliases.get(n, n) for n in names]
        if len(exports) != len(set(exports)):
            raise ValueError('Duplicate exported skill')
        prefix = 'plugins/' + package + '/'
        edition = {**manifest, 'skills': [], 'executable_files': []}
        for name in names:
            exported = aliases.get(name, name)
            item = {**skills[name], 'name': exported, 'sha256': {}}
            for relative, data in resources[name].items():
                if relative == 'SKILL.md' and name != exported:
                    data = data.replace(('\nname: ' + name + '\n').encode(), ('\nname: ' + exported + '\n').encode(), 1)
                generated[prefix + 'skills/' + exported + '/' + relative] = data
                item['sha256'][relative] = hashlib.sha256(data).hexdigest()
            edition['skills'].append(item)
        for relative in manifest.get('executable_files', []):
            parts = relative.split('/')
            if len(parts) < 3 or parts[0] != 'skills' or parts[1] not in skills:
                raise ValueError('Invalid executable inventory')
            if parts[1] in names:
                parts[1] = aliases.get(parts[1], parts[1])
                edition['executable_files'].append('/'.join(parts))
        for name, data in licenses.items():
            generated[prefix + name] = data
        generated[prefix + 'sources.json'] = (json.dumps(edition, indent=2, ensure_ascii=False) + '\n').encode()
    return generated


def sync(root, check=False):
    expected = editions(root)
    managed = {Path(p).parts[1] for p in expected}
    for name in managed:
        folder = root / 'plugins' / name
        if folder.is_symlink():
            raise ValueError('Generated package must not be a symlink')
        for path in folder.rglob('*') if folder.exists() else []:
            if path.is_symlink():
                raise ValueError('Generated package must not contain symlinks')
            if path.is_file() and path.relative_to(folder).as_posix() not in {'.claude-plugin/plugin.json', '.codex-plugin/plugin.json'}:
                relative = path.relative_to(root).as_posix()
                if relative not in expected:
                    if check:
                        raise ValueError('Stale generated resource: ' + relative)
                    path.unlink()
        allowed_files = {p for p in expected if Path(p).parts[1] == name}
        allowed_files.update('plugins/' + name + '/' + p for p in ['.claude-plugin/plugin.json', '.codex-plugin/plugin.json'])
        allowed_directories = {parent for p in allowed_files for parent in Path(p).parents if parent != Path('.')}
        for path in sorted(folder.rglob('*'), key=lambda p: len(p.parts), reverse=True):
            if path.is_dir() and path.relative_to(root) not in allowed_directories:
                if check:
                    raise ValueError('Stale generated directory: ' + path.relative_to(root).as_posix())
                path.rmdir()
    for relative, data in expected.items():
        path = root / relative
        if check:
            if not path.is_file() or path.read_bytes() != data:
                raise ValueError('Generated skill edition differs: ' + relative)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
