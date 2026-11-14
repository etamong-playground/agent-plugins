# Provider routes

Verify the installed CLI help or exposed tool schema on the execution host before using a route.
Model, permission, worktree and repository choices come from that host's guidance and explicit user request.
Never bypass a runtime restriction through another launcher.

## Claude Code

Inspect `claude --help` and the supported session-list, attach, stop and removal commands.
A supported background route may expose `--bg`, `--model`, `--permission-mode` and a session name; choose each explicitly under the existing policy, without widening permissions to remove a prompt.
Record the full returned session identity, host and directory, then verify state through the supported listing interface.
Capture listings in memory and expose only the task-owned identity, name, state and directory.
If no supported message route exists, agree on a coordinator-readable result artifact or user relay before dispatch.
Do not invent a send command or read private inbox files as a substitute.
A resume may create a copy; verify the returned identity before messaging or launching again.
Stopping execution and deleting a session/worktree are separate operations.
See [Claude Code agent view](https://code.claude.com/docs/en/agent-view) and installed help for current interfaces.

## Codex

When app tools are exposed, inspect the schemas for chat creation, messaging, bounded waits and archiving.
Create a user-owned chat only when the runtime's human-authorization requirements are met; use native delegation for internal subtasks when permitted.
Record final thread and host identities after any asynchronous setup and verify progress through the supported wait interface.
Queue acceptance is delivery registration, not receipt or completion.

For an explicitly authorized bounded CLI job, inspect `codex exec --help` and its resume help.
Use an isolated task worktree, explicit permitted model and existing sandbox/approval settings.
A non-interactive job is not an interactive chat, a remote-control connection or an autonomous goal.
Do not assume a queue command exists: use it only when installed help actually advertises it and the target/reply authorization is established.
Preserve the full job identity and process handle, and sanitize the event stream in memory rather than saving raw logs.
Use a supported stop or goal interface and verify the state; archiving alone does not confirm execution stopped.
See [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode).
