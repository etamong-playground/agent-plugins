import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
(root / '.tmp').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='client-smoke-', dir=root / '.tmp') as work:
    work = Path(work)
    source = work / 'marketplace'
    shutil.copytree(root, source, ignore=shutil.ignore_patterns('.git', '.tmp', '__pycache__'))
    catalog = json.loads((source / 'catalog.json').read_text())
    remote = 'https://marketplace-qualification.invalid/catalog.git'
    git_config = work / 'gitconfig'
    git_config.write_text('[core]\n\thooksPath = /dev/null\n[url "' + source.as_uri() + '"]\n\tinsteadOf = ' + remote + '\n[protocol "file"]\n\tallow = always\n')
    template = work / 'empty-template'
    template.mkdir()
    git_env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    git_env.update(GIT_CONFIG_GLOBAL=str(git_config), GIT_CONFIG_NOSYSTEM='1', GIT_TEMPLATE_DIR=str(template))
    subprocess.run(['git', 'init', '--initial-branch=main', str(source)], env=git_env, check=True, capture_output=True)

    def commit_fixture():
        subprocess.run(['git', '-C', str(source), 'add', '.'], env=git_env, check=True)
        subprocess.run(['git', '-C', str(source), '-c', 'user.name=Package qualification',
                        '-c', 'user.email=qualification@example.invalid', '-c', 'commit.gpgsign=false',
                        'commit', '-m', 'test: update marketplace fixture'], env=git_env, check=True, capture_output=True)

    commit_fixture()
    clients = {}
    for client in ['codex', 'claude']:
        profile = work / client
        profile.mkdir(mode=0o700)
        env = dict(git_env)
        env['CODEX_HOME' if client == 'codex' else 'CLAUDE_CONFIG_DIR'] = str(profile)
        env.update(CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='1', DISABLE_AUTOUPDATER='1')
        clients[client] = (profile, env)

    def run(client, args):
        profile, env = clients[client]
        result = subprocess.run([client] + args, env=env, cwd=profile, capture_output=True, text=True, timeout=45)
        if result.returncode:
            raise RuntimeError(result.stderr or result.stdout)
        return result.stdout

    run('codex', ['plugin', 'marketplace', 'add', remote, '--json'])
    run('claude', ['plugin', 'validate', str(source)])
    run('claude', ['plugin', 'marketplace', 'add', remote, '--scope', 'user'])
    for upgrading in [False, True]:
        if upgrading:
            for service in catalog['plugins']:
                major, minor, patch = map(int, service['version'].split('.'))
                service['version'] = f'{major}.{minor}.{patch + 1}'
            (source / 'catalog.json').write_text(json.dumps(catalog, indent=2) + '\n')
            subprocess.run([sys.executable, str(source / 'scripts/generate.py')], check=True)
            commit_fixture()
            run('codex', ['plugin', 'marketplace', 'upgrade', catalog['name'], '--json'])
            run('claude', ['plugin', 'marketplace', 'update', catalog['name']])
        for service in catalog['plugins']:
            selector = service['name'] + '@' + catalog['name']
            run('codex', ['plugin', 'add', selector, '--json'])
            run('claude', ['plugin', 'update' if upgrading else 'install', selector, '--scope', 'user'])
        for client in clients:
            result = json.loads(run(client, ['plugin', 'list', '--json']))
            installed = result['installed'] if client == 'codex' else result
            for service in catalog['plugins']:
                selector = service['name'] + '@' + catalog['name']
                entry = next(item for item in installed if item.get('pluginId', item.get('id')) == selector)
                assert entry['enabled'] and entry['version'] == service['version'], (client, selector)
                if client == 'claude':
                    connection = entry['mcpServers'][service['name']]
                    assert connection['type'] == 'stdio' and connection['command'] == service['claudeAdapter']['command']
                    assert connection['env'][service['claudeAdapter']['originEnv']] == service['resource']
            print(client + (' upgrade' if upgrading else ' installation') + ' verified')
print('Client smoke checks passed without user OAuth grants or model calls')
