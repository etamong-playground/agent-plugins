import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import skill_packages

ROOT = Path(__file__).resolve().parents[1]


class CategoryPackagesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.tmp', '__pycache__'))

    def run_script(self, name, *args):
        return subprocess.run([sys.executable, str(self.root / 'scripts' / name), *args],
                              text=True, capture_output=True, timeout=20)

    def test_categories_have_one_owner_and_complete_resources(self):
        config = json.loads((self.root / 'catalog.json').read_text())['skillPackages']
        source = self.root / 'plugins/onul'
        seen = set()
        for package, names in config['categories'].items():
            self.assertFalse(seen.intersection(names))
            seen.update(names)
            folder = self.root / 'plugins' / package
            self.assertEqual({p.name for p in (folder / 'skills').iterdir()}, set(names))
            manifest = json.loads((folder / 'sources.json').read_text())
            for item in manifest['skills']:
                for relative, expected in item['sha256'].items():
                    actual = (folder / 'skills' / item['name'] / relative).read_bytes()
                    self.assertEqual(actual, (source / 'skills' / item['name'] / relative).read_bytes())
                    self.assertEqual(hashlib.sha256(actual).hexdigest(), expected)
                self.assertEqual((folder / item['license']).read_bytes(), (source / item['license']).read_bytes())
        self.assertEqual(seen, {p.name for p in (source / 'skills').iterdir()})
        legacy = self.root / 'plugins/jskills/skills'
        self.assertTrue((legacy / 'feature-planning/SKILL.md').is_file())
        self.assertFalse((legacy / 'planning').exists())
        self.assertIn('\nname: feature-planning\n', (legacy / 'feature-planning/SKILL.md').read_text())

    def test_changed_and_missing_category_resource_fail_check_and_regenerate(self):
        path = self.root / 'plugins/onul-development/skills/tdd/tests.md'
        original = path.read_bytes()
        path.write_bytes(b'wrong resource')
        self.assertNotEqual(self.run_script('generate.py', '--check').returncode, 0)
        self.assertEqual(self.run_script('generate.py').returncode, 0)
        self.assertEqual(path.read_bytes(), original)
        path.unlink()
        self.assertNotEqual(self.run_script('generate.py', '--check').returncode, 0)

    def test_duplicate_or_missing_category_membership_is_rejected(self):
        path = self.root / 'catalog.json'
        original = json.loads(path.read_text())
        for change in ['duplicate', 'missing']:
            catalog = json.loads(json.dumps(original))
            categories = catalog['skillPackages']['categories']
            if change == 'duplicate':
                categories['onul-writing'].append('tdd')
            else:
                categories['onul-development'].remove('tdd')
            path.write_text(json.dumps(catalog))
            self.assertNotEqual(self.run_script('generate.py').returncode, 0)

    def test_unsafe_mapping_and_symlink_do_not_materialize_external_content(self):
        path = self.root / 'catalog.json'
        original = json.loads(path.read_text())
        original['skillPackages']['legacy']['../../escape'] = {}
        path.write_text(json.dumps(original))
        self.assertNotEqual(self.run_script('generate.py').returncode, 0)
        self.assertFalse((self.root.parent / 'escape').exists())
        path.write_text((ROOT / 'catalog.json').read_text())
        folder = self.root / 'plugins/onul/skills/tdd'
        shutil.rmtree(folder)
        folder.symlink_to(ROOT / 'plugins/onul/skills/tdd', target_is_directory=True)
        self.assertNotEqual(self.run_script('generate.py').returncode, 0)

    def test_stale_generated_resource_is_detected_and_removed(self):
        stale = self.root / 'plugins/onul-writing/skills/old/SKILL.md'
        stale.parent.mkdir()
        stale.write_text('old edition')
        self.assertNotEqual(self.run_script('generate.py', '--check').returncode, 0)
        self.assertEqual(self.run_script('generate.py').returncode, 0)
        self.assertFalse(stale.exists())
        self.assertFalse(stale.parent.exists())
        self.assertEqual(self.run_script('generate.py', '--check').returncode, 0)

    def test_unreviewed_metadata_resource_is_rejected(self):
        path = self.root / 'plugins/onul-writing/.claude-plugin/private-notes.md'
        path.write_text('unreviewed synthetic notes')
        result = self.run_script('generate.py', '--check')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Stale generated resource', result.stderr)

    def test_editions_do_not_depend_on_filesystem_enumeration_order(self):
        baseline = skill_packages.editions(self.root)
        original = Path.rglob
        def reversed_entries(path, pattern):
            return iter(reversed(list(original(path, pattern))))
        with patch.object(Path, 'rglob', reversed_entries):
            self.assertEqual(skill_packages.editions(self.root), baseline)
