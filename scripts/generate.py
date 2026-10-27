import argparse
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


def stdio_connection(adapter, resource):
    connection = {'type': 'stdio', 'command': adapter['command'], 'args': adapter['args']}
    if not isinstance(adapter['command'], str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', adapter['command']):
        raise ValueError('Local adapter command must be a program name')
    if not isinstance(adapter['args'], list) or any(not isinstance(arg, str) or '\n' in arg for arg in adapter['args']):
        raise ValueError('Local adapter arguments must be separate strings')
    if adapter.get('originEnv'):
        connection['env'] = {adapter['originEnv']: resource}
    return connection


def generate(root):
    catalog = json.loads((root / 'catalog.json').read_text())
    codex = {'name': catalog['name'], 'interface': {'displayName': catalog['displayName']}, 'plugins': []}
    claude = {'name': catalog['name'], 'owner': {'name': catalog['owner']}, 'metadata': {'description': catalog['description']}, 'plugins': []}
    files = {}
    seen = set()
    for service in catalog['plugins']:
        name = service['name']
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', name) or name in seen:
            raise ValueError('Service names must be unique plugin identifiers')
        seen.add(name)
        if not re.fullmatch(r'\d+\.\d+\.\d+', service['version']):
            raise ValueError('Service versions must use major.minor.patch')
        resource = urlsplit(service['resource'])
        if resource.scheme != 'https' or not resource.netloc or resource.username or resource.password or resource.path or resource.query or resource.fragment:
            raise ValueError('Service resources must be canonical HTTPS origins')
        if service['endpoint'] != service['resource'] + '/mcp':
            raise ValueError('Service endpoint must use its canonical resource origin')
        if not (root / 'plugins' / name / 'skills').is_dir():
            raise ValueError('Service skill tree is missing')
        common = {'name': name, 'version': service['version'], 'description': service['description'],
                  'author': {'name': catalog['owner']}, 'homepage': service['homepage'], 'repository': catalog['repository']}
        codex_manifest = {**common, 'skills': './skills/', 'mcpServers': './.mcp.codex.json',
                          'interface': {'displayName': service['displayName'], 'shortDescription': service['description'],
                                        'longDescription': service['description'], 'developerName': catalog['owner'],
                                        'category': 'Productivity', 'capabilities': service.get('capabilities', ['Read', 'Write']),
                                        'defaultPrompt': [service['defaultPrompt']]}}
        base = f'plugins/{name}/'
        files[base + '.codex-plugin/plugin.json'] = codex_manifest
        files[base + '.claude-plugin/plugin.json'] = common
        if service.get('codexAdapter'):
            codex_manifest['requires_local_executor'] = True
            native = stdio_connection(service['codexAdapter'], service['resource'])
        else:
            native = {'type': 'http', 'url': service['endpoint'], 'oauth': {'clientId': service['clientId']},
                      'oauth_resource': service['resource'], 'scopes': service['scopes']}
        files[base + '.mcp.codex.json'] = {'mcpServers': {name: native}}
        files[base + '.mcp.json'] = {'mcpServers': {name: stdio_connection(service['claudeAdapter'], service['resource'])}}
        codex['plugins'].append({'name': name, 'source': {'source': 'local', 'path': './plugins/' + name},
                                 'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'}, 'category': 'Productivity'})
        claude['plugins'].append({'name': name, 'source': './plugins/' + name,
                                  'version': service['version'], 'description': service['description']})
    files['.agents/plugins/marketplace.json'] = codex
    files['.claude-plugin/marketplace.json'] = claude
    return {path: json.dumps(value, indent=2, ensure_ascii=False) + '\n' for path, value in files.items()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    for relative, content in generate(root).items():
        path = root / relative
        if args.check:
            if not path.is_file() or path.read_text() != content:
                raise SystemExit(f'Generated metadata differs: {relative}; run python3 scripts/generate.py')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print('Generated client metadata is current' if args.check else 'Generated client manifests and marketplaces')


if __name__ == '__main__':
    main()
