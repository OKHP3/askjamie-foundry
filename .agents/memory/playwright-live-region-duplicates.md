---
name: Workbench live-region test locators
description: Avoid ambiguous Playwright text matches when a screen-reader status repeats visible feedback.
---

The workbench places some user feedback in both a visually hidden live region and a visible confirmation. Playwright text locators can match both, producing strict-mode failures even though the user-facing confirmation is unique.

**Why:** Browser validation exposed that the visually hidden live-region copy remains available to locator matching alongside the visible status box.

**How to apply:** Scope visible-feedback assertions to the visible component (for example, `.success-box`) and screen-reader assertions to `#live-region`, checking its status role and relevant message.
