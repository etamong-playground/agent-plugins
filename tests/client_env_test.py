import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('client_env', ROOT / 'scripts/client_env.py')
client_env = importlib.util.module_from_spec(spec)
spec.loader.exec_module(client_env)


class ClientEnvironmentTest(unittest.TestCase):
    def test_retains_only_runtime_environment(self):
        ambient = {key: 'synthetic-value' for key in [
            'AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'AWS_SESSION_TOKEN',
            'AZURE_CLIENT_SECRET', 'GOOGLE_APPLICATION_CREDENTIALS', 'SSH_AUTH_SOCK',
            'OPENAI_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'CODEX_HOME', 'CLAUDE_CONFIG_DIR',
            'HOME', 'XDG_CONFIG_HOME', 'GIT_CONFIG_GLOBAL', 'HTTP_PROXY', 'TMPDIR',
        ]}
        ambient.update(PATH='/fixture/bin', LANG='C.UTF-8')
        self.assertEqual(client_env.isolated_environment(ambient), {'PATH': '/fixture/bin', 'LANG': 'C.UTF-8'})
        self.assertIn('AWS_SECRET_ACCESS_KEY', ambient)


if __name__ == '__main__':
    unittest.main()
