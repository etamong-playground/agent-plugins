import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import queue
import re
import threading

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
    def discovered_codex():
        profile, env = clients['codex']
        messages = [
            {'jsonrpc': '2.0', 'id': 1, 'method': 'initialize', 'params': {'clientInfo': {'name': 'skill-qualification', 'version': '1'}}},
            {'jsonrpc': '2.0', 'method': 'initialized'},
            {'jsonrpc': '2.0', 'id': 2, 'method': 'skills/list', 'params': {'cwds': [str(profile)], 'forceReload': True}},
        ]
        process = subprocess.Popen(['codex', 'app-server'], env=env, cwd=profile,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        lines = queue.Queue()
        def read_stdout():
            for line in process.stdout:
                lines.put(line)
        threading.Thread(target=read_stdout, daemon=True).start()
        def send(message):
            process.stdin.write(json.dumps(message) + '\n')
            process.stdin.flush()
        def receive(identifier):
            while True:
                value = json.loads(lines.get(timeout=30))
                if value.get('id') == identifier:
                    if 'error' in value:
                        raise RuntimeError(value['error'])
                    return value
        try:
            send(messages[0])
            receive(1)
            send(messages[1])
            send(messages[2])
            reply = receive(2)
        finally:
            process.terminate()
            process.wait(timeout=5)
        data = reply['result']['data']
        assert all(not entry.get('errors') for entry in data), data
        return [s for entry in data for s in entry['skills'] if str(profile) in s['path']]

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
                if client == 'claude' and service.get('kind') != 'skills':
                    connection = entry['mcpServers'][service['name']]
                    assert connection['type'] == 'stdio' and connection['command'] == service['claudeAdapter']['command']
                    assert connection['env'][service['claudeAdapter']['originEnv']] == service['resource']
            if client == 'codex':
                discovered = discovered_codex()
                expected = {p['name'] + ':' + skill.name for p in catalog['plugins'] if p.get('kind') == 'skills' for skill in (source / 'plugins' / p['name'] / 'skills').iterdir()}
                assert expected.issubset({s['name'] for s in discovered}), 'Missing discovered plugin skills'
            if client == 'claude':
                details = run('claude', ['plugin', 'details', 'onul@' + catalog['name']])
                expected_count = len(list((source / 'plugins/onul/skills').iterdir()))
                assert 'planning' in details and f'Skills ({expected_count})' in details
            print(client + (' upgrade' if upgrading else ' installation') + ' verified')
    skill_packages = [p for p in catalog['plugins'] if p.get('kind') == 'skills']
    active = {p['name'] for p in skill_packages}

    def select_packages(names):
        global active
        for name in sorted(active - set(names)):
            selector = name + '@' + catalog['name']
            run('codex', ['plugin', 'remove', selector, '--json'])
            run('claude', ['plugin', 'uninstall', selector, '--scope', 'user'])
        for name in sorted(set(names) - active):
            selector = name + '@' + catalog['name']
            run('codex', ['plugin', 'add', selector, '--json'])
            run('claude', ['plugin', 'install', selector, '--scope', 'user'])
        active = set(names)
        expected = {name + ':' + folder.name for name in names
                    for folder in (source / 'plugins' / name / 'skills').iterdir()}
        actual = {s['name'] for s in discovered_codex()}
        family = {p['name'] for p in skill_packages}
        actual = {n for n in actual if n.split(':')[0] in family}
        assert actual == expected, (sorted(expected - actual), sorted(actual - expected))
        for name in names:
            details = run('claude', ['plugin', 'details', name + '@' + catalog['name']])
            match = re.search(r'Skills \(\d+\)  ([^\n]+)', details)
            assert match, details
            found = set(match.group(1).split(', '))
            wanted = {folder.name for folder in (source / 'plugins' / name / 'skills').iterdir()}
            assert found == wanted, (name, found, wanted)
        for client in clients:
            listed = json.loads(run(client, ['plugin', 'list', '--json']))
            entries = listed['installed'] if client == 'codex' else listed
            installed = {entry.get('pluginId', entry.get('id')).split('@')[0] for entry in entries if entry['enabled']}
            assert installed.intersection(family) == set(names), (client, installed, names)
        print('Client discovery and inventories verified:', ', '.join(names))

    for name in catalog['skillPackages']['categories']:
        select_packages([name])
    select_packages(list(catalog['skillPackages']['categories']))
    select_packages(['jskills'])
    select_packages(['onul'])
    select_packages(['onul-planning', 'onul-development'])
print('Client smoke checks passed without user OAuth grants or model calls')
