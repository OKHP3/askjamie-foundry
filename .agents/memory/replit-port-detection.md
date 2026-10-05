---
name: Replit port auto-detection
description: Handle incidental `.replit` port mappings caused by temporary local servers.
---

A one-off shell HTTP server bound to port 5000 may cause Replit to append a `[[ports]]` mapping to `.replit`. Direct edits to `.replit` are blocked by the workspace; write the intended full TOML to a temporary file inside the workspace and use `verifyAndReplaceDotReplit({ tempFilePath })` to apply a validated replacement.

**Why:** During a static-artifact preview, starting a temporary server resulted in an unrelated port mapping being added to project configuration. Direct patching was rejected, while the validation callback safely restored the prior configuration.

**How to apply:** After using a temporary server, inspect `git diff -- .replit`. If a mapping is incidental, preserve all other TOML, remove only that mapping in a temp file, validate and replace it, then confirm the diff is clean.