# Replit capability activation candidates

These two Replit activation entries are **unverified candidates**. The
portable skill remains the sole authoritative procedure for each capability.

| Activation source | Canonical portable procedure |
| --- | --- |
| `capabilities/resume-representative/adapters/replit/resume-representative/SKILL.md` | `capabilities/resume-representative/skills/resume-representative/SKILL.md` |
| `capabilities/professional-portfolio/adapters/replit/professional-portfolio/SKILL.md` | `capabilities/professional-portfolio/skills/professional-portfolio/SKILL.md` |

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

Use synthetic inputs and the approved Free Mode. Record exact source and entry
hashes, host/project identity, actual skill-load event and subsequent canonical
file read, synthetic output, and pre/post workspace state. Probe an unavailable
canonical target in an isolated setup; the agent should report the missing
procedure rather than pretend it loaded. A structural check or Replit's skill
preview alone does not prove this behavior. Remove or retain test outputs only
under the applicable owner and cleanup rules.

No native import, discovery, execution, automated update, host compatibility,
model equivalence, or publication is established by these sources. Host
integration remains subject to the applicable acceptance and review gates.
See [Replit Agent Skills](https://docs.replit.com/replitai/skills) and
[AF-22 native adapter acceptance](acceptance/af-22-native-adapter-acceptance.md).
