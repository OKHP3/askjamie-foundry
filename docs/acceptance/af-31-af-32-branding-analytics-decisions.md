# AF-31 and AF-32: branding and analytics decisions

**Status:** preparation published; external setting changes and analytics behavior remain pending owner decisions.  
**Source reviewed:** `OKHP3/askjamie-foundry` main at `828b94d4c90ee9d5e13189763ebc0b75a2843fdb`. The referenced implementation files are unchanged from preparation baseline `0e340c5ee18396c8de59aa0b7d01780d0dce83e4`.

## AF-31: external project branding

### Retained image choices

| Surface | Candidate | Source record | Decision point |
|---|---|---|---|
| README and public Pages card | `public/assets/social-preview.jpg`, 1774 × 887 | `docs/presentation-assets.md` identifies it as the canonical banner and Open Graph/Twitter card. | Keep as the current website and README image. |
| GitHub repository social preview | `public/assets/social-preview.jpg` | `docs/presentation-assets.md` says GitHub's Social preview setting is separate from website metadata. | Owner chooses whether to use the canonical Pages image in repository link previews. |
| GitHub social preview alternative | `assets/brand/askjamie-cover.png`, 1280 × 640; editable `askjamie-social-card.svg` | `assets/brand/README.md` lists it as a cover/social-card alternative. | Use only if the owner prefers the retained Replit-era design over the canonical Pages image. |
| Replit project avatar | `assets/brand/askjamie-avatar.png`, 512 × 512; editable `askjamie-avatar.svg` | Brand asset inventory identifies this square image as a project avatar. | Check the actual avatar crop and select explicitly. |
| Replit project cover | `assets/brand/askjamie-cover.png`, 1280 × 640 | Brand asset inventory identifies this wide image for a Replit cover. | Check the actual cover crop and select explicitly. |

**Suggested choice for owner review:** retain the workshop JPEG and A-mark icons for the public website and README; use the JPEG for the GitHub repository preview if the owner wants the same image there; use the retained square avatar and wide cover for the Replit project if their settings previews look right. This is a proposal only. No external settings have been changed.

### Apply and verify

1. Select the GitHub preview and Replit avatar/cover files.
2. In GitHub repository settings, open **Settings → General → Social preview**, upload the selected image, save, revisit the setting, and check a visible repository link preview. A cached preview may take time to refresh.
3. In the exact Replit project, update only the project avatar and/or cover selected by the owner. Reload settings and the project card to verify the saved image and visible crop. This does not change a personal account avatar.
4. Record each service separately, including selected filename, saved-setting readback, visible card evidence, date, and any cache delay.

**Closure evidence:** direct post-save readback and visible preview for GitHub, plus direct setting readback and visible avatar/cover for Replit. Source files or website metadata alone do not establish that either external setting changed.

## AF-32: public analytics notice and visitor choice

### Source behavior at the reviewed revision

- `public/index.html` loads GA4 in the head of the public orientation page and configures the supplied measurement ID.
- `scripts/build-public-artifact.py` requires the public analytics markers and rejects that tracking setup in private workbench HTML, JavaScript, and CSS.
- `docs/presentation-assets.md` explicitly separates visitor disclosure and tracking choice from the existing GA4 source. Source checks do not prove event delivery or analytics reports.
- No disclosure or tracking-choice interface was present in the reviewed public HTML.

### Owner choices

| Option | Behavior | Verification required |
|---|---|---|
| A. Disclosure only | Add clear, reachable language that accurately explains that analytics loads on page view. Do not imply an opt-out or consent control exists. | Publication reviewer approves audience, exact wording, placement, and behavior. Browser inspection confirms the notice is reachable and accurate. |
| B. Opt in before analytics | Do not load/configure GA4 until the visitor actively opts in. Decide persistence and how the choice can be changed. | In clean browser sessions, verify no analytics request before opt-in, expected request after opt-in, rejection behavior, and the chosen persistence/change behavior. |
| C. Remove GA4 | Remove the public page's GA4 loader/configuration and do not substitute another tracker without a separate decision. | Verify the source/build expectations and confirm the live page sends no GA4 request. |

Choose the intended audience, option, notice placement, and (for B) persistence/change behavior before implementation. Obtain review of the exact visitor-facing text. This record makes no conclusion about which legal requirements apply.

### Implement and verify after the decision

1. Record the audience and selected A/B/C behavior, plus approved exact wording.
2. Implement only the selected behavior in the public orientation surface. Keep tracking out of the private workbench and generated packages.
3. Run the applicable public-artifact validation and project checks. Record the tested commit and environment.
4. Inspect the public page in a clean browser profile. Check the notice and accessibility path, then observe analytics network requests against the chosen behavior.
5. After an authorized Pages release, verify the deployed page and record URL, date, browser, and result.

**Closure evidence:** owner-selected audience and behavior, publication approval of exact wording, source checks at the implemented commit, public-browser behavior, and post-release verification. A passing source check alone does not prove notice visibility, visitor choice, or third-party event collection.

## Evidence and current gates

The public asset inventory is in `docs/presentation-assets.md` (canonical images and settings surfaces, lines 9–74). Recovered alternatives are listed in `assets/brand/README.md` (contents and usage). GA4 loading is visible in `public/index.html` (head scripts); public/private source guards are in `scripts/build-public-artifact.py` (analytics markers and private-workbench scan). These paths were checked at the source revision above; no settings, build, test, live browser, or analytics report was changed or run for this preparation.

**Remaining owner inputs:** select GitHub/Replit images; select analytics audience and option A/B/C; approve exact disclosure wording. Until those inputs and the stated readbacks are available, AF-31 and AF-32 remain open.
