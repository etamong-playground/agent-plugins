import types
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'plugins/onul/skills/explain-code-change/scripts/validate_html.py'
validator = types.ModuleType('explainer_validator')
exec(compile(source.read_text(), str(source), 'exec'), validator.__dict__)
CSP = "; ".join(key + ' ' + ' '.join(values) for key, values in validator.EXPECTED_CSP.items())
META = '<meta http-equiv="Content-Security-Policy" content="' + CSP + '">'
SECTIONS = ''.join('<section id="' + name + '"></section>' for name in sorted(validator.REQUIRED_SECTIONS))


def errors(html):
    parser = validator.ExplainerValidator()
    parser.feed(html)
    return parser.finish()


class ExplainerContractTest(unittest.TestCase):
    def test_valid_offline_document(self):
        self.assertEqual(errors('<html><head>' + META + '</head><body>' + SECTIONS + '<script>const answer = 2;</script></body></html>'), [])

    def test_script_before_policy_is_rejected(self):
        html = '<html><head><script>new Image().src="https://example.invalid/beacon";</script>' + META + '</head><body>' + SECTIONS + '</body></html>'
        self.assertTrue(errors(html))

    def test_policy_outside_head_is_rejected(self):
        self.assertTrue(errors('<html><head></head><body>' + META + SECTIONS + '<script>const answer = 2;</script></body></html>'))

    def test_loading_and_dom_insertion_are_rejected(self):
        for payload in ['<img\nsrc="https://example.invalid/a">', '<script>document.body.innerHTML = value;</script>', '<style>body {background: url(https://example.invalid/a)}</style>']:
            with self.subTest(payload=payload):
                self.assertTrue(errors('<html><head>' + META + '</head><body>' + SECTIONS + '<script>const answer = 2;</script>' + payload + '</body></html>'))

    def test_missing_sections_and_changed_policy_are_rejected(self):
        self.assertTrue(errors('<html><head>' + META + '</head><body><script>const answer = 2;</script></body></html>'))
        self.assertTrue(errors('<html><head>' + META.replace("default-src 'none'", "default-src *") + '</head><body>' + SECTIONS + '<script>const answer = 2;</script></body></html>'))

    def test_duplicate_policy_attributes_are_rejected(self):
        meta = META.replace('http-equiv="Content-Security-Policy"', 'http-equiv="x" http-equiv="Content-Security-Policy"')
        self.assertTrue(errors('<html><head>' + meta + '<script>new Image().src="https://example.invalid/beacon";</script></head><body>' + SECTIONS + '</body></html>'))
