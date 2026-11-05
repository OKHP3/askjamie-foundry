---
name: Playwright route races
description: Workspace lesson for deterministic delayed-response browser tests.
---

For browser tests that delay or fail a specific request, intercept its exact URL and keep one route handler active for the race. Avoid overlapping wildcard handlers across sequential race cases; Playwright can attempt more than one handler action on the same request and report that the route was already handled. Use an explicit event to signal when the delayed response has actually completed instead of assuming `networkidle` proves it.

**Why:** A delayed project-switch failure test initially produced route-already-handled errors and a false timing assumption around `networkidle`; exact matching, one handler, and explicit completion signaling made the test deterministic.

**How to apply:** For browser acceptance races, route only the endpoint under test, use one controlled handler or remove it completely before registering another, and wait for an event set after `continue_()` or `fulfill()` completes.
