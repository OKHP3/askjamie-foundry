# AF-27 human accessibility acceptance

**Preparation status:** complete. **Human execution:** pending. This is the public-safe acceptance protocol for AF-27. The detailed worker packet and usage receipt remain private.

## Objective and evidence boundary

A human tester will exercise draft creation, editing, save and error announcements, recovery, evaluations, and export using a keyboard and a real screen reader. Record the browser, operating system, and assistive technology versions, observed focus, actual spoken output, task result, and scoped defects.

The existing browser usability check at `tests/browser/workbench-usability.py` covers shell keyboard focus, save feedback, stale-save recovery, and navigation confirmation. That automation, DOM roles, and accessibility snapshots do not establish real spoken output or human acceptance.

This protocol was prepared against source commit `0e340c5ee18396c8de59aa0b7d01780d0dce83e4`. The reviewed app-interface files remain unchanged through current `main` `992468e0032f1dcb919065f21848b23d2aee95d2`. Confirm the checkout SHA before execution.

## Prerequisites

- A human tester using a desktop screen reader and keyboard.
- A browser and operating system the tester can use. Record exact product versions and do not infer support from automation.
- A disposable checkout and a fresh temporary workbench data directory.
- Synthetic test content only. Never use client or other private capability data.
- The repository's documented Python runtime and pinned dependencies. Record the actual interpreter and dependency setup.
- A private location for screenshots or notes that may contain test data.

If any prerequisite is missing, mark the dependent scenario not run with its reason. Do not replace a human screen-reader observation with an automated snapshot.

## Setup

From the repository root, create an isolated environment, install the pinned requirements, and start the loopback-only workbench with a new disposable data directory. Follow the platform-specific virtual-environment activation command for the tester's shell.

Example launch command:

```sh
python -m workbench --port 8765 --data-dir /path/to/disposable-af27-store
```

Open `http://127.0.0.1:8765` in the recorded browser. Do not point the run at an existing `.foundry-data` directory. Record the source SHA, working-tree state, setup commands, versions, and startup result.

## Test procedure

For each step, keep the screen reader active, use keyboard input, and record the actual focus and literal spoken output. Include silence, duplicate or interrupted speech, and unexpected focus movement. Do not write an expected announcement as if it occurred.

### 1. Startup, loading, and navigation

1. Open the local workbench and listen through initial loading.
2. Use Tab and Shift+Tab to move through navigation, Refresh, New project, and the main content. Continue until focus returns to its start.
3. Activate Refresh from the keyboard and record progress and completion feedback.

**Expected outcome:** focus is visible, controls have understandable names, navigation is not trapped, and loading or refresh state is conveyed as status. Record whether the screen reader gives useful page orientation.

### 2. Create and edit a synthetic draft

1. Open **New project**. Record initial focus, dialog name, template choices, and Tab and arrow-key behavior.
2. Dismiss with **Keep looking**. Reopen the dialog and create a **Portable Agent Skill** draft.
3. Record focus after the dialog closes and after draft creation.
4. Use the editor tabs and complete the Brief, Behavior, and Evidence fields with synthetic values only. Confirm each field name and current value are understandable while navigating.
5. Change a field, move focus away, and record the unsaved state.

**Expected outcome:** the dialog opens with useful focus, its controls are named, and dismissal returns focus to its launcher. Editor tabs expose selection state and can be operated by keyboard. Fields convey their labels and values. Unsaved state is announced without taking focus away.

### 3. Save feedback and errors

1. Save the synthetic draft by keyboard.
2. Record focus before and after saving, the visible save state, and the literal spoken result.
3. If an ordinary validation or save error can be produced safely with the synthetic draft, record its wording, announcement timing, focus, and recovery guidance. Do not modify the database or inject requests to force an error.

**Expected outcome:** saved and error states are announced promptly, accurately, and without unexpected focus movement. The user can distinguish success from error and identify the next safe action.

### 4. Recovery

1. With a saved synthetic project open, edit a field and wait for the local draft state to settle.
2. Close and reopen the browser tab using the same disposable profile. Record any recovery notice, focus, and available restore or discard actions.
3. Restore the draft if offered. Record the recovered value and whether the app distinguishes local unsaved content from the saved copy.
4. Exercise stale-save recovery only when a second session on the same disposable store is available: save an update from session B, then attempt to save a different pending edit from session A. Record the warning and the **Reload saved copy** action. Do not proceed until any edits at risk have been recorded.

**Expected outcome:** recovery status and choices are announced; restore or discard actions have clear names and keyboard focus; the restored draft and any remaining save requirement are clear. The stale-save warning describes the conflict and the effect of reloading.

The existing F21 cancel/leave regression is not a separate AF-27 scenario and is not human AT evidence.

### 5. Evaluation

1. Save the synthetic draft and open Package.
2. Activate **Run evaluations** by keyboard.
3. Record the completion announcement and navigate through revision, counts, case names, statuses, details, and any stale-revision warning. If there are no cases, record that result without inventing test data.

**Expected outcome:** the evaluated revision and pass, fail, and unrun counts are clear. Case status and details are understandable in reading order, and focus stays predictable.

### 6. Export

1. Activate **Download private ZIP** by keyboard.
2. Record spoken or browser download feedback, focus, and whether the private/local nature of the export is clear.
3. If in scope, repeat for **Download backup**. Keep downloaded files private and do not attach or upload them.

**Expected outcome:** the download action is keyboard reachable and clearly named; completion is discoverable; the user can tell that the artifact is private/local. A download does not mean publication or adapter installation.

## Issue severity

- **S1 Blocker:** a core task cannot be completed with keyboard and AT, the user is trapped, or data may be lost without accessible recovery.
- **S2 Major:** a critical control or state is unavailable or misleading, preventing a safe, reliable task without an undocumented workaround.
- **S3 Moderate:** substantial friction, repeated or misordered speech, weak orientation, or a confusing but completable path.
- **S4 Minor:** low-impact wording or focus polish with a clear successful path.

For each defect, record the scenario, expected and actual result, exact spoken words, focus location, reproduction steps, severity and reason, frequency, workaround, environment, and privacy-safe evidence location. Separate confirmed observations from interpretation.

## Recording template

```text
AF-27 human accessibility acceptance
Date/time and timezone:
Tester identifier (store privately if needed):
Source commit and working-tree state:
Operating system and version:
Browser and full version:
Screen reader and version:
Speech settings and language:
Zoom, display scale, and input device:
Python version and dependency setup:
Server command and result:
Synthetic data and disposable profile confirmed: yes/no

Scenario and step:
Action and input:
Expected focus and spoken meaning:
Actual visible and screen-reader focus:
Actual literal spoken output, or silence:
Task result:
Issue ID, severity, or none:
Private evidence location:
Notes and limitations:

Overall: accepted | accepted with scoped defects | not accepted | incomplete
Defect list:
Tester sign-off and date:
Coordinator disposition:
```

## Stop rule and closure

After two failures using the same approach, stop that scenario, preserve the evidence, and change approach only with coordinator or owner direction. Stop immediately for unexpected real/private data, risk to non-disposable state, a keyboard trap, or an ambiguous destructive action.

AF-27 closes only after a human returns the completed record for every feasible scenario, marks gated scenarios not run with a reason, records exact environment versions and observed focus/spoken output, and supplies a scoped defect list or an explicit none-found result. The coordinator records disposition. The protocol and automated checks alone do not close AF-27.
