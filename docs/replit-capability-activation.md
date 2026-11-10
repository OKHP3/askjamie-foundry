# Replit capability activation candidates

These Replit activation entries are **unverified candidates**. The
portable skill remains the sole authoritative procedure for each capability.

| Activation source | Canonical portable procedure |
| --- | --- |
| `capabilities/resume-representative/adapters/replit/resume-representative/SKILL.md` | `capabilities/resume-representative/skills/resume-representative/SKILL.md` |
| `capabilities/professional-portfolio/adapters/replit/professional-portfolio/SKILL.md` | `capabilities/professional-portfolio/skills/professional-portfolio/SKILL.md` |
| `capabilities/professional-portfolio/adapters/replit/aj02-buyer-reply/SKILL.md` | `capabilities/professional-portfolio/skills/professional-portfolio/SKILL.md` |

They live under the capability's `adapters/` source boundary. The repository's
`.agents/skills/` directory remains contributor tooling; this change does not
install either product skill in the shared checkout or make it discoverable.

For a controlled **test**, a host operator may place the relevant entry at the
Replit project's native `.agents/skills/<name>/SKILL.md` discovery location,
only in an authorized isolated environment that contains the corresponding
canonical procedure at the project-root path. Confirm the host, target version,
ownership, permissions, collision-free destination, and recovery plan before
installation. Do not overwrite an existing skill, include private knowledge, or
alter an active shared checkout. The temporary installed entry is a host output,
not another editable canonical source.

The buyer-reply router is an isolated Replit routing experiment, not a
general-purpose or installed product. It was drafted from the capability's
public procedure; the repository's [license](../LICENSE.md) applies. It does
not include the original GPT's knowledge files. Its repository-hosted
`verify_canonical.py` checks the **raw bytes** of the canonical AJ02 procedure
against two fixed SHA-256 pins: the reviewed LF Git blob and its exact,
complete CRLF representation. No runtime newline normalization occurs. Mixed
endings, lone CR, other content changes, missing or unreadable files, and hash
errors fail the check. Both pins must be derived and reviewed together whenever
the procedure changes, followed by fresh tests against the exact new bytes.

The host must have the repository's verifier and a working Python 3 interpreter.
From the repository root, run the verifier at
`capabilities/professional-portfolio/adapters/replit/aj02-buyer-reply/verify_canonical.py`.
Use `python3` on Replit or a suitable Python 3 launcher on Windows. The router
instructs the agent to stop without drafting if the verifier cannot run, fails,
or returns an unclear result. A verifier result and instructions to an agent
are not a host-enforced security boundary: a file could change between checking
and reading, and a malicious host or modified verifier is outside this check.
Verify actual host behavior before treating the candidate as usable.

Use synthetic inputs and the approved Free Mode. Record exact source and entry
hashes, host/project identity, actual skill-load event and subsequent canonical
file read, synthetic output, and pre/post workspace state. Probe an unavailable
canonical target in an isolated setup; the agent should report the missing
procedure rather than pretend it loaded. A structural check or Replit's skill
preview alone does not prove this behavior. Remove or retain test outputs only
under the applicable owner and cleanup rules.

No general native import, discovery, execution, automated update, host
compatibility, model equivalence, or publication is established by these sources. Host
integration remains subject to the applicable acceptance and review gates.
See [Replit Agent Skills](https://docs.replit.com/replitai/skills) and
[AF-22 native adapter acceptance](acceptance/af-22-native-adapter-acceptance.md).
