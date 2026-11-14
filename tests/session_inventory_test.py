from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "inventory", ROOT / "plugins/onul/skills/distill-session-history/scripts/inventory.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
previous_bytecode = sys.dont_write_bytecode
sys.dont_write_bytecode = True
try:
    SPEC.loader.exec_module(MODULE)
finally:
    sys.dont_write_bytecode = previous_bytecode
SESSION = "00000000-0000-4000-8000-000000000001"
NOW = datetime(2026, 11, 14, 12, tzinfo=timezone.utc)


class SessionInventoryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "sessions"
        self.root.mkdir()
        self.repo = self.base / "project"
        self.repo.mkdir()

    def write(self, name="one", **updates):
        payload = {"id": SESSION, "cwd": str(self.repo), "source": "cli",
                   "git": {"repository_url": "git@example.org:team/project.git"}, **updates}
        path = self.root / (name + ".jsonl")
        path.write_text(json.dumps({"type": "session_meta", "payload": payload}) + '\n'
                        + '{"type":"message","secret":"synthetic-content-must-not-be-exported"}\n')
        os.utime(path, (NOW.timestamp(), NOW.timestamp()))
        return path

    def rows(self, **kwargs):
        return list(MODULE.inventory(self.root, "codex", [self.repo], kwargs.get("excluded", []),
                                    kwargs.get("remotes", []), NOW - timedelta(hours=1), NOW + timedelta(hours=1)))

    def test_exports_only_allowed_metadata(self):
        self.write()
        rows = self.rows()
        self.assertEqual(len(rows), 1)
        self.assertEqual(set(rows[0]), {"provider", "session", "cwd", "modified"})
        self.assertEqual(rows[0]["session"], SESSION)
        self.assertNotIn("synthetic-content", json.dumps(rows))

    def test_filters_other_repositories_exclusions_and_job_sessions(self):
        self.write()
        self.assertEqual(self.rows(excluded=[self.repo]), [])
        self.assertEqual(self.rows(remotes=["example.org/team"]), [])
        self.write("unknown", cwd="")
        self.write("other", cwd=str(self.base / "other"))
        self.write("job", source="exec")
        self.write("child", source={"subagent": "review"})
        self.assertEqual(len(self.rows()), 1)

    def test_ignores_symlinks_malformed_metadata_and_out_of_window_files(self):
        path = self.write()
        os.utime(path, (1, 1))
        outside = self.base / "outside.jsonl"
        outside.write_text(json.dumps({"type": "session_meta", "payload": {"id": SESSION, "cwd": str(self.repo)}}))
        (self.root / "link.jsonl").symlink_to(outside)
        (self.root / "broken.jsonl").write_text("not json")
        self.write("invalid-id", id="not-a-session-id")
        self.assertEqual(self.rows(), [])

    def test_claude_uses_first_record_only_and_exports_no_messages(self):
        path = self.root / "claude.jsonl"
        path.write_text(json.dumps({"sessionId": SESSION, "cwd": str(self.repo),
                                    "type": "user", "message": {"content": "synthetic private prompt"}}) + '\nnot json\n')
        os.utime(path, (NOW.timestamp(), NOW.timestamp()))
        rows = list(MODULE.inventory(self.root, "claude", [self.repo], [], [],
                                     NOW - timedelta(hours=1), NOW + timedelta(hours=1)))
        self.assertEqual(rows[0]["session"], SESSION)
        self.assertNotIn("message", rows[0])

    def test_remote_spellings_normalize_without_userinfo(self):
        for value in ["git@example.org:team/project.git", "https://example.org/team/project.git",
                      "ssh://git@example.org/team/project.git"]:
            self.assertEqual(MODULE.remote_name(value), "example.org/team/project")

    def test_remote_exclusions_accept_url_forms_and_skip_unknown_metadata(self):
        self.write()
        for prefix in ["example.org/team", "https://example.org/team/project.git", "git@example.org:team/project.git"]:
            with self.subTest(prefix=prefix):
                self.assertEqual(self.rows(remotes=[prefix]), [])
        for git in [{}, {"repository_url": ""}, {"repository_url": "?invalid"}, None]:
            with self.subTest(git=git):
                self.write(git=git)
                self.assertEqual(self.rows(remotes=["example.org/forbidden"]), [])
        with self.assertRaises(ValueError):
            self.rows(remotes=["?invalid"])
