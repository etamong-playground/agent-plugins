import hashlib
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from urllib.parse import urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
spec = importlib.util.spec_from_file_location('build_onul', ROOT / 'scripts/build_onul.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.id_counts = {}
        self.id_panels = {}
        self.sections = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'section':
            self.sections.append(attrs.get('data-purpose', self.sections[-1] if self.sections else None))
        if 'id' in attrs:
            self.ids.add(attrs['id'])
            self.id_counts[attrs['id']] = self.id_counts.get(attrs['id'], 0) + 1
            self.id_panels[attrs['id']] = self.sections[-1] if self.sections else None
        for key in ['href', 'src']:
            if key in attrs:
                self.links.append(attrs[key])

    def handle_endtag(self, tag):
        if tag == 'section':
            self.sections.pop()


class JskillsTest(unittest.TestCase):
    def setUp(self):
        (ROOT / '.tmp').mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / '.tmp')
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)
        self.original_plugin = builder.PLUGIN
        self.addCleanup(setattr, builder, 'PLUGIN', self.original_plugin)

    def test_page_displays_the_version_of_its_downloaded_package(self):
        builder.PLUGIN = self.work / 'plugin'
        shutil.copytree(self.original_plugin, builder.PLUGIN)
        for name in ['.claude-plugin/plugin.json', '.codex-plugin/plugin.json']:
            path = builder.PLUGIN / name
            data = json.loads(path.read_text())
            data['version'] = '9.8.7'
            path.write_text(json.dumps(data))
        output = self.work / 'site'
        builder.build(output)

        class VersionText(HTMLParser):
            def __init__(self):
                super().__init__()
                self.active = False
                self.text = []

            def handle_starttag(self, tag, attrs):
                if tag == 'span' and 'release-version' in dict(attrs).get('class', '').split():
                    self.active = True

            def handle_data(self, text):
                if self.active:
                    self.text.append(text)

            def handle_endtag(self, tag):
                if tag == 'span':
                    self.active = False

        page = VersionText()
        page.feed((output / 'index.html').read_text())
        self.assertEqual(page.text, ['v9.8.7'])
        with zipfile.ZipFile(output / 'downloads/onul.zip') as bundle:
            manifest = json.loads(bundle.read('onul/.claude-plugin/plugin.json'))
            self.assertEqual(manifest['version'], '9.8.7')

    def test_downloads_preserve_originals_and_licenses(self):
        output = self.work / 'site'
        builder.build(output)
        manifest = builder.SOURCE
        with zipfile.ZipFile(output / 'downloads/onul.zip') as full:
            self.assertIn('onul/.claude-plugin/plugin.json', full.namelist())
            self.assertIn('onul/.codex-plugin/plugin.json', full.namelist())
            for skill in manifest['skills']:
                with zipfile.ZipFile(output / 'downloads' / (skill['name'] + '.zip')) as single:
                    self.assertEqual(single.read(skill['name'] + '/LICENSE'), (builder.PLUGIN / skill['license']).read_bytes())
                    for name, expected in skill['sha256'].items():
                        data = full.read('onul/skills/' + skill['name'] + '/' + name)
                        self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
                        self.assertEqual(single.read(skill['name'] + '/' + name), data)
            script = 'onul/skills/diagnosing-bugs/scripts/hitl-loop.template.sh'
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
                self.assertTrue((output / urlsplit(link).path).is_file(), link)

    def test_asset_update_changes_its_public_cache_key(self):
        fixture = self.work / 'fixture'
        shutil.copytree(ROOT / 'site', fixture / 'site')
        old_root = builder.ROOT
        self.addCleanup(setattr, builder, 'ROOT', old_root)
        builder.ROOT = fixture
        first, second = self.work / 'first', self.work / 'second'
        builder.build(first)
        css = fixture / 'site/onul/style.css'
        css.write_text(css.read_text() + '\nbody { outline: none; }\n')
        builder.build(second)
        urls = []
        for output in [first, second]:
            links = Links()
            links.feed((output / 'index.html').read_text())
            url = next(link for link in links.links if urlsplit(link).path == 'style.css')
            self.assertTrue(urlsplit(url).query)
            self.assertEqual((output / urlsplit(url).path).read_bytes(), (output / 'style.css').read_bytes())
            urls.append(url)
        self.assertNotEqual(*urls)

    def test_published_fragments_still_resolve_in_the_correct_purpose(self):
        output = self.work / 'site'
        builder.build(output)
        links = Links()
        links.feed((output / 'index.html').read_text())
        for fragment, purpose in {'_1': 'product', '_7': 'installation', 'codex': 'installation', 'jskills': 'product', 'mac-첫-앱의-범위-정하기': 'mac', 'mac-실시간-기능과-배포로-확장하기': 'mac'}.items():
            self.assertEqual(links.id_panels[fragment], purpose)
        self.assertTrue(all(count == 1 for count in links.id_counts.values()))

    def test_navigation_script_changes_its_public_cache_key(self):
        fixture = self.work / 'fixture'
        shutil.copytree(ROOT / 'site', fixture / 'site')
        old_root = builder.ROOT
        self.addCleanup(setattr, builder, 'ROOT', old_root)
        builder.ROOT = fixture
        first, second = self.work / 'first', self.work / 'second'
        builder.build(first)
        script = fixture / 'site/onul/tabs.js'
        script.write_text(script.read_text() + '\nvoid 0;\n')
        builder.build(second)
        urls = []
        for output in [first, second]:
            links = Links()
            links.feed((output / 'index.html').read_text())
            url = next(link for link in links.links if urlsplit(link).path == 'tabs.js')
            self.assertTrue(urlsplit(url).query)
            urls.append(url)
        self.assertNotEqual(*urls)

    def test_build_is_reproducible_and_refuses_overwrite(self):
        first, second = self.work / 'first', self.work / 'second'
        builder.build(first)
        builder.PLUGIN = self.work / 'mode-changed-plugin'
        shutil.copytree(self.original_plugin, builder.PLUGIN)
        (builder.PLUGIN / 'skills/diagnosing-bugs/scripts/hitl-loop.template.sh').chmod(0o755)
        builder.build(second)
        self.assertEqual((first / 'downloads/onul.zip').read_bytes(), (second / 'downloads/onul.zip').read_bytes())
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
