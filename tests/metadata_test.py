import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class MetadataTest(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        self.work = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(self.work.cleanup)
        self.root = Path(self.work.name) / 'package'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.tmp', '__pycache__'))

    def command(self, script):
        return subprocess.run([sys.executable, str(self.root / 'scripts' / script)], capture_output=True, text=True, timeout=15)

    def test_valid_package(self):
        result = self.command('validate.py')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_client_secret_in_catalog(self):
        path = self.root / 'catalog.json'
        catalog = json.loads(path.read_text())
        catalog['plugins'][0]['clientSecret'] = 'synthetic-qualification-secret'
        path.write_text(json.dumps(catalog))
        result = self.command('validate.py')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Credential field', result.stdout + result.stderr)

    def test_credential_shaped_content(self):
        path = self.root / 'README.md'
        original = path.read_text()
        for prefix in ['ghp_', 'ghs_', 'ghu_', 'gho_', 'ghr_', 'github_pat_']:
            with self.subTest(prefix=prefix):
                path.write_text(original + '\n' + prefix + 'a' * 40)
                result = self.command('validate.py')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Credential-shaped content', result.stdout + result.stderr)

    def test_symlink_escape(self):
        outside = Path(self.work.name) / 'outside.txt'
        outside.write_text('Synthetic external content')
        (self.root / 'plugins/pages/skills/outside').symlink_to(outside)
        result = self.command('validate.py')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('symlinks', result.stdout + result.stderr)

    def test_offline_scope_required(self):
        path = self.root / 'catalog.json'
        catalog = json.loads(path.read_text())
        catalog['plugins'][0]['scopes'].remove('offline_access')
        path.write_text(json.dumps(catalog))
        self.assertEqual(self.command('generate.py').returncode, 0)
        result = self.command('validate.py')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('offline access', result.stdout + result.stderr)

    def test_pages_permissions_required(self):
        path = self.root / 'catalog.json'
        original = path.read_text()
        for scope in ['pages:read', 'pages:write']:
            with self.subTest(scope=scope):
                catalog = json.loads(original)
                catalog['plugins'][0]['scopes'].remove(scope)
                path.write_text(json.dumps(catalog))
                self.assertEqual(self.command('generate.py').returncode, 0)
                result = self.command('validate.py')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('Pages read/write permissions', result.stdout + result.stderr)

    def test_eventops_access_is_read_only(self):
        path = self.root / 'catalog.json'
        original = path.read_text()
        for mutation in ['missing-read', 'write-scope', 'roles-scope', 'private-scope', 'write-capability']:
            with self.subTest(mutation=mutation):
                catalog = json.loads(original)
                service = next(item for item in catalog['plugins'] if item['name'] == 'eventops')
                if mutation == 'missing-read':
                    service['scopes'].remove('eventops:read')
                elif mutation == 'write-capability':
                    service['capabilities'].append('Write')
                else:
                    service['scopes'].append({'write-scope': 'eventops:write', 'roles-scope': 'roles', 'private-scope': 'fixture:private:read'}[mutation])
                path.write_text(json.dumps(catalog))
                self.assertEqual(self.command('generate.py').returncode, 0)
                result = self.command('validate.py')
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('published-schedule read access only', result.stdout + result.stderr)

    def test_generated_eventops_access_is_read_only(self):
        manifest = json.loads((self.root / 'plugins/eventops/.codex-plugin/plugin.json').read_text())
        self.assertEqual(manifest['interface']['capabilities'], ['Read'])
        native = json.loads((self.root / 'plugins/eventops/.mcp.codex.json').read_text())['mcpServers']['eventops']
        self.assertEqual(set(native['scopes']), {'openid', 'email', 'profile', 'eventops:read', 'offline_access'})
        self.assertEqual(native['oauth']['clientId'], 'eventops-native')
        self.assertEqual(native['oauth_resource'], 'https://eventops.onul.me')

    def test_portable_manifest_shadow(self):
        (self.root / 'plugins/pages/plugin.json').write_text('{}')
        result = self.command('validate.py')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('shadow', result.stdout + result.stderr)

    def test_generated_metadata_drift(self):
        path = self.root / 'plugins/pages/.mcp.codex.json'
        data = json.loads(path.read_text())
        del data['mcpServers']['pages']['oauth_resource']
        path.write_text(json.dumps(data))
        self.assertNotEqual(self.command('validate.py').returncode, 0)

    def test_service_path_escape(self):
        path = self.root / 'catalog.json'
        catalog = json.loads(path.read_text())
        catalog['plugins'][0]['name'] = '../../outside'
        outside = Path(self.work.name) / 'outside'
        (outside / 'skills').mkdir(parents=True)
        path.write_text(json.dumps(catalog))
        self.assertNotEqual(self.command('generate.py').returncode, 0)
        self.assertFalse((outside / '.codex-plugin/plugin.json').exists())


if __name__ == '__main__':
    unittest.main()
