import argparse
from datetime import date, datetime, time, timedelta
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
from uuid import UUID


def under(path, roots):
    return any(path == root or root in path.parents for root in roots)


def remote_name(value):
    if not isinstance(value, str):
        return ""
    if "://" not in value:
        value = re.sub(r"^(?:[^@/:]+@)?([^/:]+):", r"ssh://\1/", value)
    if "://" not in value:
        value = "https://" + value
    parsed = urlsplit(value)
    if not parsed.hostname or not re.fullmatch(r"[A-Za-z0-9.-]+", parsed.hostname) or parsed.query or parsed.fragment:
        return ""
    return (parsed.hostname.lower() + parsed.path.removesuffix(".git")).rstrip("/")


def inventory(root, provider, repos, excluded, excluded_remotes, since, until):
    root = root.resolve()
    excluded_remotes = [remote_name(value) for value in excluded_remotes]
    if any(not value for value in excluded_remotes):
        raise ValueError("Remote exclusions require a valid host/repository prefix")
    for path in sorted(root.rglob("*.jsonl")):
        if path.is_symlink() or not under(path.resolve(), [root]):
            continue
        try:
            modified = datetime.fromtimestamp(path.stat().st_mtime).astimezone()
            if not since <= modified < until:
                continue
            with path.open(encoding="utf-8") as stream:
                line = stream.readline(1024 * 1024 + 1)
            if len(line) > 1024 * 1024:
                continue
            record = json.loads(line)
            if not isinstance(record, dict):
                continue
            if provider == "codex":
                if record.get("type") != "session_meta" or not isinstance(record.get("payload"), dict):
                    continue
                meta = record["payload"]
                if meta.get("source") == "exec" or isinstance(meta.get("source"), dict) or meta.get("parent_thread_id"):
                    continue
                identity = meta.get("id")
            else:
                meta = record
                if meta.get("isSidechain") or meta.get("isMeta"):
                    continue
                identity = meta.get("sessionId")
            identity = str(UUID(str(identity)))
            cwd = meta.get("cwd")
            if not isinstance(cwd, str) or not Path(cwd).is_absolute():
                continue
            cwd = Path(cwd).resolve()
            if not under(cwd, repos) or under(cwd, excluded):
                continue
            git = meta.get("git")
            remote = remote_name(git.get("repository_url", "")) if isinstance(git, dict) else ""
            if excluded_remotes and (not remote or any(remote == prefix or remote.startswith(prefix + "/") for prefix in excluded_remotes)):
                continue
            yield {"provider": provider, "session": identity, "cwd": str(cwd), "modified": modified.isoformat()}
        except (OSError, ValueError, TypeError):
            continue


def main():
    parser = argparse.ArgumentParser(description="Inventory authorized session metadata without exporting transcript content")
    parser.add_argument("--provider", required=True, choices=["claude", "codex"])
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--repo-root", required=True, action="append", type=Path)
    parser.add_argument("--exclude", action="append", default=[], type=Path)
    parser.add_argument("--exclude-remote", action="append", default=[])
    parser.add_argument("--since", required=True, type=date.fromisoformat)
    parser.add_argument("--until", type=date.fromisoformat, default=date.today() + timedelta(days=1))
    args = parser.parse_args()
    if args.since >= args.until:
        parser.error("--since must precede --until")
    if not args.root.is_absolute() or not args.root.is_dir() or args.root.resolve() == Path.home():
        parser.error("--root must be an existing absolute provider session directory, not the home directory")
    bounds = [datetime.combine(day, time()).astimezone() for day in [args.since, args.until]]
    rows = inventory(args.root, args.provider, [p.resolve() for p in args.repo_root],
                     [p.resolve() for p in args.exclude], [r.rstrip("/") for r in args.exclude_remote], *bounds)
    print(json.dumps(list(rows), ensure_ascii=False))


if __name__ == "__main__":
    main()
