---
name: github-permalink
description: Generate verified repository file links with suitable refs, UTF-8 path encoding and line anchors.
---

# Generate repository file links

Confirm the repository's canonical web host, owner and name; an SSH alias is not a web hostname.
Check that the file exists at the chosen ref, not only in an uncommitted local checkout.

Use an immutable commit for evidence tied to a revision and a branch link for intentionally living documents.
Prefer a full commit SHA for stable permalinks.
Encode the repository-relative path mechanically:

```python
from urllib.parse import quote
path = "docs/example folder/report,final.md"
encoded_path = quote(path, safe="/")
```

For GitHub files, use `https://github.com/<owner>/<repo>/blob/<commit>/<encoded-path>`.
Use `tree` for directories and append verified line anchors after the path, such as `#L10-L20`.
Confirm line numbers against that exact revision.
For a branch name containing `/`, resolve a commit instead of guessing how a renderer splits the ref from the path.
Use the target host's documented raw-file URL when bytes rather than a source viewer are needed.

Verify the resulting destination through an authorized repository API or browser.
Private links remain private; state the recipient's required access without changing repository visibility.
Do not place credentials or signed access tokens in shared links.

Example: “Link the submitted revision of docs/example folder/report,final.md.”
Resolve its committed version, encode the path and return a commit-pinned link.
