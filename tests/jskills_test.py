import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_jskills', ROOT / 'scripts/build_jskills.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for key in ['href', 'src']:
            if key in attrs:
                self.links.append(attrs[key])


class JskillsTest(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.original_plugin = builder.PLUGIN
        self.addCleanup(setattr, builder, 'PLUGIN', self.original_plugin)

    def test_downloads_preserve_originals_and_licenses(self):
        output = self.work / 'site'
        builder.build(output)
        manifest = builder.SOURCE
        with zipfile.ZipFile(output / 'downloads/jskills.zip') as full:
            self.assertIn('jskills/.claude-plugin/plugin.json', full.namelist())
            self.assertIn('jskills/.codex-plugin/plugin.json', full.namelist())
            for skill in manifest['skills']:
                with zipfile.ZipFile(output / 'downloads' / (skill['name'] + '.zip')) as single:
                    self.assertIn('Copyright (c) 2026 Matt Pocock', single.read(skill['name'] + '/LICENSE').decode())
                    for name, expected in skill['sha256'].items():
                        data = full.read('jskills/skills/' + skill['name'] + '/' + name)
                        self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
                        self.assertEqual(single.read(skill['name'] + '/' + name), data)
            script = 'jskills/skills/diagnosing-bugs/scripts/hitl-loop.template.sh'
            self.assertFalse((full.getinfo(script).external_attr >> 16) & 0o111)
            with zipfile.ZipFile(output / 'downloads/diagnosing-bugs.zip') as single:
                self.assertFalse((single.getinfo('diagnosing-bugs/scripts/hitl-loop.template.sh').external_attr >> 16) & 0o111)
            self.assertFalse(any('..' in Path(name).parts or name.startswith('/') for name in full.namelist()))
        for line in (output / 'downloads/SHA256SUMS.txt').read_text().splitlines():
            expected, name = line.split('  ')
            self.assertEqual(hashlib.sha256((output / 'downloads' / name).read_bytes()).hexdigest(), expected)
        links = Links()
        links.feed((output / 'index.html').read_text())
        for link in links.links:
            if link.startswith('#'):
                self.assertTrue(link == '#' or link[1:] in links.ids, link)
            elif not link.startswith('https://'):
                self.assertTrue((output / link).is_file(), link)

    def test_build_is_reproducible_and_refuses_overwrite(self):
        first, second = self.work / 'first', self.work / 'second'
        builder.build(first)
        builder.PLUGIN = self.work / 'mode-changed-plugin'
        shutil.copytree(self.original_plugin, builder.PLUGIN)
        (builder.PLUGIN / 'skills/diagnosing-bugs/scripts/hitl-loop.template.sh').chmod(0o755)
        builder.build(second)
        self.assertEqual((first / 'downloads/jskills.zip').read_bytes(), (second / 'downloads/jskills.zip').read_bytes())
        with self.assertRaises(FileExistsError):
            builder.build(first)

    def test_modified_missing_and_private_originals_are_rejected(self):
        builder.PLUGIN = self.work / 'plugin'
        shutil.copytree(self.original_plugin, builder.PLUGIN)
        target = builder.PLUGIN / 'skills/grilling/SKILL.md'
        original = target.read_bytes()
        for suffix in [b'\nChanged original', b'\n/Users/private-owner/project']:
            target.write_bytes(original + suffix)
            with self.assertRaises(ValueError):
                builder.build(self.work / 'unpublished')
            self.assertFalse((self.work / 'unpublished').exists())
        target.unlink()
        with self.assertRaises(ValueError):
            builder.build(self.work / 'unpublished')

    def test_unreviewed_root_file_and_symlink_are_rejected(self):
        builder.PLUGIN = self.work / 'plugin'
        shutil.copytree(self.original_plugin, builder.PLUGIN)
        extra = builder.PLUGIN / 'debug.txt'
        extra.write_text('unreviewed local notes')
        with self.assertRaisesRegex(ValueError, 'unexpected'):
            builder.build(self.work / 'unpublished')
        extra.unlink()
        outside = self.work / 'private.txt'
        outside.write_text('private local notes')
        extra.symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            builder.build(self.work / 'unpublished')
        self.assertFalse((self.work / 'unpublished').exists())

    def test_truncated_license_is_rejected(self):
        builder.PLUGIN = self.work / 'plugin'
        shutil.copytree(self.original_plugin, builder.PLUGIN)
        (builder.PLUGIN / 'LICENSE').write_text('Copyright (c) 2026 Matt Pocock')
        with self.assertRaisesRegex(ValueError, 'MIT notice'):
            builder.build(self.work / 'unpublished')
        self.assertFalse((self.work / 'unpublished').exists())


if __name__ == '__main__':
    unittest.main()
