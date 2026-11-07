---
name: Canceled browser refreshes
description: Playwright behavior when a beforeunload prompt is dismissed during a reload.
---

When a browser `beforeunload` prompt is dismissed, the refresh is canceled, but Playwright's `page.reload()` may still wait for navigation until its timeout. Catch that expected timeout only after confirming the beforeunload dialog was handled, then assert the current page state remains intact.

**Why:** Browser acceptance coverage for retaining unsaved drafts needs to distinguish a canceled refresh from a successful reload without treating Playwright's navigation wait as a product failure.

**How to apply:** In a reload-cancellation test, use a short explicit navigation timeout, verify the captured dialog type, then check that the edited value and unsaved indicator remain visible.
