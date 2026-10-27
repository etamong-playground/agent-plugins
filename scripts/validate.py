import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / 'scripts/generate.py'), '--check'], check=True)
catalog = json.loads((root / 'catalog.json').read_text())
for path in root.rglob('*'):
    relative = path.relative_to(root)
    if any(part in {'.git', '.tmp', '__pycache__'} for part in relative.parts):
        continue
    if path.is_symlink():
        raise SystemExit(f'Package symlinks require an explicit review: {relative}')
    if not path.is_file():
        continue
    text = path.read_text()
    if re.search(r'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}|sk-(?:ant-)?[A-Za-z0-9_-]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', text):
        raise SystemExit(f'Credential-shaped content in {relative}')
    if path.suffix == '.json':
        data = json.loads(text)
        def check(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key.lower().replace('_', '').replace('-', '') in {'clientsecret', 'accesstoken', 'refreshtoken', 'authorization', 'pagestoken'}:
                        raise SystemExit(f'Credential field in {relative}')
                    check(item)
            elif isinstance(value, list):
                for item in value:
                    check(item)
        check(data)

for service in catalog['plugins']:
    plugin = root / 'plugins' / service['name']
    if (plugin / 'plugin.json').exists() or (plugin / 'mcp.json').exists():
        raise SystemExit('Portable root metadata would shadow the qualified Codex OAuth adapter')
    manifest = json.loads((plugin / '.codex-plugin/plugin.json').read_text())
    for field in ['skills', 'mcpServers']:
        target = (plugin / manifest[field]).resolve()
        if not target.is_relative_to(plugin.resolve()) or not target.exists():
            raise SystemExit(f'Plugin component path escapes or is missing: {service["name"]}/{field}')
    skills = list((plugin / 'skills').glob('*/SKILL.md'))
    if not skills:
        raise SystemExit(f'No shared service skills: {service["name"]}')
    for skill in skills:
        text = skill.read_text()
        if not text.startswith('---\n') or '\nname: ' not in text or '\ndescription: ' not in text:
            raise SystemExit(f'Invalid skill frontmatter: {skill.relative_to(root)}')
    native = json.loads((plugin / '.mcp.codex.json').read_text())['mcpServers'][service['name']]
    if service.get('codexAdapter'):
        if native['type'] != 'stdio' or not manifest.get('requires_local_executor'):
            raise SystemExit('Device connections require a local stdio executor')
        if any(key in native for key in ['oauth', 'oauth_resource', 'url', 'scopes']):
            raise SystemExit('Device connections cannot include a native authorization-code adapter')
    elif native['oauth']['clientId'] != service['clientId'] or native['oauth_resource'] != service['resource']:
        raise SystemExit('Native OAuth client/resource binding is missing')
    if service['name'] == 'pages' and not {'pages:read', 'pages:write'}.issubset(service['scopes']):
        raise SystemExit('Pages read/write permissions are missing')
    if 'offline_access' not in service['scopes']:
        raise SystemExit('Native OAuth offline access is missing')
    adapter = json.loads((plugin / '.mcp.json').read_text())['mcpServers'][service['name']]
    expected_env = {service['claudeAdapter']['originEnv']: service['resource']} if service['claudeAdapter'].get('originEnv') else {}
    if adapter['type'] != 'stdio' or adapter.get('env', {}) != expected_env:
        raise SystemExit('Claude requires an explicitly bound local adapter')
    ordinary_services = {
        'scheduler': ('https://scheduler-api.onul.me', 'scheduler', 'scheduler:read'),
        'sports-calendar': ('https://sports-calendar.onul.me', 'sports', 'sports:read'),
    }
    if service['name'] in ordinary_services:
        resource, command, read_scope = ordinary_services[service['name']]
        expected_scopes = {'openid', 'profile', 'email', 'offline_access', read_scope}
        if service['resource'] != resource or set(service['scopes']) != expected_scopes:
            raise SystemExit('Device services require their ordinary resource and read-only scopes')
        if manifest['interface']['capabilities'] != ['Read']:
            raise SystemExit('Device services advertise read capabilities only')
        for connection in [native, adapter]:
            if connection != {'type': 'stdio', 'command': command, 'args': ['mcp']}:
                raise SystemExit('Device services require their fixed ordinary adapters')
print('Public metadata, contained component paths, credential exclusions and client bindings validated')
