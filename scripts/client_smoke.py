import json
import os
import select
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

from client_env import isolated_environment

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
    git_env = isolated_environment(os.environ)
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
        for variable, folder in [('HOME', 'home'), ('XDG_CONFIG_HOME', 'config'), ('XDG_CACHE_HOME', 'cache'), ('XDG_STATE_HOME', 'state'), ('TMPDIR', 'tmp')]:
            directory = profile / folder
            directory.mkdir(mode=0o700)
            env[variable] = str(directory)
        env.update(TEMP=env['TMPDIR'], TMP=env['TMPDIR'])
        env['CODEX_HOME' if client == 'codex' else 'CLAUDE_CONFIG_DIR'] = str(profile)
        env.update(CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='1', DISABLE_AUTOUPDATER='1', SCHEDULER_NO_UPDATE='1', PAGES_NO_UPDATE='1', EVENTOPS_NO_UPDATE='1', SPORTS_NO_UPDATE='1', GIT_TERMINAL_PROMPT='0')
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
            subprocess.run([sys.executable, str(source / 'scripts/generate.py')], env=git_env, cwd=source, check=True)
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
                if client == 'codex':
                    installed_root = Path(entry['source']['path']).resolve()
                    assert installed_root.is_relative_to(clients[client][0].resolve())
                    manifest = json.loads((installed_root / '.codex-plugin/plugin.json').read_text())
                    component = (installed_root / manifest['mcpServers']).resolve()
                    assert component.is_relative_to(installed_root)
                    installed_connection = json.loads(component.read_text())['mcpServers'][service['name']]
                    expected_connection = json.loads((source / 'plugins' / service['name'] / '.mcp.codex.json').read_text())['mcpServers'][service['name']]
                    assert installed_connection == expected_connection, (client, selector)
                    if service.get('codexAdapter'):
                        assert manifest['requires_local_executor'] is True
                        assert installed_connection == {'type': 'stdio', 'command': service['codexAdapter']['command'], 'args': ['mcp']}
                assert entry['enabled'] and entry['version'] == service['version'], (client, selector)
                if client == 'claude':
                    connection = entry['mcpServers'][service['name']]
                    assert connection['type'] == 'stdio' and connection['command'] == service['claudeAdapter']['command']
                    if service['claudeAdapter'].get('originEnv'):
                        assert connection['env'][service['claudeAdapter']['originEnv']] == service['resource']
                    else:
                        assert not connection.get('env')
            print(client + (' upgrade' if upgrading else ' installation') + ' verified')
    profile, client_env = clients['codex']
    with (work / 'app-server.stderr').open('wb') as errors:
        process = subprocess.Popen(['codex', 'app-server', '--stdio'], cwd=profile, env=client_env,
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=errors)
        buffer = bytearray()

        def send(value):
            process.stdin.write((json.dumps(value) + '\n').encode())
            process.stdin.flush()

        def rpc(identifier, method, params):
            send({'id': identifier, 'method': method, 'params': params})
            deadline = time.monotonic() + 20
            while time.monotonic() < deadline:
                while b'\n' in buffer:
                    line, _, remainder = buffer.partition(b'\n')
                    buffer[:] = remainder
                    value = json.loads(line)
                    if value.get('id') == identifier:
                        if 'error' in value:
                            raise RuntimeError('Codex skill inventory failed: ' + str(value['error']))
                        return value['result']
                if process.poll() is not None:
                    raise RuntimeError('Codex inventory ended before its response')
                ready, _, _ = select.select([process.stdout], [], [], max(0, deadline - time.monotonic()))
                if ready:
                    chunk = os.read(process.stdout.fileno(), 65536)
                    if not chunk:
                        raise RuntimeError('Codex inventory stream closed')
                    buffer.extend(chunk)
            raise TimeoutError('Codex inventory did not return within 20 seconds')

        try:
            rpc(1, 'initialize', {'clientInfo': {'name': 'service-plugin-qualification', 'version': '0.1.0'},
                                  'capabilities': {'experimentalApi': True}})
            send({'method': 'initialized'})
            inventory = rpc(2, 'skills/list', {'cwds': [str(profile)], 'forceReload': True})
            skills = [skill for entry in inventory['data'] for skill in entry['skills']]
            for service in catalog['plugins']:
                for canonical in (root / 'plugins' / service['name'] / 'skills').glob('*/SKILL.md'):
                    skill = next(item for item in skills if item['name'].endswith(canonical.parent.name)
                                 and item['enabled'] and Path(item['path']).resolve().is_relative_to(profile.resolve()))
                    if Path(skill['path']).read_bytes() != canonical.read_bytes():
                        raise AssertionError('Codex discovered a different shared skill: ' + service['name'])
            print('Codex runtime discovered every installed shared service skill')
        finally:
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)
    for service in catalog['plugins']:
        details = run('claude', ['plugin', 'details', service['name'] + '@' + catalog['name']])
        for skill in (root / 'plugins' / service['name'] / 'skills').glob('*/SKILL.md'):
            if skill.parent.name not in details:
                raise AssertionError('Claude component inventory missed a shared skill: ' + service['name'])
    print('Claude component inventory discovered every installed shared service skill')
print('Client smoke checks passed without user OAuth grants or model calls')
